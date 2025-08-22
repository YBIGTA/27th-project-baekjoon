from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolvedProblemCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    solution_code: str = Field(..., description="해결 코드")
    input_generator: Optional[str] = Field(None, description="입력 생성기")


class SolvedProblemResponse(BaseModel):
    problem_id: int
    solution_code: str
    input_generator: Optional[str]
    submitted_at: datetime

    class Config:
        from_attributes = True


class ProblemMetadataCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    title: str = Field(..., description="문제 제목")
    description: str = Field(..., description="문제 설명")
    difficulty: Optional[int] = Field(None, description="난이도")
    category: Optional[str] = Field(None, description="문제 카테고리")


class ProblemMetadataResponse(BaseModel):
    problem_id: int
    title: str
    difficulty: Optional[int]
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
