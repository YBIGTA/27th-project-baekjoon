from pydantic import BaseModel, Field
from typing import List


class ProblemData(BaseModel):
    problem_id: int = Field(..., description="문제 번호")
    title: str = Field(..., description="문제 제목")
    description: str = Field(..., description="문제 설명 HTML")
    constraints: str = Field(..., description="제한사항 HTML")
    input_description: str = Field(..., description="입력 설명 HTML")
    output_description: str = Field(..., description="출력 설명 HTML")
    tags: List[str] = Field([], description="문제 태그")


