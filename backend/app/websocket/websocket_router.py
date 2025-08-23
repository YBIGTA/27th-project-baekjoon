import json
import traceback
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from langchain_core.messages import BaseMessage  # (future use)

from app.problem.problem_service import SolvedProblemService
from app.problem.problem_repository import SolvedProblemRepository
from app.counterexample.runner import CounterexampleRunner
from app.dependencies import (
    get_solved_problem_service,
    get_solved_problem_repository,
    get_counterexample_runner,
)

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/counterexample")
async def counterexample_ws(
    websocket: WebSocket,
    service: SolvedProblemService = Depends(get_solved_problem_service),
    repo: SolvedProblemRepository = Depends(get_solved_problem_repository),
    counterexample_runner: CounterexampleRunner = Depends(get_counterexample_runner),
):
    """Counterexample 탐색 진행 상황 / LLM 출력 스트리밍 WebSocket.

        초기 메시지(JSON): {
        "problem_id": int,
        "user_code": str,
        "language": "python" (optional, default python)
    }
        이벤트 타입:
            - node_update: 그래프 노드 실행 후 상태 조각
            - message: (향후) LLM 메시지
            - finish: 최종 결과
            - error
    """
    await websocket.accept()
    try:
        init_text = await websocket.receive_text()
        init_payload = json.loads(init_text)
        problem_id = int(init_payload.get("problem_id"))
        user_code = init_payload.get("user_code", "")
        language = init_payload.get("language", "python")

        if not user_code:
            await websocket.send_json({"type": "error", "message": "user_code is required"})
            await websocket.close()
            return

        metadata = await service.get_problem_metadata(problem_id)
        solution = repo.get_problem_solution(problem_id)

        async for event in counterexample_runner.stream_find_counterexample(
            problem_description=metadata.description,
            user_code=user_code,
            language=language,
            difficulty=metadata.difficulty,
            correct_solution=solution.solution_code if solution else None,
            input_generator=solution.input_generator if solution else None,
            start_from_compare=True if solution else False,
        ):
            await websocket.send_json(event)
            if event.get("type") == "finish":
                break
    except WebSocketDisconnect:
        return
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "trace": traceback.format_exc(limit=2)
        })
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
