from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.solved_problem.solved_problem_repository import SolvedProblemRepository
from app.solved_problem.solved_problem_schema import (
    SolvedProblemCreate, 
    SolvedProblemResponse, 
    ProblemMetadataCreate,
    ProblemMetadataResponse
)


class SolvedProblemService:
    def __init__(self, repository: SolvedProblemRepository):
        self.repository = repository

    def save_solved_problem(self, solved_problem: SolvedProblemCreate) -> SolvedProblemResponse:
        existing_solution = self.repository.get_problem_solution(solved_problem.problem_id)
        
        if existing_solution:
            updated_solution = self.repository.update_solved_problem(solved_problem.problem_id, solved_problem)
            return SolvedProblemResponse.model_validate(updated_solution)
        else:
            new_solution = self.repository.create_solved_problem(solved_problem)
            return SolvedProblemResponse.model_validate(new_solution)

    def get_problem_solution(self, problem_id: int) -> Optional[SolvedProblemResponse]:
        solution = self.repository.get_problem_solution(problem_id)
        if solution:
            return SolvedProblemResponse.model_validate(solution)
        return None

    def delete_solved_problem(self, problem_id: int) -> bool:
        return self.repository.delete_solved_problem(problem_id)

    def save_problem_metadata(self, problem_metadata: ProblemMetadataCreate) -> ProblemMetadataResponse:
        metadata = self.repository.create_problem_metadata(problem_metadata)
        return ProblemMetadataResponse.model_validate(metadata)

    def get_problem_metadata(self, problem_id: int) -> Optional[ProblemMetadataResponse]:
        metadata = self.repository.get_problem_metadata(problem_id)
        if metadata:
            return ProblemMetadataResponse.model_validate(metadata)
        return None

    def update_problem_metadata(self, problem_id: int, problem_metadata: ProblemMetadataCreate) -> Optional[ProblemMetadataResponse]:
        metadata = self.repository.update_problem_metadata(problem_id, problem_metadata)
        if metadata:
            return ProblemMetadataResponse.model_validate(metadata)
        return None
