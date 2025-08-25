import json
import traceback
import asyncio
from typing import AsyncGenerator
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

async def producer(websocket: WebSocket, gen: AsyncGenerator[dict, None], cancel_event: asyncio.Event):
    """
    스트림 생성기(gen)의 이벤트를 클라이언트에게 전송합니다.
    """
    try:
        async for event in gen:
            # cancel_event가 설정되면 즉시 중단합니다.
            if cancel_event.is_set():
                break
            
            if (data := event.get("data")) and isinstance(data, dict):
                sanitized_data = {k: v for k, v in data.items() if not k.startswith("_")}
                event["data"] = sanitized_data
            
            # send 중 연결이 끊기면 여기서 WebSocketDisconnect 예외가 발생합니다.
            await websocket.send_json(event)

            if event.get("type") == "finish":
                break
    except WebSocketDisconnect:
        print("Producer: 클라이언트가 전송 중 연결을 끊었습니다.")
    finally:
        # 이 태스크가 끝나면 cancel_event를 설정하여 다른 태스크도 종료시킵니다.
        cancel_event.set()


async def consumer(websocket: WebSocket, cancel_event: asyncio.Event):
    """
    클라이언트로부터의 메시지를 계속 수신 대기하여 연결 종료를 즉시 감지합니다.
    """
    try:
        while not cancel_event.is_set():
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Consumer: 클라이언트가 연결을 끊었습니다.")
    finally:
        cancel_event.set()


@router.websocket("/counterexample")
async def counterexample_ws(
    websocket: WebSocket,
    service: SolvedProblemService = Depends(get_solved_problem_service),
    repo: SolvedProblemRepository = Depends(get_solved_problem_repository),
    counterexample_runner: CounterexampleRunner = Depends(get_counterexample_runner),
):
    await websocket.accept()
    cancel_event = asyncio.Event()
    gen = None

    try:
        init_text = await websocket.receive_text()
        init_payload = json.loads(init_text)
        problem_id = int(init_payload.get("problem_id"))
        user_code = init_payload.get("user_code", "")
        language = init_payload.get("language", "python")

        if not user_code:
            await websocket.send_json({"type": "error", "message": "user_code is required"})
            return

        metadata = await service.get_problem_metadata(problem_id)
        solution = repo.get_problem_solution(problem_id)

        gen = counterexample_runner.stream_find_counterexample(
            problem_id=problem_id,
            problem_description=metadata.description,
            user_code=user_code,
            language=language,
            difficulty=metadata.difficulty,
            correct_solution=solution.solution_code if solution else None,
            input_generator=solution.input_generator if solution else None,
            start_from_compare=True if solution else False,
            cancel_event=cancel_event,
        )

        producer_task = asyncio.create_task(producer(websocket, gen, cancel_event))
        consumer_task = asyncio.create_task(consumer(websocket, cancel_event))

        done, pending = await asyncio.wait(
            {producer_task, consumer_task},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "trace": traceback.format_exc(limit=2)
        })
    finally:
        cancel_event.set()
        if gen:
            try:
                await gen.aclose()
            except Exception:
                pass
        try:
            await websocket.close()
        except Exception:
            pass