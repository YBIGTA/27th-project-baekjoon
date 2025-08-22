import httpx
import asyncio
from bs4 import BeautifulSoup, Tag
from typing import Optional

from .crawler_schema import ProblemData, ProblemTag, SolvedAcData, FullProblemInfo


class AcmicpcCrawler:
    BASE_URL = "https://www.acmicpc.net/problem/{problem_id}"
    SOLVED_AC_URL = "https://solved.ac/api/v3/problem/show"

    async def fetch_problem(self, problem_id: int) -> Optional[ProblemData]:
        """
        acmicpc.net에서 문제 정보를 비동기적으로 크롤링합니다.
        User-Agent 헤더를 추가하여 403 차단을 우회합니다.
        """
        url = self.BASE_URL.format(problem_id=problem_id)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
                response = await client.get(url)
                response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Error fetching problem {problem_id}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("span", id="problem_title")
        if not title_tag:
            return None  # 문제가 없는 페이지

        # 섹션별 HTML 추출
        description = self._get_section_html(soup, "problem_description")
        input_desc = self._get_section_html(soup, "problem_input")
        output_desc = self._get_section_html(soup, "problem_output")

        # '제한' 섹션은 ID가 없으므로 h2 태그로 검색
        limit_h2 = soup.find("h2", string="제한")
        constraints = str(limit_h2.find_next_sibling("div")) if limit_h2 and isinstance(limit_h2.find_next_sibling("div"), Tag) else ""

        return ProblemData(
            problem_id=problem_id,
            title=title_tag.get_text(strip=True),
            description=description,
            constraints=constraints,
            input_description=input_desc,
            output_description=output_desc,
        )
    
    async def fetch_solved_ac_problem(self, problem_id: int) -> Optional[SolvedAcData]:
        """
        Solved.ac API를 사용하여 문제 정보를 비동기적으로 크롤링합니다.
        """
        params = {"problemId": problem_id}
        headers = {
            "x-solvedac-language": "ko"
        }
        try:
            async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
                response = await client.get(self.SOLVED_AC_URL, params=params)
                response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Error fetching Solved.ac problem {problem_id}: {e}")
            return None

        data = response.json()
        if not data or "problemId" not in data:
            return None

        print(data.get("tags", []))

        return SolvedAcData(
            level=data.get("level", 0),
            tags=[ProblemTag(**tag) for tag in data.get("tags", [])]
        )
    
    async def fetch_full_problem(self, problem_id: int) -> Optional[FullProblemInfo]:
        acmicpc_data, solved_ac_data = await asyncio.gather(
            self.fetch_problem(problem_id),
            self.fetch_solved_ac_problem(problem_id)
        )

        if not acmicpc_data or not solved_ac_data:
            return None

        return FullProblemInfo(
            **acmicpc_data.model_dump(),
            **solved_ac_data.model_dump()
        )

    def _get_section_html(self, soup: BeautifulSoup, section_id: str) -> str:
        section = soup.find("div", id=section_id)
        return str(section) if section else ""
