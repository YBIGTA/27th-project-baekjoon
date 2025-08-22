from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class ProblemData(BaseModel):
    problem_id: int = Field(..., description="문제 번호")
    title: str = Field(..., description="문제 제목")
    description: str = Field(..., description="문제 설명 HTML")
    constraints: str = Field(..., description="제한사항 HTML")
    input_description: str = Field(..., description="입력 설명 HTML")
    output_description: str = Field(..., description="출력 설명 HTML")


# Solved AC types
class Language(str, Enum):
    """지원되는 언어"""
    KOREAN = "ko"
    ENGLISH = "en" 
    JAPANESE = "ja"


class ProblemTagAlias(BaseModel):
    """문제 태그 별명"""
    alias: str = Field(..., description="별칭")


class ProblemTagNameTranslated(BaseModel):
    """언어별 태그 이름"""
    language: Language = Field(..., description="태그 이름이 작성된 언어")
    name: str = Field(..., description="이름")
    short: str = Field(..., description="짧은 이름. 따로 없을 경우 name과 같은 값")


class ProblemTag(BaseModel):
    """solved.ac 문제 태그 스키마"""
    key: str = Field(..., description="solved.ac에서 쓰는 태그 ID", examples=["arbitrary_precision"])
    isMeta: bool = Field(..., description="메타 태그 여부", examples=[False])
    bojTagId: int = Field(..., description="백준 온라인 저지에서 쓰는 태그 ID", examples=[117])
    problemCount: int = Field(..., description="태그가 붙은 문제 수", examples=[241])
    displayNames: List[ProblemTagNameTranslated] = Field(..., description="언어별 태그 이름 목록")
    aliases: List[ProblemTagAlias] = Field(default_factory=list, description="별명 목록. 빈 배열일 수 있음")


class SolvedAcData(BaseModel):
    level: int = Field(..., description="문제 난이도")
    tags: List[ProblemTag] = Field(default_factory=list, description="문제 태그")


# Full problem info
class FullProblemInfo(ProblemData, SolvedAcData):
    pass