from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from database.mysql_connection import SessionLocal
from app.user.user_repository import UserRepository
from app.user.user_service import UserService
from app.solved_problem.solved_problem_service import SolvedProblemService
from app.solved_problem.solved_problem_repository import SolvedProblemRepository
from app.crawler.acmicpc_crawler import AcmicpcCrawler
from app.user.user_schema import UserDB
from app.auth import get_current_user_email


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


def get_crawler() -> AcmicpcCrawler:
    return AcmicpcCrawler()


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


def get_solved_problem_repository(db: Session = Depends(get_db)) -> SolvedProblemRepository:
    """
    FastAPI에서 사용할 SolvedProblemRepository 객체를 의존성 주입으로 제공
    """
    return SolvedProblemRepository(db)


def get_solved_problem_service(
    repo: SolvedProblemRepository = Depends(get_solved_problem_repository),
    crawler: AcmicpcCrawler = Depends(get_crawler)
) -> SolvedProblemService:
    """
    FastAPI에서 사용할 SolvedProblemService 객체를 의존성 주입으로 제공
    """
    return SolvedProblemService(repo, crawler)


def get_current_user(
    current_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
) -> UserDB:
    """JWT 토큰의 이메일로 현재 사용자 정보를 조회하여 반환합니다."""
    repo = UserRepository(db)
    user_db = repo.get_user_by_email(current_email)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db

