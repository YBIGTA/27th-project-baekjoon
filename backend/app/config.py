import os
from dotenv import load_dotenv
from pydantic import SecretStr

# .env 파일 로드
load_dotenv()

# Server
PORT = 8000

# JWT/Auth
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PROD")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or "60")

# AI
UPSTAGE_API_KEY = SecretStr(os.getenv("UPSTAGE_API_KEY", ''))
OPENAI_API_KEY = SecretStr(os.getenv("OPENAI_API_KEY", ''))
CODE_RUNNER_URL = os.getenv("CODE_RUNNER_URL", "http://code-runner:8000")