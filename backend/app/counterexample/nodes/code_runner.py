import logging
from typing import Dict, Any
from app.counterexample.state import CounterexampleState
from app.counterexample.tools.code_runner_client import CodeRunnerClient

async def run_codes_and_compare(state: CounterexampleState) -> CounterexampleState:
    """사용자 코드와 올바른 해결책을 실행하고 결과 비교"""
    user_code = state.get("user_code", "")
    correct_solution = state.get("correct_solution", "")
    test_case_generator = state.get("test_case_generator", "")
    language = state.get("language", "python")
    cancel_event = state.get("_cancel_event")

    if not user_code or not correct_solution or not test_case_generator:
        return {**state, "counterexample_found": False}

    async with CodeRunnerClient() as code_runner:

        user_outputs = []
        correct_outputs = []
        counterexample_found = False
        counterexample_input = None
        counterexample_detail = None

        for i in range(100):
            if cancel_event and cancel_event.is_set():
                logging.info("Cancellation requested: stopping code-runner loop early")
                break
            logging.info(f"Running test case {i+1}")

            input_gen_result = await code_runner.run_code(test_case_generator, language)
            if input_gen_result["error"]:
                logging.error(f"Input generation failed: {input_gen_result['error']}")
                return {**state, "counterexample_found": False}
            test_input = input_gen_result.get("output", "")
            logging.info(f"Test input: {test_input}")

            try:
                # 사용자 코드 실행
                user_result = await code_runner.run_code(user_code, test_input, language)
                user_output = user_result.get("output", "").strip()
                user_outputs.append(user_output)
                
                # 올바른 해결책 실행
                correct_result = await code_runner.run_code(correct_solution, test_input, language)
                correct_output = correct_result.get("output", "").strip()
                correct_outputs.append(correct_output)
                
                # 출력 비교
                if user_output != correct_output:
                    counterexample_found = True
                    counterexample_input = test_input
                    counterexample_detail = {
                        "test_case_index": i,
                        "input": test_input,
                        "user_output": user_output,
                        "correct_output": correct_output,
                        "description": f"테스트케이스 {i+1}"
                    }
                    break
                    
            except Exception as e:
                # 실행 오류가 발생한 경우도 반례로 간주
                counterexample_found = True
                counterexample_input = test_input
                counterexample_detail = {
                    "test_case_index": i,
                    "input": test_input,
                    "error": str(e),
                    "description": f"테스트케이스 {i+1}"
                }
                break
        
        return {
            **state,
            "user_outputs": user_outputs,
            "correct_outputs": correct_outputs,
            "counterexample_found": counterexample_found,
            "counterexample_input": counterexample_input,
            "counterexample_detail": counterexample_detail
        }

async def execute_single_code(code: str, test_input: str, language: str) -> Dict[str, Any]:
    """단일 코드 실행"""
    async with CodeRunnerClient() as code_runner:
        try:
            result = await code_runner.run_code(code, test_input, language)
            return {
                "success": True,
                "output": result.get("output", ""),
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }