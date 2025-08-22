from typing import Optional
from bs4 import BeautifulSoup
from app.problem.problem_repository import SolvedProblemRepository
from app.problem.problem_schema import (
    CalcCounterExampleResponse,
    ProblemMetadataCreate,
    ProblemMetadataResponse,
    SolvedProblemCreate
)
from app.crawler.crawler_schema import FullProblemInfo
from app.crawler.acmicpc_crawler import AcmicpcCrawler
from app.counterexample.runner import CounterexampleRunner, CounterexampleSuccess


class SolvedProblemService:
    def __init__(self, 
                 repository: SolvedProblemRepository, 
                 crawler: AcmicpcCrawler,
                 counterexample_runner: CounterexampleRunner):
        self.repository = repository
        self.crawler = crawler
        self.counterexample_runner = counterexample_runner

    async def calc_counter_example(self, problem_id: int, user_code: str, user_code_language: str) -> CalcCounterExampleResponse:
        metadata = await self.get_problem_metadata(problem_id)
        solution = self.repository.get_problem_solution(problem_id)
        counter_example = await self.counterexample_runner.find_counterexample(
            metadata.description,
            user_code, 
            user_code_language,
            metadata.difficulty,
            solution.solution_code if solution else None,
            solution.input_generator if solution else None,
            True if solution else False
        )
        if not isinstance(counter_example, CounterexampleSuccess):
            raise ValueError("Failed to find counterexample")
        if not solution:
            solved_problem = SolvedProblemCreate(
                problem_id=problem_id,
                solution_code=counter_example.correct_solution,
                input_generator=counter_example.input_generator
            )
            self.repository.create_solved_problem(solved_problem)
        if not counter_example.counterexample_input:
            raise ValueError("Counterexample input is missing")
        return CalcCounterExampleResponse(
            counter_example_input=counter_example.counterexample_input,
        )

    async def get_problem_metadata(self, problem_id: int) -> ProblemMetadataResponse:
        metadata = self.repository.get_problem_metadata(problem_id)
        if not metadata:
            data = await self.crawler.fetch_full_problem(problem_id)
            if not data:
                raise ValueError("Failed to fetch problem metadata")
            
            category = ','.join(
                tag.displayNames[0].name
                for tag in data.tags
                if tag.displayNames and len(tag.displayNames) > 0
            )
            problem_metadata = ProblemMetadataCreate(
                problem_id=problem_id,
                title=data.title,
                description=self._get_problem_markdown(data),
                category=category,
                difficulty=data.level
            )
            metadata = self.repository.create_problem_metadata(problem_metadata)
        return ProblemMetadataResponse.model_validate(metadata)

    @staticmethod
    def _get_problem_markdown(problem_info: FullProblemInfo):
        # HTML 태그 제거를 위한 헬퍼 함수
        def clean_html(text: str) -> str:
            if not text:
                return ""
            soup = BeautifulSoup(text, 'html.parser')
            return soup.get_text().strip()

        title = clean_html(problem_info.title)
        description = clean_html(problem_info.description)
        input_description = clean_html(problem_info.input_description)
        output_description = clean_html(problem_info.output_description)
        constraints = clean_html(problem_info.constraints)

        result = (
            f"# {title}\n\n"
            f"## 문제 \n\n{description}\n\n"
            f"## 입력\n\n{input_description}\n\n"
            f"## 출력\n\n{output_description}\n\n"
        )
        
        if constraints:
            result += f"## 제약조건\n\n{constraints}\n"
            
        return result