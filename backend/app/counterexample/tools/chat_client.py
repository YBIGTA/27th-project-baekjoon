from langchain_upstage import ChatUpstage
from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from app.config import UPSTAGE_API_KEY, OPENAI_API_KEY


def get_counterexample_chat(difficulty: int = 0) -> BaseChatOpenAI:
    # TODO: 더욱 세련된 구현으로 바꿔볼 수 있음
    if difficulty <= 0:
        return ChatUpstage(
            api_key=UPSTAGE_API_KEY,
            model="solar-pro2",
            reasoning_effort="medium",
        )
    elif difficulty <= 5:
        return ChatUpstage(
            api_key=UPSTAGE_API_KEY,
            model="solar-pro2",
            reasoning_effort="minimal",
        )
    elif difficulty <= 10:
        return ChatUpstage(
            api_key=UPSTAGE_API_KEY,
            model="solar-pro2",
            reasoning_effort="low",
        )
    elif difficulty <= 15:
        return ChatUpstage(
            api_key=UPSTAGE_API_KEY,
            model="solar-pro2",
            reasoning_effort="medium",
        )
    elif difficulty <= 20:
        return ChatUpstage(
            api_key=UPSTAGE_API_KEY,
            model="solar-pro2",
            reasoning_effort="high",
        )
    else:
        return ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt5",
            reasoning_effort="high",
        )
