from typing import Optional, Literal
from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    """Request body for asking the AI solver to generate code."""
    problem: str = Field(..., description="Problem description or prompt text.")
    language: Literal["python", "cpp", "java", "js"] = Field(
        "python", description="Target programming language for the solution."
    )
    time_limit_ms: Optional[int] = Field(
        None, description="Optional time limit hint in milliseconds."
    )
    memory_limit_mb: Optional[int] = Field(
        None, description="Optional memory limit hint in megabytes."
    )


class SolveResponse(BaseModel):
    """Response body containing the generated solution code."""
    code: str
    language: str
    message: Optional[str] = None

