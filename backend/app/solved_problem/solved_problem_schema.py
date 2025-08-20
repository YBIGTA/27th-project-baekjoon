from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ProblemStatusEnum(str, Enum):
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"


class SolvedProblemCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    solution_code: str = Field(..., description="해결 코드")
    language: str = Field(default="python", description="프로그래밍 언어")
    execution_time_ms: Optional[int] = Field(None, description="실행 시간 (밀리초)")
    memory_usage_mb: Optional[float] = Field(None, description="메모리 사용량 (MB)")
    status: ProblemStatusEnum = Field(..., description="제출 결과 상태")


class SolvedProblemResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    solution_code: str
    language: str
    execution_time_ms: Optional[int]
    memory_usage_mb: Optional[float]
    status: ProblemStatusEnum
    submitted_at: datetime

    class Config:
        from_attributes = True


class ProblemMetadataCreate(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    title: str = Field(..., description="문제 제목")
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
