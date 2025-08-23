import logging
from langchain_core.output_parsers import StrOutputParser
from app.counterexample.state import CounterexampleState
from app.counterexample.prompts.input_gen import INPUT_GEN_PROMPT
from app.counterexample.tools.chat_client import get_counterexample_chat
from app.counterexample.utils.markdown import extract_code_block

async def generate_test_cases(state: CounterexampleState) -> CounterexampleState:
    """문제에 맞는 다양한 테스트케이스 생성"""
    problem = state.get("problem_description", "")
    language = state.get("language", "python")
    
    try:
        chat = get_counterexample_chat()
        chain = INPUT_GEN_PROMPT | chat | StrOutputParser()
        response = await chain.ainvoke({
            "problem_description": problem,
            "language": language,
        })
        code = extract_code_block(response)
        if not code:
            raise ValueError("Code block not found.")
        
        logging.info(f"LLM input generator Response: {response}")

        return {**state, "test_case_generator": code}
    except Exception:
        return {**state, "test_case_generator": ""}


