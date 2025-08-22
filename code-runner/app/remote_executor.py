import docker
import argparse
import json
import base64

# 이 스크립트는 원격 EC2 인스턴스에서 실행됩니다.

client = docker.from_env()

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

def execute_code(language: str, code: str):
    """주어진 코드를 도커 컨테이너에서 실행하고 결과를 반환합니다."""
    if language not in SUPPORTED_LANGUAGES:
        return {"error": f"지원하지 않는 언어: {language}"}

    lang_config = SUPPORTED_LANGUAGES[language]
    image = lang_config["image"]
    
    # 컴파일 및 실행 명령을 정의합니다.
    if language == "c":
        # 1. 코드를 a.c에 씁니다.
        # 2. a.c를 a.out으로 컴파일합니다.
        # 3. a.out을 실행합니다.
        command = ["/bin/sh", "-c", "echo \"$CODE\" > a.c && gcc a.c -o a.out && ./a.out"]
    elif language == "cpp":
        command = ["/bin/sh", "-c", "echo \"$CODE\" > a.cpp && g++ a.cpp -o a.out && ./a.out"]
    elif language == "java":
        command = ["/bin/sh", "-c", "echo \"$CODE\" > Main.java && javac Main.java && java Main"]
    else: # Python, Javascript
        command = lang_config["command"] + [code]

    try:
        # 환경 변수로 코드를 전달하여 셸 주입을 방지합니다.
        environment = {"CODE": code} if language in ["c", "cpp", "java"] else {}

        container = client.containers.run(
            image=image,
            command=command,
            environment=environment,
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
        # 너무 큰 오류 메시지를 피하기 위해 stderr의 크기를 제한합니다.
        error_output = e.stderr.decode("utf-8", errors='ignore')[:2000]
        return {"error": error_output}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="도커 컨테이너에서 코드를 실행합니다.")
    parser.add_argument("--language", required=True, help="프로그래밍 언어.")
    parser.add_argument("--code_base64", required=True, help="실행할 base64 인코딩된 코드.")

    args = parser.parse_args()

    try:
        decoded_code = base64.b64decode(args.code_base64).decode('utf-8')
        result = execute_code(args.language, decoded_code)
    except Exception as e:
        result = {"error": f"코드를 디코딩하거나 실행하지 못했습니다: {str(e)}"}
    
    print(json.dumps(result))