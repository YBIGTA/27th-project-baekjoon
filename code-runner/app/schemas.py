from pydantic import BaseModel


class CodeRequest(BaseModel):
    language: str
    input_value: str
    code: str


class TaskResponse(BaseModel):
    task_id: str
