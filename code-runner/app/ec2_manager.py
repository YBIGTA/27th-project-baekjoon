from botocore.exceptions import ClientError
from app.config import (
    ec2_client,
    EC2_AMI_ID,
    EC2_INSTANCE_TYPE,
    EC2_SECURITY_GROUP_ID,
    EC2_IAM_INSTANCE_PROFILE_ARN
)

def set_instance_status(instance_id: str, status: str):
    """EC2 인스턴스의 'Status' 태그를 설정합니다."""
    print(f"인스턴스 {instance_id}의 상태를 '{status}'로 설정 중...")
    try:
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[{'Key': 'Status', 'Value': status}]
        )
        print(f"인스턴스 {instance_id}의 상태를 성공적으로 설정했습니다.")
    except ClientError as e:
        print(f"인스턴스 {instance_id}의 상태 설정 중 AWS 오류 발생: {e}")
    except Exception as e:
        print(f"인스턴스 {instance_id}의 상태 설정 중 예기치 않은 오류 발생: {e}")

def provision_instances(count: int = 3):
    """
    여러 개의 EC2 인스턴스를 프로비저닝하고 'Idle'로 태그를 지정합니다.
    """
    print(f"{count}개의 인스턴스를 프로비저닝 중...")
    try:
        response = ec2_client.run_instances(
            ImageId=EC2_AMI_ID,
            InstanceType=EC2_INSTANCE_TYPE,
            MinCount=count,
            MaxCount=count,
            SecurityGroupIds=[EC2_SECURITY_GROUP_ID],
            IamInstanceProfile={'Arn': EC2_IAM_INSTANCE_PROFILE_ARN},
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'code-runner-worker'},
                        {'Key': 'ManagedBy', 'Value': 'Baekjoon-Code-Runner'},
                        {'Key': 'Status', 'Value': 'Initializing'}
                    ]
                }
            ]
        )
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        print(f"인스턴스를 성공적으로 프로비저닝했습니다: {instance_ids}")
        
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=instance_ids)
        print(f"인스턴스 {instance_ids}가 실행 중입니다.")
        for instance_id in instance_ids:
            set_instance_status(instance_id, "Idle")
            
        return instance_ids
    except ClientError as e:
        print(f"인스턴스 프로비저닝 중 AWS 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"인스턴스 프로비저닝 중 예기치 않은 오류 발생: {e}")
        return []

def get_idle_instance_id():
    """
    실행 중인 'Idle' 상태의 인스턴스 ID를 찾아 반환합니다.
    유휴 인스턴스를 찾으면 상태를 'Busy'로 설정합니다.
    """
    print("유휴 인스턴스를 검색 중...")
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:ManagedBy', 'Values': ['Baekjoon-Code-Runner']},
                {'Name': 'tag:Status', 'Values': ['Idle']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        instances = [res['Instances'][0] for res in response['Reservations'] if res['Instances']]
        
        if not instances:
            print("유휴 인스턴스를 찾을 수 없습니다.")
            return None
        
        idle_instance_id = instances[0]['InstanceId']
        print(f"유휴 인스턴스를 찾았습니다: {idle_instance_id}")
        
        set_instance_status(idle_instance_id, "Busy")
        
        return idle_instance_id
    except ClientError as e:
        print(f"유휴 인스턴스를 찾는 중 AWS 오류 발생: {e}")
        return None
    except Exception as e:
        print(f"유휴 인스턴스를 찾는 중 예기치 않은1 오류 발생: {e}")
        return None

def list_instances():
    """이 서비스에서 관리하는 모든 인스턴스와 해당 상태를 나열합니다."""
    print("관리되는 인스턴스를 나열 중...")
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:ManagedBy', 'Values': ['Baekjoon-Code-Runner']},
                {'Name': 'instance-state-name', 'Values': ['pending', 'running', 'stopping', 'stopped']}
            ]
        )
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                instances.append({
                    "InstanceId": instance["InstanceId"],
                    "InstanceType": instance["InstanceType"],
                    "State": instance["State"]["Name"],
                    "Status": tags.get("Status", "N/A"),
                    "PublicIpAddress": instance.get("PublicIpAddress", "N/A")
                })
        print(f"{len(instances)}개의 인스턴스를 찾았습니다.")
        return instances
    except ClientError as e:
        print(f"인스턴스 나열 중 AWS 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"인스턴스 나열 중 예기치 않은 오류 발생: {e}")
        return []

def terminate_instances(instance_ids: list[str]):
    """EC2 인스턴스 목록을 종료합니다."""
    if not instance_ids:
        print("종료할 인스턴스 ID가 제공되지 않았습니다.")
        return

    print(f"인스턴스를 종료하는 중: {instance_ids}...")
    try:
        ec2_client.terminate_instances(InstanceIds=instance_ids)
        print(f"인스턴스에 대한 종료를 성공적으로 시작했습니다: {instance_ids}")
    except ClientError as e:
        print(f"인스턴스 종료 중 AWS 오류 발생: {e}")
    except Exception as e:
        print(f"인스턴스 종료 중 예기치 않은 오류 발생: {e}")