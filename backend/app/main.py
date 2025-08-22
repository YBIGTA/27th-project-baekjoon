from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.user.user_router import router as user_router
from app.solved_problem.solved_problem_router import router as solved_problem_router
import httpx

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(solved_problem_router)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/execute-code")
async def execute_code(request: dict):
    """
    code-runner 서비스를 통해 코드를 실행합니다.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://code-runner:8000/run-code",
                json=request,
                timeout=30.0
            )
            return response.json()
    except Exception as e:
        return {
            "output": f"코드 실행 중 오류가 발생했습니다: {str(e)}",
            "executionTime": 0,
            "memoryUsage": 0,
            "status": "runtime_error"
        }