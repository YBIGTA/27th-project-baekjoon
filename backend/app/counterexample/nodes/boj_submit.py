import logging
from app.counterexample.state import CounterexampleState
from app.counterexample.tools.acmicpc_client import AcmicpcClient

async def boj_submit(state: CounterexampleState) -> CounterexampleState:
    """백준 결과를 통해 올바른 해결책 검증"""
    problem_id = state.get("problem_id", 1000)
    correct_solution = state.get("correct_solution", "")
    language = state.get("language", "python")
    
    async with AcmicpcClient() as client:
        submit_result = await client.submit_code(problem_id, correct_solution, language)

        if submit_result["error"] or submit_result["status"] != "Accepted":
            return {
                **state, 
                "is_solution_validated": False, 
                "solution_generate_try": state.get("solution_generate_try", 0) + 1,
            }

        return {
            **state,
            "is_solution_validated": True,
            "solution_generate_try": state.get("solution_generate_try", 0) + 1
        }
