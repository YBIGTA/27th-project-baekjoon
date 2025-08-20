from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.mysql_connection import Base
import enum


class ProblemStatus(enum.Enum):
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"


class SolvedProblemModel(Base):
    __tablename__ = "solved_problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    solution_code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False, default="python")
    execution_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    memory_usage_mb: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[ProblemStatus] = mapped_column(Enum(ProblemStatus), nullable=False)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("UserModel", back_populates="solved_problems")
