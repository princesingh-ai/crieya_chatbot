from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ProblemSearchFilters(BaseModel):
    """
    Defines all optional filters that can be applied
    while searching problem statements.
    Each field is optional and applied only if provided.
    """
    problem_id: Optional[str] = None
    title: Optional[str] = None
    technology_bucket: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    organization: Optional[str] = None


class ProblemSearchResponse(BaseModel):
    """
    Standard response structure for problem search.
    - count   : number of matching records
    - results : list of problem statement records
    """
    count: int
    results: List[Dict[str, Any]]


class InnovationProcessFilters(BaseModel):
    process_no: Optional[int] = None
    stages: bool = False
    field: Optional[str] = None

class InnovationProcessResponse(BaseModel):
    count: int
    results: List[Dict[str, Any]]

class CrieyaPreincubationHubQARequest(BaseModel):
    question: str

class CrieyaPreincubationHubQAResponse(BaseModel):
    answer: str
    source: str

class CrieyaFocusQARequest(BaseModel):
    question: str


class CrieyaFocusQAResponse(BaseModel):
    answer: str
    source: str

class TrlLevelRequest(BaseModel):
    question: str

class TrlLevelResponse(BaseModel):
    answer: str
    source: str

class AicGuidelinesRequest(BaseModel):
    section: Optional[str] = None
    keyword: Optional[str] = None

class AicGuidelinesSection(BaseModel):
    section_name: str
    content: Any

class AicGuidelinesResponse(BaseModel):
    count: int
    results: List[AicGuidelinesSection]
    source: str = "AIC_Guidelines Seed Fund Scheme Document"