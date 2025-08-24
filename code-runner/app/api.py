from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from .worker import celery_app, run_code_task
from .schemas import CodeRequest, TaskResponse

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/run-code", response_model=TaskResponse)
async def submit_code(req: CodeRequest):
    """코드를 실행 요청을 받아 Celery 작업 큐에 넣고 작업 ID를 반환합니다."""
    task = run_code_task.delay(req.language, req.code, req.input_value)
    return {"task_id": task.id}


@app.get("/results/{task_id}")
async def get_result(task_id: str):
    """작업 ID를 사용하여 코드 실행 결과를 조회합니다."""
    task_result = AsyncResult(task_id, app=celery_app)

    if not task_result.ready():
        # 작업이 아직 완료되지 않았을 경우
        return {"status": task_result.status, "result": None}

    if task_result.failed():
        # 작업이 실패했을 경우
        raise HTTPException(status_code=500, detail=str(task_result.info))

    # 작업이 성공적으로 완료되었을 경우
    result = task_result.get()
    return {"status": task_result.status, "result": result}
