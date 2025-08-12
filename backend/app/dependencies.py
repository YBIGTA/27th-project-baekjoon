from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from database.mysql_connection import SessionLocal
from app.user.user_repository import UserRepository
from app.user.user_service import UserService


def get_db() -> Generator[Session, None, None]:
    """
    요청이 들어올 때마다 DB 세션을 열고,
    응답이 끝나면 세션을 닫는 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    FastAPI에서 사용할 UserRepository 객체를 의존성 주입으로 제공
    """
    return UserRepository(db)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    FastAPI에서 사용할 UserService 객체를 의존성 주입으로 제공
    """
    user_repo = UserRepository(db)
    return UserService(user_repo)
