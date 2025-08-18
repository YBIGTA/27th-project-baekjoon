from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.mysql_connection import Base


class UserModel(Base):
    """
    SQLAlchemy ORM 모델 - users 테이블과 매핑
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    username = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
