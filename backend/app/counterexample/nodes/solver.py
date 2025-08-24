import logging
from langchain_core.output_parsers import StrOutputParser
from app.counterexample.state import CounterexampleState
from app.counterexample.prompts.solver import SOLVE_PROMPT
from app.counterexample.tools.chat_client import get_counterexample_chat
from app.counterexample.utils.markdown import extract_code_block

async def generate_solution(state: CounterexampleState) -> CounterexampleState:
    """주어진 문제에 대한 올바른 해결 코드를 생성"""
    problem = state.get("problem_description", "")
    language = state.get("language", "python")
    difficulty = state.get("difficulty", 0)
    try_count = state.get("solution_generate_try", 0)

    if not problem:
        return {**state, "correct_solution": ""}
    
    # LLM을 사용해서 올바른 해결책 생성 시도
    try:
        chat = get_counterexample_chat(difficulty + 2 * try_count)
        chain = SOLVE_PROMPT | chat | StrOutputParser()
        response = await chain.ainvoke({
            "problem_description": problem,
            "language": language,
        })
        code = extract_code_block(response)

        logging.info(f"LLM solver Response: {response}")

        if not code:
            raise ValueError("Code block not found.")
        
        return {**state, "correct_solution": code}
    except Exception:
        return {**state, "correct_solution": ""}