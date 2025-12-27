import pandas as pd
from pydantic  import BaseModel
from typing import Optional
from typing import List, Dict, Any

class ProblemSearchFilters (BaseModel):
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

class ProblemSearchResponse (BaseModel):
    """
    Standard response structure for problem search.
    - count   : number of matching records
    - results : list of problem statement records
    """
    count: int
    results: List[Dict[str, Any]]

DF = pd.read_excel("data/problem_statements.xlsx", sheet_name="Worksheet")

DF = DF.rename(columns={
    "Problem Creator's Organization": "organization",
    "Technology Bucket": "technology_bucket",
    "Category": "category",
    "Description": "description",
    "Title": "title",
    "ID": "problem_id",
})

def get_problem_statements(filters: ProblemSearchFilters) -> ProblemSearchResponse:
    """
    Filters problem statements based on provided search criteria.

    Args:
        filters (ProblemSearchFilters): Search parameters sent by client

    Returns:
        ProblemSearchResponse: Matching problem statements and count
    """

    # Create a copy so the original DataFrame remains untouched
    df = DF.copy()

    # Filter by exact problem ID match
    if filters.problem_id:
        df = df[df["problem_id"].astype(str) == filters.problem_id]

    # Filter by title
    if filters.title:
        df = df[df["title"].str.contains(filters.title, case=False, na=False)]

    # Filter by technology bucket
    if filters.technology_bucket:
        df = df[df["technology_bucket"].str.contains(filters.technology_bucket, case=False, na=False)]

    # Filter by category
    if filters.category:
        df = df[df["category"].str.contains(filters.category, case=False, na=False)]

    # Filter by description
    if filters.description:
        df = df[df["description"].str.contains(filters.description, case=False, na=False)]
    
    # filter by organization
    if filters.organization:
        df = df[df["organization"].str.contains(filters.organization, case=False, na=False)]

    # Convert filtered DataFrame into list of dictionaries
    records = df.to_dict(orient="records")

    # Return structured response
    return ProblemSearchResponse(
        count = len(records),
        results = records
    )