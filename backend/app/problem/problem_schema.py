from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolvedProblemCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    solution_code: str = Field(..., description="해결 코드")
    input_generator: str = Field(..., description="입력 생성기")


class SolvedProblemResponse(BaseModel):
    problem_id: int
    solution_code: str
    input_generator: Optional[str]
    submitted_at: datetime

    class Config:
        from_attributes = True


class CalcCounterExampleRequest(BaseModel):
    user_code: str = Field(..., description="유저 코드")
    user_code_language: str = Field(..., description="유저 코드 언어")


class CalcCounterExampleResponse(BaseModel):
    counter_example_input: str = Field(..., description="반례")


class ProblemMetadataCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    title: str = Field(..., description="문제 제목")
    description: str = Field(..., description="문제 설명")
    difficulty: int = Field(..., description="난이도")
    category: str = Field(..., description="문제 카테고리")


class ProblemMetadataResponse(BaseModel):
    problem_id: int
    title: str
    description: str
    difficulty: int
    category: str
    created_at: datetime

    class Config:
        from_attributes = True
