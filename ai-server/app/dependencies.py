"""DI providers for the AI solver service (and future deps)."""

from app.api.api_service import AISolveService


def get_solve_service() -> AISolveService:
	"""Provide AISolveService instance. Replace with stateful/LLM client later."""
	return AISolveService()
