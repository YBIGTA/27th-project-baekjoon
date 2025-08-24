import aiohttp
import json
from typing import Dict, Any, List
from app.config import BOJ_RUNNER_URL

class AcmicpcClient:
    """백준 제출 서비스와 통신하는 클라이언트"""

    def __init__(self, base_url: str = BOJ_RUNNER_URL):
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

    async def submit_code(self, problem_id: int, code: str, language: str = "python") -> Dict[str, Any]:
        """
        백준 제출 요청
        
        Args:
            problem_id: 제출할 문제 번호
            input_data: 입력 데이터
            language: 프로그래밍 언어
            
        Returns:
            실행 결과 (output, error, status 등)
        """
        endpoint = f"{self.base_url}/submit"
        
        payload = {
            "problem_id": problem_id,
            "language": language,
            "code": code
        }

        if not self.session:
            raise RuntimeError("세션이 초기화되지 않았습니다. 'async with' 문을 사용하여 세션을 관리하세요.")
        
        try:
            async with self.session.post(endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=300)) as response:
                response.raise_for_status()
                result = await response.json()
                return {
                    "status": result.get("status", ""),
                    "raw_output": result.get("raw_output", ""),
                    "error": result.get("error", "")
                }
            
        except aiohttp.ClientError as e:
            return {
                "error": f"백준 제출 서비스 연결 실패: {str(e)}",
                "status": "connection_error",
                "raw_output": ""
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"응답 파싱 실패: {str(e)}",
                "status": "parse_error",
                "raw_output": ""
            }
        except Exception as e:
            return {
                "error": f"예상치 못한 오류: {str(e)}",
                "raw_output": "",
                "status": "unknown_error"
            }
    
    async def health_check(self) -> bool:
        """백준 제출 서비스 상태 확인"""
        if not self.session:
            raise RuntimeError("세션이 초기화되지 않았습니다. 'async with' 문을 사용하여 세션을 관리하세요.")
        try:
            async with self.session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
        except:
            return False