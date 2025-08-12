from fastapi import APIRouter, Depends, status
from app.api.api_schema import SolveRequest, SolveResponse
from app.api.api_service import AISolveService
from app.dependencies import get_solve_service


solve_router = APIRouter(prefix="/api")


@solve_router.post(
    "/solve",
    response_model=SolveResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate solution code for a PS problem",
)
def solve(req: SolveRequest, service: AISolveService = Depends(get_solve_service)) -> SolveResponse:
    return service.solve(req)
