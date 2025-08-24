import aiohttp
import asyncio
import requests
import json
from typing import Dict, Any, List
from app.config import CODE_RUNNER_URL

PENDING = "PENDING"


class CodeRunnerClient:
    """코드 실행 서비스와 통신하는 클라이언트"""
    
    def __init__(self, base_url: str = CODE_RUNNER_URL):
        self.base_url = base_url
        self.session = None
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def run_code(self, code: str, input_data: str, language: str = "python") -> Dict[str, Any]:
        """
        코드 실행 요청
        
        Args:
            code: 실행할 코드
            input_data: 입력 데이터
            language: 프로그래밍 언어
            
        Returns:
            실행 결과 (output, error, status 등)
        """
        endpoint = f"{self.base_url}/run-code"
        
        payload = {
            "code": code,
            "language": language,
            "input_value": input_data
        }
        
        try:
            if not self.session:
                raise RuntimeError("세션이 초기화되지 않았습니다. 'async with' 문을 사용하여 세션을 관리하세요.")

            response = await self.session.post(endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=30))
            response.raise_for_status()

            result = await response.json()
            task_id: str | None = result.get("task_id")

            if not task_id:
                raise ValueError("작업 ID가 없습니다.")

            task_status = PENDING
            while task_status == PENDING:
                task_response = await self.session.get(f"{self.base_url}/results/{task_id}", timeout=aiohttp.ClientTimeout(total=30))
                task_response.raise_for_status()
                task_result = await task_response.json()
                task_status = task_result.get("status", PENDING)
                if task_status == PENDING:
                    await asyncio.sleep(1)

            task_result: dict[str, Any] = task_result.get("result", {})  # type: ignore
            task_output = task_result.get("output", "")
            task_error = task_result.get("error", "")
            task_status = task_result.get("status", "unknown")

            return {
                "output": task_output,
                "error": task_error,
                "status": task_status,
                "execution_time": result.get("execution_time", 0)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "output": "",
                "error": f"코드 실행 서비스 연결 실패: {str(e)}",
                "status": "connection_error",
                "execution_time": 0
            }
        except json.JSONDecodeError as e:
            return {
                "output": "",
                "error": f"응답 파싱 실패: {str(e)}",
                "status": "parse_error",
                "execution_time": 0
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"예상치 못한 오류: {str(e)}",
                "status": "unknown_error",
                "execution_time": 0
            }
    
    async def health_check(self) -> bool:
        """코드 실행 서비스 상태 확인"""
        if not self.session:
            raise RuntimeError("세션이 초기화되지 않았습니다. 'async with' 문을 사용하여 세션을 관리하세요.")
        try:
            response = await self.session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(5))
            return response.status == 200
        except:
            return False

    async def get_supported_languages(self) -> List[str]:
        """지원하는 프로그래밍 언어 목록 조회"""
        if not self.session:
            raise RuntimeError("세션이 초기화되지 않았습니다. 'async with' 문을 사용하여 세션을 관리하세요.")
        try:
            response = await self.session.get(f"{self.base_url}/languages", timeout=aiohttp.ClientTimeout(5))
            if response.status == 200:
                return (await response.json()).get("languages", ["python"])
        except:
            pass
        return ["python"]  # 기본값