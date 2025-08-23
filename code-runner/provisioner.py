import argparse
from app import ec2_manager

def main():
    parser = argparse.ArgumentParser(description="Code Runner EC2 인스턴스 프로비저너")
    parser.add_argument("count", type=int, help="프로비저닝할 인스턴스 수")
    args = parser.parse_args()

    print(f"{args.count}개의 EC2 인스턴스를 프로비저닝합니다...")
    instance_ids = ec2_manager.provision_instances(args.count)

    if instance_ids:
        print(f"프로비저닝에 성공했습니다. 인스턴스 ID: {instance_ids}")
    else:
        print("프로비저닝에 실패했습니다.")

if __name__ == "__main__":
    main()
