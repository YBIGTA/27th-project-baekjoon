from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.mysql_connection import Base


class SolvedProblemModel(Base):
    __tablename__ = "solved_problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    solution_code: Mapped[str] = mapped_column(Text, nullable=False)
    counter_example: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="submissions")
