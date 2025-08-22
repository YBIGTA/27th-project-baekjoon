from pydantic import BaseModel


class CodeRequest(BaseModel):
    language: str
    code: str


class TaskResponse(BaseModel):
    task_id: str
