import os
import re
import subprocess
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import asyncio

app = FastAPI()


WORKSPACE_DIR = Path(os.environ.get("BOJ_WORKSPACE", "/app/boj_workspace"))


class CodeRequest(BaseModel):
    problem_id: int = Field(..., description="백준 문제 번호")
    language: str = Field(..., description="언어 (예: python3, c++17)")
    code: str = Field(..., description="제출 코드")


class SubmitResponse(BaseModel):
    status: str
    raw_output: List[str]


@app.get("/health")
def health_check():
    return {"status": "ok"}


def _map_language(lang: str):
    lang = lang.lower()
    if lang in {"py", "python", "python3"}:
        return "py", "main.py"
    if "cpp" in lang or "c++" in lang:
        return "cpp", "main.cpp"
    # Extend as needed
    raise ValueError(f"지원하지 않는 언어입니다: {lang}")


def _ensure_workspace():
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    # If .boj directory missing, run `boj init`, then copy .boj directory
    if not (WORKSPACE_DIR / ".boj").exists():
        home_boj_dir = Path('/app/.boj')
        if home_boj_dir.exists():
            subprocess.run(["cp", "-r", str(home_boj_dir), str(WORKSPACE_DIR)], check=True)


def _ensure_problem(problem_id: int, filetype: str):
    problem_dir = WORKSPACE_DIR / 'problems' / str(problem_id)
    main_file = problem_dir / ("main.py" if filetype == "py" else "main.cpp")
    if not main_file.exists():
        # If directory exists but main file missing, we recreate with force.
        args = ["boj", "add", "-t", filetype, "-f", str(problem_id)]
        result = subprocess.run(args, cwd=WORKSPACE_DIR, text=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(f"boj add 실패: {result.stderr}")
    return problem_dir, main_file


def _write_code(main_file: Path, code: str):
    main_file.write_text(code, encoding="utf-8")


ACCEPT_PATTERNS = [
    (re.compile(r"Accepted", re.I), "Accepted"),
    (re.compile(r"Wrong Answer", re.I), "Wrong Answer"),
    (re.compile(r"Compile Error", re.I), "Compile Error"),
    (re.compile(r"Runtime Error", re.I), "Runtime Error"),
    (re.compile(r"Time Limit Exceeded", re.I), "Time Limit Exceeded"),
]


def _parse_status(lines: List[str]) -> str:
    # Search from end for known patterns
    for line in reversed(lines):
        for pattern, status in ACCEPT_PATTERNS:
            if pattern.search(line):
                return status
    return "Unknown"


async def _run_submit(problem_id: int) -> SubmitResponse:
    # Run `boj submit {id}` from workspace
    proc = await asyncio.create_subprocess_exec(
        "boj", "submit", str(problem_id),
        cwd=str(WORKSPACE_DIR),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    lines: List[str] = []
    assert proc.stdout is not None
    # Read line by line as bytes
    while True:
        line = await proc.stdout.readline()
        if not line:
            break
        try:
            decoded = line.decode('utf-8', errors='replace').rstrip('\n')
        except Exception:
            decoded = str(line)
        lines.append(decoded)
        print(decoded)
    await proc.wait()
    status = _parse_status(lines)
    if proc.returncode != 0 and status == "Unknown":
        raise RuntimeError("boj submit 실패")
    return SubmitResponse(status=status, raw_output=lines)


@app.post("/submit", response_model=SubmitResponse)
async def submit(req: CodeRequest):
    try:
        filetype, main_filename = _map_language(req.language)
        await asyncio.to_thread(_ensure_workspace)
        problem_dir, main_file = await asyncio.to_thread(_ensure_problem, req.problem_id, filetype)
        await asyncio.to_thread(_write_code, main_file, req.code)
        # Submit
        resp = await _run_submit(req.problem_id)
        return resp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알 수 없는 오류: {e}")
