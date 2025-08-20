from langchain_upstage import ChatUpstage
from app.config import UPSTAGE_API_KEY


def get_counterexample_chat() -> ChatUpstage:
    return ChatUpstage(
        api_key=UPSTAGE_API_KEY,
        model="solar-pro2",
        reasoning_effort="high",
    )
