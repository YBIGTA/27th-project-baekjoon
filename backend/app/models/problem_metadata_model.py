from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped
from database.mysql_connection import Base


class ProblemMetadataModel(Base):
    __tablename__ = "problem_metadata"

    problem_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
