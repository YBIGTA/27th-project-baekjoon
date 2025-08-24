from langgraph.graph import StateGraph, END
from app.counterexample.state import CounterexampleState
from app.counterexample.nodes.solver import generate_solution
from app.counterexample.nodes.input_gen import generate_test_cases
from app.counterexample.nodes.code_runner import run_codes_and_compare
from app.counterexample.nodes.boj_submit import boj_submit

def should_continue(state: CounterexampleState) -> str:
    """반례를 찾았는지 확인하여 다음 단계 결정"""
    if state.get("counterexample_found", False):
        return "end"
    
    return "continue"

def should_have_solution(state: CounterexampleState) -> str:
    """solve 이후 올바른 해결책이 생성되었는지 확인하여 다음 단계 결정"""
    return "ok" if state.get("correct_solution") else "retry"

def should_solution_validated(state: CounterexampleState) -> str:
    return "ok" if state.get("is_solution_validated") else "retry"

def should_have_inputs(state: CounterexampleState) -> str:
    """generate_inputs 이후 테스트케이스 생성기가 있는지 확인하여 다음 단계 결정"""
    return "ok" if state.get("test_case_generator") else "retry"

def _build_base_graph(entry_point: str = "solve"):
    """기본 그래프 구조를 생성하는 공통 함수"""
    # StateGraph 생성
    graph = StateGraph(CounterexampleState)
    
    # 노드 추가
    graph.add_node("solve", generate_solution)
    graph.add_node("boj_submit", boj_submit)
    graph.add_node("generate_inputs", generate_test_cases)
    graph.add_node("run_and_compare", run_codes_and_compare)
    
    # 시작점 설정
    graph.set_entry_point(entry_point)
    
    # solve 이후 correct_solution이 없으면 다시 solve로 돌아가 재시도
    graph.add_conditional_edges(
        "solve",
        should_have_solution,
        {
            "ok": "boj_submit",
            "retry": "solve",
        },
    )
    # 백준 제출 후 올바른 해결책이 검증되지 않으면 다시 solve로 돌아가 재시도
    graph.add_conditional_edges(
        "boj_submit",
        should_solution_validated,
        {
            "ok": "generate_inputs",
            "retry": "solve",
        },
    )
    # generate_inputs 이후 test_case_generator가 없으면 다시 generate_inputs로 돌아가 재시도
    graph.add_conditional_edges(
        "generate_inputs",
        should_have_inputs,
        {
            "ok": "run_and_compare",
            "retry": "generate_inputs",
        },
    )
    
    # 조건부 엣지: 반례를 찾았으면 종료, 아니면 더 테스트케이스 생성
    graph.add_conditional_edges(
        "run_and_compare",
        should_continue,
        {
            "end": END,
            "continue": "generate_inputs"
        }
    )
    
    return graph.compile()

def build_counterexample_graph():
    """반례 찾기 워크플로우 그래프 구성 (solve 노드부터 시작)"""
    return _build_base_graph("solve")

def build_counterexample_graph_from_compare():
    """run_and_compare 노드부터 시작하는 반례 찾기 워크플로우 그래프 구성"""
    return _build_base_graph("run_and_compare")