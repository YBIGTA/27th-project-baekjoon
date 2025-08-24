import docker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
client = docker.from_env()

class CodeRequest(BaseModel):
    language: str
    code: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/run-code")
async def run_code(req: CodeRequest):
    if req.language != "python":
        raise HTTPException(status_code=400, detail="Only Python supported")

    try:
        container = client.containers.run(
            image="python:3.12-slim",
            command=["python3", "-c", req.code],
            detach=False,
            remove=True,
            network_disabled=True,
            mem_limit="128m",
            cpu_period=100000,
            cpu_quota=50000,  # 0.5 CPU
            stderr=True,
            stdout=True,
            tty=False
        )
        return {"output": container.decode("utf-8")}
    except docker.errors.ContainerError as e:
        return {"error": e.stderr.decode("utf-8")}
