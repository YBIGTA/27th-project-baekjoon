import time
import json
import base64

from app.config import celery_app, ssm_client, REMOTE_EXECUTOR_PATH, IDLE_INSTANCE_WAIT_TIMEOUT, IDLE_INSTANCE_POLL_INTERVAL
from app import ec2_manager



@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def run_code_task(self, language: str, code: str):
    """
    SSM Run Command를 통해 원격 EC2 인스턴스에서 코드를 실행하는 Celery 작업입니다.
    """
    instance_id = None
    try:
        # 1. 유휴 EC2 인스턴스 가져오기
        start_time = time.time()
        while time.time() - start_time < IDLE_INSTANCE_WAIT_TIMEOUT:
            instance_id = ec2_manager.get_idle_instance_id()
            if instance_id:
                break
            print(f"사용 가능한 유휴 인스턴스가 없습니다. {IDLE_INSTANCE_POLL_INTERVAL}초 동안 기다립니다...")
            time.sleep(IDLE_INSTANCE_POLL_INTERVAL)
        
        if not instance_id:
            print("유휴 인스턴스를 기다리는 동안 시간이 초과되었습니다. 작업을 다시 시도합니다...")
            raise self.retry(exc=Exception("사용 가능한 유휴 EC2 인스턴스가 없습니다."))

        print(f"코드 실행을 위해 인스턴스 {instance_id}를 확보했습니다.")

        # 2. SSM 명령 준비 및 전송
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        command = [
            f"python3 {REMOTE_EXECUTOR_PATH} --language '{language}' --code_base64 '{encoded_code}'"
        ]
        
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': command},
            TimeoutSeconds=300 # 명령 자체에 대한 5분 시간 초과
        )
        command_id = response['Command']['CommandId']
        print(f"SSM 명령 {command_id}를 인스턴스 {instance_id}로 보냈습니다.")

        # 3. 명령이 완료될 때까지 기다립니다.
        waiter = ssm_client.get_waiter('command_executed')
        waiter.wait(
            CommandId=command_id,
            InstanceId=instance_id,
            WaiterConfig={
                'Delay': 2,
                'MaxAttempts': 150
            }
        )

        # 4. 명령 출력 가져오기
        output = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )

        if output['Status'] == 'Success':
            remote_result_str = output['StandardOutputContent']
            try:
                result = json.loads(remote_result_str)
                print(f"명령이 성공했습니다. 결과: {result}")
                return result
            except json.JSONDecodeError:
                # 원격 스크립트 출력이 유효한 JSON이 아닌 경우 처리
                print(f"원격 스크립트 출력에서 JSON 디코딩 오류: {remote_result_str}")
                return {"error": "원격 스크립트가 잘못된 형식의 데이터를 반환했습니다."}
        else:
            error_message = output.get('StandardErrorContent', 'SSM 명령이 stderr 없이 실패했습니다.')
            print(f"SSM 명령이 실패했습니다. 오류: {error_message}")
            return {"error": error_message}

    except Exception as e:
        print(f"run_code_task에서 오류가 발생했습니다: {e}")
        raise self.retry(exc=e)

    finally:
        # 5. 항상 인스턴스를 풀로 다시 해제합니다.
        if instance_id:
            print(f"인스턴스 {instance_id}를 풀로 다시 해제합니다.")
            ec2_manager.set_instance_status(instance_id, "Idle")