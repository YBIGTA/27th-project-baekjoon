from langchain.prompts import PromptTemplate

INPUT_GEN_TEMPLATE = """
당신은 세계 최고의 알고리즘 테스트 데이터 생성기입니다. 주어진 문제의 입력 형식과 제약을 분석하여, 해당 형식에 맞는 유효한 입력을 생성하는 프로그램 코드를 작성해주세요.

문제 설명:
{problem_description}

요구사항:
- 아래 문제의 입력 형식과 제약을 준수하는 입력을 출력(stdout)하는 프로그램을 {language}로 작성해주세요.
- 가능하다면 랜덤성을 사용하되, 제공된 시드(seed)가 있다면 이를 사용하여 재현 가능하도록 해주세요.
- 단일 파일로 전체 코드를 제공하고, 실행 시 표준 출력으로 테스트 케이스를 생성해야 합니다.
- 여러 테스트 케이스(cases)가 주어질 수 있음을 고려하고, 해당 수만큼 생성하도록 옵션을 지원하세요(없다면 1개 생성).
- 입력 형식이 애매하다면 합리적 가정을 명시하는 주석을 달아주세요.
- 반드시 전체 코드를 마크다운 코드 블록(``` ... ```)으로 감싸서 제공해주세요.
"""

INPUT_GEN_PROMPT = PromptTemplate.from_template(INPUT_GEN_TEMPLATE)