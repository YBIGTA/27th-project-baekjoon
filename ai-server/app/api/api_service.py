import re
from fastapi import Depends
from langchain_upstage import ChatUpstage
from app.api.api_schema import SolveRequest, SolveResponse
from langchain_core.output_parsers import StrOutputParser

from app.api.prompt import SOLVE_PROMPT


class AISolveService:
    """Service that would call an LLM/agent to produce solution code.

    For now, this is a stub that returns a simple template matching the
    requested language. Replace with real LLM logic later.
    """
    def __init__(self, chat: ChatUpstage):
        self.chat = chat

    def solve(self, req: SolveRequest) -> SolveResponse:
        lang = req.language
        code = self._bootstrap_code(lang, req.problem)
        return SolveResponse(code=code, language=lang, message="generated")

    def _bootstrap_code(self, lang: str, problem: str) -> str:
        """Generate a simple code template based on the requested language."""

        chain = SOLVE_PROMPT | self.chat | StrOutputParser()
        response = chain.invoke({
            "problem_description": problem, 
            "language": lang
        })

        code = self.extract_code_block(response) or '[ERROR]'

        return code

    @staticmethod
    def extract_code_block(markdown_text: str) -> str | None:
        """
        마크다운 텍스트에서 ``` ... ```으로 감싸진 코드 블록을 추출합니다.
        """
        patterns = [
            # ```python  \n code ... \n```
            r"```[ \t]*[a-zA-Z0-9._+-]+[ \t]*\r?\n([\s\S]*?)\r?\n?```",
            # ``` \n code ... \n```
            r"```\r?\n([\s\S]*?)\r?\n?```",
        ]

        for pat in patterns:
            match = re.search(pat, markdown_text)
            if match:
                return match.group(1).strip()

        return None
