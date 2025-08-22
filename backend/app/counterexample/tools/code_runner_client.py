import requests
import json
from typing import Dict, Any, List
from app.config import CODE_RUNNER_URL

class CodeRunnerClient:
    """코드 실행 서비스와 통신하는 클라이언트"""
    
    def __init__(self, base_url: str = CODE_RUNNER_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def run_code_with_input(self, code: str, input_data: str, language: str = "python") -> Dict[str, Any]:
        """
        임시 사용 용도로 만듦
        """
        input_data_repr = repr(input_data)
        input_simulate_code = (
            f"import sys\n"
            f"from io import StringIO\n"
            f"sys.stdin = StringIO({input_data_repr})\n\n"
        )
        return self.run_code(input_simulate_code + code, language)

    def run_code(self, code: str, language: str = "python") -> Dict[str, Any]:
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
            "language": language
        }
        
        try:
            response = self.session.post(endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "output": result.get("output", ""),
                "error": result.get("error", ""),
                "status": result.get("status", "unknown"),
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
    
    def health_check(self) -> bool:
        """코드 실행 서비스 상태 확인"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_supported_languages(self) -> List[str]:
        """지원하는 프로그래밍 언어 목록 조회"""
        try:
            response = self.session.get(f"{self.base_url}/languages", timeout=5)
            if response.status_code == 200:
                return response.json().get("languages", ["python"])
        except:
            pass
        return ["python"]  # 기본값