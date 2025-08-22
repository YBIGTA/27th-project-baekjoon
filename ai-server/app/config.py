import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

PORT = 8080
UPSTAGE_API_KEY = SecretStr(os.getenv("UPSTAGE_API_KEY", ''))
OPENAI_API_KEY = SecretStr(os.getenv("OPENAI_API_KEY", ''))
CODE_RUNNER_URL = os.getenv("CODE_RUNNER_URL", "http://code-runner:8000")