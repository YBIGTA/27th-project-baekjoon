from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.solved_problem_model import SolvedProblemModel
from app.models.problem_metadata_model import ProblemMetadataModel
from app.solved_problem.solved_problem_schema import SolvedProblemCreate, ProblemMetadataCreate


class SolvedProblemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_solved_problem(self, user_id: int, solved_problem: SolvedProblemCreate) -> SolvedProblemModel:
        db_solved_problem = SolvedProblemModel(
            user_id=user_id,
            problem_id=solved_problem.problem_id,
            solution_code=solved_problem.solution_code,
            counter_example=solved_problem.counter_example
        )
        self.db.add(db_solved_problem)
        self.db.commit()
        self.db.refresh(db_solved_problem)
        return db_solved_problem

    def get_user_solved_problems(self, user_id: int, skip: int = 0, limit: int = 100) -> List[SolvedProblemModel]:
        return self.db.query(SolvedProblemModel).filter(
            SolvedProblemModel.user_id == user_id
        ).offset(skip).limit(limit).all()

    def get_user_problem_solution(self, user_id: int, problem_id: int) -> Optional[SolvedProblemModel]:
        return self.db.query(SolvedProblemModel).filter(
            and_(
                SolvedProblemModel.user_id == user_id,
                SolvedProblemModel.problem_id == problem_id
            )
        ).first()

    def update_solved_problem(self, user_id: int, problem_id: int, solved_problem: SolvedProblemCreate) -> Optional[SolvedProblemModel]:
        db_solved_problem = self.get_user_problem_solution(user_id, problem_id)
        if not db_solved_problem:
            return None

        db_solved_problem.solution_code = solved_problem.solution_code
        db_solved_problem.counter_example = solved_problem.counter_example

        self.db.commit()
        self.db.refresh(db_solved_problem)
        return db_solved_problem

    def delete_solved_problem(self, user_id: int, problem_id: int) -> bool:
        db_solved_problem = self.get_user_problem_solution(user_id, problem_id)
        if not db_solved_problem:
            return False

        self.db.delete(db_solved_problem)
        self.db.commit()
        return True

    def create_problem_metadata(self, problem_metadata: ProblemMetadataCreate) -> ProblemMetadataModel:
        db_problem_metadata = ProblemMetadataModel(
            problem_id=problem_metadata.problem_id,
            title=problem_metadata.title,
            difficulty=problem_metadata.difficulty,
            category=problem_metadata.category
        )
        self.db.add(db_problem_metadata)
        self.db.commit()
        self.db.refresh(db_problem_metadata)
        return db_problem_metadata

    def get_problem_metadata(self, problem_id: int) -> Optional[ProblemMetadataModel]:
        return self.db.query(ProblemMetadataModel).filter(
            ProblemMetadataModel.problem_id == problem_id
        ).first()

    def update_problem_metadata(self, problem_id: int, problem_metadata: ProblemMetadataCreate) -> Optional[ProblemMetadataModel]:
        db_problem_metadata = self.get_problem_metadata(problem_id)
        if not db_problem_metadata:
            return None

        db_problem_metadata.title = problem_metadata.title
        db_problem_metadata.difficulty = problem_metadata.difficulty
        db_problem_metadata.category = problem_metadata.category

        self.db.commit()
        self.db.refresh(db_problem_metadata)
        return db_problem_metadata
