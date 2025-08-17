import os
from dotenv import load_dotenv

load_dotenv()

PORT = 8080 
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY", '')