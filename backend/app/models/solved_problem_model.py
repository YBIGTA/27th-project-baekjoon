from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.mysql_connection import Base


class SolvedProblemModel(Base):
    __tablename__ = "solved_problems"

    problem_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    solution_code: Mapped[str] = mapped_column(Text, nullable=False)
    input_generator: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
