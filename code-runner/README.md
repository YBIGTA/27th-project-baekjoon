# Code Runner 서비스

## 개요

Code Runner는 사용자로부터 제출된 코드 스니펫을 안전하게 실행하기 위해 설계된 FastAPI 기반 서비스입니다. Docker를 활용하여 격리된 샌드박스 환경에서 코드를 실행하므로, 온라인 코딩 플랫폼이나 교육용 도구와 같이 신뢰할 수 없는 코드를 평가해야 하는 애플리케이션에 적합합니다.

## 주요 기능

- **보안 실행**: 사용자 코드는 호스트 및 다른 서비스와 완전히 격리된 임시 Docker 컨테이너 내부에서 실행됩니다.
- **리소스 제한**: 각 컨테이너는 무분별한 사용을 방지하기 위해 CPU 및 메모리 사용량이 제한됩니다.
- **네트워크 차단**: 실행 컨테이너는 외부 API 호출이나 악의적인 공격을 방지하기 위해 네트워킹이 비활성화됩니다.
- **비동기 API**: 서비스는 비동기 엔드포인트를 사용하여 블로킹 없이 여러 요청을 효율적으로 처리합니다.
- **헬스 체크 및 자동 재시작**: 서비스의 상태를 지속적으로 확인하고, 문제 발생 시 자동으로 재시작하여 안정성을 높입니다.

## 시작하기

### 요구사항

- Docker
- Docker Compose
- Python 3.12 이상

### 서비스 실행 방법

#### Docker Compose 사용 (권장)

이 서비스는 메인 프로젝트의 `docker-compose.yml`의 일부로 실행되도록 설정되어 있습니다.

1.  **서비스 빌드 및 실행:**
    ```bash
    # 프로젝트 최상위 디렉터리에서 실행
    docker-compose up --build code-runner
    ```
2.  서비스는 `http://localhost:8001`에서 접근할 수 있습니다.

#### 단독 실행

호스트 머신에서 Docker 데몬이 실행 중인 경우, 서비스를 직접 실행할 수도 있습니다.

1.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **서버 실행:**
    ```bash
    # 참고: 포트는 백엔드 서비스와의 충돌을 피하기 위해 8001로 설정되었습니다.
    uvicorn main:app --host 0.0.0.0 --port 8001
    ```

## API 명세

### `POST /run-code`

주어진 코드 스니펫을 실행하고 표준 출력 또는 오류를 반환합니다.

- **요청 본문 (Request Body)**:

  ```json
  {
    "language": "python",
    "code": "print('Hello, from the container!')"
  }
  ```

  - `language` (string, 필수): 코드의 프로그래밍 언어입니다. 현재는 "python"만 지원됩니다.
  - `code` (string, 필수): 실행할 소스 코드입니다.

- **성공 응답 (`200 OK`)**:

  ```json
  {
    "output": "Hello, from the container!\n"
  }
  ```

- **오류 응답 (`200 OK`)**:

  ```json
  {
    "error": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nNameError: name 'prit' is not defined\n"
  }
  ```

### `GET /health`

서비스의 동작 상태를 확인하는 헬스 체크 엔드포인트입니다.

- **요청 본문**: 없음
- **성공 응답 (`200 OK`)**:
  서비스가 정상적으로 실행 중인 경우, 다음과 같은 응답을 반환합니다.
  ```json
  {
    "status": "ok"
  }
  ```

## Docker Compose 상세 설정

`docker-compose.yml` 파일에는 서비스의 안정성을 높이기 위해 다음과 같은 설정이 추가되었습니다.

- **`restart: unless-stopped`**: 컨테이너에 예기치 않은 오류가 발생하더라도, 사용자가 직접 중지하지 않는 한 자동으로 재시작됩니다.
- **`healthcheck`**: 주기적으로 `/health` API를 호출하여 컨테이너가 정상적으로 동작하는지 확인합니다. 만약 비정상 상태가 감지되면 컨테이너가 재시작될 수 있습니다.

## 보안 모델

이 서비스는 "Docker-out-of-Docker" 접근 방식을 사용합니다. `code-runner` 컨테이너 자체는 호스트의 Docker 소켓 (`/var/run/docker.sock`)에 접근 권한을 가집니다. 이는 높은 권한을 부여하지만, 서비스는 통제된 게이트웨이 역할을 하여 위험을 완화하도록 설계되었습니다.

**사용자가 제출한 모든 코드는 서비스 컨테이너 자체에서 절대 실행되지 않습니다.** 대신, 다음과 같은 제한 사항이 적용된 **별도의, 수명이 짧은, 샌드박스 처리된 컨테이너**에서 실행됩니다.

- **네트워크 접근 불가** (`network_disabled=True`)
- **엄격한 메모리 제한** (`mem_limit="128m"`)
- **제한된 CPU 사용량** (`cpu_quota`)

이 모델은 잠재적으로 악의적인 사용자 코드가 격리된 상태를 유지하고 호스트 시스템이나 다른 서비스를 손상시키지 않도록 보장합니다.
