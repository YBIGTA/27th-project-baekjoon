from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.solved_problem.solved_problem_service import SolvedProblemService
from app.solved_problem.solved_problem_schema import (
    SolvedProblemCreate,
    SolvedProblemResponse,
    ProblemMetadataCreate,
    ProblemMetadataResponse
)
from app.user.user_schema import UserResponse

router = APIRouter(prefix="/solved-problems", tags=["solved-problems"])


@router.post("/", response_model=SolvedProblemResponse)
def save_solved_problem(
    solved_problem: SolvedProblemCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    return service.save_solved_problem(current_user.id, solved_problem)


@router.get("/", response_model=List[SolvedProblemResponse])
def get_user_solved_problems(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    return service.get_user_solved_problems(current_user.id, skip, limit)


@router.get("/{problem_id}", response_model=SolvedProblemResponse)
def get_user_problem_solution(
    problem_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    solution = service.get_user_problem_solution(current_user.id, problem_id)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 문제의 해결 기록을 찾을 수 없습니다."
        )
    return solution


@router.delete("/{problem_id}")
def delete_solved_problem(
    problem_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    success = service.delete_solved_problem(current_user.id, problem_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 문제의 해결 기록을 찾을 수 없습니다."
        )
    return {"message": "해결 기록이 삭제되었습니다."}


@router.get("/stats/summary")
def get_user_stats(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    return service.get_user_stats(current_user.id)


@router.post("/metadata", response_model=ProblemMetadataResponse)
def save_problem_metadata(
    problem_metadata: ProblemMetadataCreate,
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    return service.save_problem_metadata(problem_metadata)


@router.get("/metadata/{problem_id}", response_model=ProblemMetadataResponse)
def get_problem_metadata(
    problem_id: int,
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    metadata = service.get_problem_metadata(problem_id)
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 문제의 메타데이터를 찾을 수 없습니다."
        )
    return metadata


@router.put("/metadata/{problem_id}", response_model=ProblemMetadataResponse)
def update_problem_metadata(
    problem_id: int,
    problem_metadata: ProblemMetadataCreate,
    db: Session = Depends(get_db)
):
    service = SolvedProblemService(db)
    metadata = service.update_problem_metadata(problem_id, problem_metadata)
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 문제의 메타데이터를 찾을 수 없습니다."
        )
    return metadata
