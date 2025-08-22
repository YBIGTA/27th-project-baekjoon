import os
import boto3
from dotenv import load_dotenv
from pathlib import Path
from celery import Celery

PORT = 8001

# 프로젝트 내부 경로를 다음과 같이 만듭니다: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 프로젝트 루트에서 .env 파일 로드
dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)

# --- AWS 설정
AWS_REGION = os.environ.get("AWS_REGION", "ap-northeast-2")

# --- EC2 인스턴스 사양
EC2_AMI_ID = os.environ.get("EC2_AMI_ID")
EC2_INSTANCE_TYPE = os.environ.get("EC2_INSTANCE_TYPE", "t2.micro")

# --- EC2 네트워킹 및 IAM
EC2_SECURITY_GROUP_ID = os.environ.get("EC2_SECURITY_GROUP_ID")
EC2_IAM_INSTANCE_PROFILE_ARN = os.environ.get("EC2_IAM_INSTANCE_PROFILE_ARN")

# --- Celery 설정
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

# --- Worker 설정
REMOTE_EXECUTOR_PATH = os.environ.get("REMOTE_EXECUTOR_PATH", "/home/ec2-user/remote_executor.py")
IDLE_INSTANCE_WAIT_TIMEOUT = int(os.environ.get("IDLE_INSTANCE_WAIT_TIMEOUT", "120"))
IDLE_INSTANCE_POLL_INTERVAL = int(os.environ.get("IDLE_INSTANCE_POLL_INTERVAL", "5"))

# --- 필수 변수가 설정되었는지 확인
_required_vars = [EC2_AMI_ID, EC2_SECURITY_GROUP_ID, EC2_IAM_INSTANCE_PROFILE_ARN]
if not all(_required_vars):
    raise ValueError(
        "하나 이상의 필수 환경 변수가 설정되지 않았습니다. "
        ".env.example에서 .env 파일을 생성하고 다음 값들을 채워주세요: "
        "EC2_AMI_ID, EC2_SECURITY_GROUP_ID, EC2_IAM_INSTANCE_PROFILE_ARN"
    )

# --- AWS 클라이언트 (중앙 관리)
boto3_session = boto3.Session(region_name=AWS_REGION)
ec2_client = boto3_session.client("ec2")
ssm_client = boto3_session.client("ssm")

# --- Celery 앱 (중앙 관리)
celery_app = Celery(
    "code_runner_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.worker'] # include에 워커 모듈 추가
)