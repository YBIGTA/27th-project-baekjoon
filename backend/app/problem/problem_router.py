from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_solved_problem_service, get_current_user
from app.problem.problem_service import SolvedProblemService
from app.problem.problem_schema import (
    SolvedProblemCreate,
    CalcCounterExampleRequest,
    CalcCounterExampleResponse,
    ProblemMetadataCreate,
    ProblemMetadataResponse
)
from app.user.user_schema import UserDB

router = APIRouter(prefix="/problem", tags=["problem"])


@router.post("/{problem_id}/calc_counter_example", response_model=CalcCounterExampleResponse)
async def get_user_problem_solution(
    problem_id: int,
    request: CalcCounterExampleRequest,
    current_user: UserDB = Depends(get_current_user),
    service: SolvedProblemService = Depends(get_solved_problem_service)
):
    solution = await service.calc_counter_example(problem_id, 
                                            request.user_code, 
                                            request.user_code_language)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 문제의 해결 기록을 찾을 수 없습니다."
        )
    return solution


@router.get("/{problem_id}", response_model=ProblemMetadataResponse)
async def get_problem_metadata(
    problem_id: int,
    service: SolvedProblemService = Depends(get_solved_problem_service)
):
    try:
        metadata = await service.get_problem_metadata(problem_id)
        return metadata
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문제 메타데이터를 가져오는 중 오류가 발생했습니다: " + str(e)
        )

