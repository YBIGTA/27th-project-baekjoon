"""DI providers for the AI solver service (and future deps)."""

from app.api.api_service import AISolveService
from langchain_upstage import ChatUpstage
from app.config import UPSTAGE_API_KEY


def get_solve_service() -> AISolveService:
	"""Provide AISolveService instance. Replace with stateful/LLM client later."""
	return AISolveService(chat=get_chat_service())

def get_chat_service() -> ChatUpstage:
	"""Provide ChatUpstage instance."""
	return ChatUpstage(
		api_key=UPSTAGE_API_KEY,
		model="solar-pro2",
		reasoning_effort="high"
	)