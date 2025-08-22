from langchain.prompts import PromptTemplate

SOLVE_TEMPLATE = """
당신은 세계 최고의 알고리즘 문제 해결사입니다. 주어진 문제를 해결하기 위한 코드를 작성해주세요.

문제 설명:
{problem_description}

요구사항:
- 아래 문제를 해결하는 코드를 {language}로 작성해주세요.
- 코드에는 각 로직에 대한 자세한 주석을 포함해주세요.
- 코드 실행에 필요한 전체 코드를 제공해주세요. (예: 입력 처리 부분 포함)
- **반드시 전체 코드를 마크다운 코드 블록(``` ... ```)으로 감싸서 제공해주세요.**
"""

SOLVE_PROMPT = PromptTemplate.from_template(SOLVE_TEMPLATE)