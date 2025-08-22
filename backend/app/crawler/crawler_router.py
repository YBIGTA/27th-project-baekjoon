from fastapi import APIRouter, HTTPException, status, Depends

from app.responses.base_response import BaseResponse
from .acmicpc_crawler import AcmicpcCrawler
from .crawler_schema import ProblemData, FullProblemInfo
from app.dependencies import get_crawler

router = APIRouter(prefix="/api/crawler", tags=["Crawler"])


@router.get(
    "/problem/{problem_id}",
    response_model=BaseResponse[FullProblemInfo],
    status_code=status.HTTP_200_OK,
    summary="백준 문제 정보 크롤링",
)
async def get_problem_data(
    problem_id: int,
    crawler_instance: AcmicpcCrawler = Depends(get_crawler),
) -> BaseResponse[FullProblemInfo]:
    """문제 번호를 받아 백준 사이트에서 문제 정보를 크롤링합니다."""
    problem_data = await crawler_instance.fetch_full_problem(problem_id)

    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found or could not be crawled.",
        )

    return BaseResponse(status="success", data=problem_data)