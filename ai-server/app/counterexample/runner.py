from typing import Dict, Any
from app.counterexample.graph import build_counterexample_graph
from app.counterexample.state import CounterexampleState

class CounterexampleRunner:
    """반례 찾기 워크플로우 실행기"""
    
    def __init__(self):
        self.graph = build_counterexample_graph()
    
    async def find_counterexample(
        self, 
        problem_description: str, 
        user_code: str, 
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        사용자 코드에서 반례를 찾는 메인 함수
        
        Args:
            problem_description: 문제 설명
            user_code: 사용자가 제출한 코드
            language: 프로그래밍 언어 (기본값: python)
            
        Returns:
            반례 찾기 결과
        """
        initial_state: CounterexampleState = {
            "problem_description": problem_description,
            "user_code": user_code,
            "language": language,
            "counterexample_found": False
        }
        
        try:
            result = await self.graph.ainvoke(initial_state)

            return {
                "success": True,
                "counterexample_found": result.get("counterexample_found", False),
                "counterexample_input": result.get("counterexample_input"),
                "counterexample_detail": result.get("counterexample_detail"),
                "test_cases_count": len(result.get("test_cases", [])),
                "correct_solution": result.get("correct_solution")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "counterexample_found": False
            }

# 글로벌 인스턴스
runner = CounterexampleRunner()