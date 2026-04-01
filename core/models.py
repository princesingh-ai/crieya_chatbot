from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ProblemSearchFilters(BaseModel):
    problem_id: Optional[str] = Field(
        None, description="Unique identifier of the problem (e.g., SIH1524)"
    )
    title: Optional[str] = Field(
        None, description="Keywords from the problem title"
    )
    technology_bucket: Optional[str] = Field(
        None, description="Technology domain (e.g., AI, IoT)"
    )
    category: Optional[str] = Field(
        None, description="Problem category"
    )
    description: Optional[str] = Field(
        None, description="Keywords from problem description"
    )
    organization: Optional[str] = Field(
        None, description="Organization name"
    )


# class ProblemSearchResponse(BaseModel):
#     """
#     Standard response structure for problem search.
#     - count   : number of matching records
#     - results : list of problem statement records
#     """
#     count: int
#     results: List[Dict[str, Any]]


class InnovationProcessFilters(BaseModel):
    process_no: Optional[int] = Field(
        None, description="Specific process number"
    )
    stages: bool = Field(
        False, description="Return only process titles if True"
    )
    field: Optional[str] = Field(
        None, description="Which field to return (title, input, process, output)"
    )


# class InnovationProcessResponse(BaseModel):
#     count: int
#     results: List[Dict[str, Any]]

class CrieyaPreincubationHubQARequest(BaseModel):
    query: str

# class CrieyaPreincubationHubQAResponse(BaseModel):
#     answer: str
#     source: str

class CrieyaFocusQARequest(BaseModel):
    query: str


# class CrieyaFocusQAResponse(BaseModel):
#     answer: str
#     source: str

class TrlLevelRequest(BaseModel):
    query: str

# class TrlLevelResponse(BaseModel):
#     answer: str
#     source: str