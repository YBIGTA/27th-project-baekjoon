from typing import TypedDict, Optional, List

class CounterexampleState(TypedDict, total=False):
    # 입력
    problem_description: str  # 주어진 문제
    user_code: str           # 사용자가 제출한 코드
    language: str
    
    # AI가 생성한 올바른 해결책
    correct_solution: str
    
    # 테스트케이스
    test_case_generator: str
    
    # 실행 결과 비교
    user_outputs: List[str]
    correct_outputs: List[str]
    
    # 최종 반례
    counterexample_found: bool
    counterexample_input: Optional[str]
    counterexample_detail: Optional[dict]