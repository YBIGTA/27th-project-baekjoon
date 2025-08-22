from typing import Dict, Any, Literal, Optional, Union
from pydantic import BaseModel
from app.counterexample.graph import build_counterexample_graph, build_counterexample_graph_from_compare
from app.counterexample.state import CounterexampleState


class CounterexampleSuccess(BaseModel):
    """반례 찾기 성공 결과"""
    success: Literal[True] = True
    counterexample_found: bool
    counterexample_input: Optional[str] = None
    counterexample_detail: Optional[str] = None
    test_cases_count: int = 0
    correct_solution: str
    input_generator: str


class CounterexampleError(BaseModel):
    """반례 찾기 실패 결과"""
    success: Literal[False] = False
    error: str
    counterexample_found: Literal[False] = False


CounterexampleResult = Union[CounterexampleSuccess, CounterexampleError]

class CounterexampleRunner:
    """반례 찾기 워크플로우 실행기"""
    
    def __init__(self):
        self._graph_from_solve = build_counterexample_graph()
        self._graph_from_compare = build_counterexample_graph_from_compare()
    
    def _get_graph(self, start_from_compare: bool = False):
        if start_from_compare:
            return self._graph_from_compare
        else:
            return self._graph_from_solve
    
    async def _execute_workflow(self, initial_state: CounterexampleState, start_from_compare: bool = False) -> CounterexampleResult:
        """워크플로우 실행 공통 로직"""
        try:
            graph = self._get_graph(start_from_compare)
            result = await graph.ainvoke(initial_state)

            correct_solution = result.get("correct_solution")
            input_generator = result.get("test_case_generator")
            if not correct_solution or not input_generator:
                raise ValueError("Correct solution or input generator is missing")
            
            return CounterexampleSuccess(
                counterexample_found=result.get("counterexample_found", False),
                counterexample_input=result.get("counterexample_input"),
                counterexample_detail=None,
                test_cases_count=len(result.get("test_cases", [])),
                correct_solution=correct_solution,
                input_generator=input_generator
            )
        except Exception as e:
            return CounterexampleError(
                error=str(e)
            )
    
    async def find_counterexample(
        self, 
        problem_description: str, 
        user_code: str, 
        language: str = "python",
        difficulty: int = 0,
        correct_solution: Optional[str] = None,
        input_generator: Optional[str] = None,
        start_from_compare: bool = False,
    ) -> CounterexampleResult:
        """
        사용자 코드에서 반례를 찾는 메인 함수
        
        Args:
            problem_description: 문제 설명
            user_code: 사용자가 제출한 코드
            language: 프로그래밍 언어 (기본값: python)
            difficulty: 문제 난이도
            correct_solution: 정답 코드 (선택사항)
            input_generator: 입력 생성기 (선택사항)
            start_from_compare: True이면 run_and_compare 노드부터 시작, False이면 solve 노드부터 시작
            
        Returns:
            반례 찾기 결과
        """
        initial_state: CounterexampleState = {
            "problem_description": problem_description,
            "user_code": user_code,
            "language": language,
            "counterexample_found": False,
            "difficulty": difficulty,
        }
        
        # 선택사항 매개변수 추가
        if correct_solution is not None:
            initial_state["correct_solution"] = correct_solution
        if input_generator is not None:
            initial_state["test_case_generator"] = input_generator
        
        return await self._execute_workflow(initial_state, start_from_compare)

# 글로벌 인스턴스
runner = CounterexampleRunner()