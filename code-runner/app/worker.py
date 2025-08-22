import docker
from celery import Celery

# Celery 애플리케이션을 생성합니다.
# 브로커로 Redis를 사용하고, 결과 저장을 위해 Redis를 백엔드로 설정합니다.
celery_app = Celery(
    "code_runner_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

client = docker.from_env()

# 지원할 언어와 해당 언어의 도커 이미지, 실행 명령어를 정의합니다.
SUPPORTED_LANGUAGES = {
    "python": {
        "image": "python:3.12-slim",
        "command": ["python3", "-c"],
    },
    "javascript": {
        "image": "node:18-slim",
        "command": ["node", "-e"],
    },
    "c": {
        "image": "gcc:12.3",
        "command": ["/bin/sh", "-c"],
    },
    "cpp": {
        "image": "gcc:12.3",
        "command": ["/bin/sh", "-c"],
    },
    "java": {
        "image": "openjdk:17-slim",
        "command": ["/bin/sh", "-c"],
    },
}


@celery_app.task
def run_code_task(language: str, code: str):
    """Celery 작업으로, 주어진 코드를 Docker 컨테이너에서 실행합니다."""
    if language not in SUPPORTED_LANGUAGES:
        return {"error": f"Unsupported language: {language}"}

    lang_config = SUPPORTED_LANGUAGES[language]
    image = lang_config["image"]
    command = lang_config["command"].copy()

    if language == "c":
        command.append(f"echo '{code}' > a.c && gcc a.c -o a.out && ./a.out")
    elif language == "cpp":
        command.append(f"echo '{code}' > a.cpp && g++ a.cpp -o a.out && ./a.out")
    elif language == "java":
        command.append(f"echo '{code}' > Main.java && javac Main.java && java Main")
    else:
        command.append(code)

    try:
        container = client.containers.run(
            image=image,
            command=command,
            detach=False,
            remove=True,
            network_disabled=True,
            mem_limit="128m",
            cpu_period=100000,
            cpu_quota=50000,  # 0.5 CPU
            stderr=True,
            stdout=True,
            tty=False,
        )
        return {"output": container.decode("utf-8")}
    except docker.errors.ContainerError as e:
        return {"error": e.stderr.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}
