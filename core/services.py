from core.models import *
from core.loaders import load_problem_statements, load_innovation_process

# Load datasets 
PS_DF = load_problem_statements()
IP_DF = load_innovation_process()


def get_problem_statements(filters: ProblemSearchFilters) -> ProblemSearchResponse:
    """
    Filters problem statements based on provided search criteria.

    Args:
        filters (ProblemSearchFilters): Search parameters sent by client

    Returns:
        ProblemSearchResponse: Matching problem statements and count
    """

    # Create a copy so the original DataFrame remains untouched
    df = PS_DF.copy()

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


def get_innovation_process(filters: InnovationProcessFilters) -> InnovationProcessResponse:
    df = IP_DF.copy()

    process_id = filters.process_no if filters.process_no is not None else filters.level
    if process_id is not None:
        df = df[df["process_no"] == process_id]

    if filters.all_processes:
        records = df[["process_no", "process_title"]].to_dict(orient="records")
        return InnovationProcessResponse(count=len(records), results=records)

    return InnovationProcessResponse(
        count=len(df),
        results=df.to_dict(orient="records")
    )


def answer_from_innovation_process(request: InnovationQARequest) -> InnovationQAResponse:
    df = IP_DF[IP_DF["process_no"] == request.level]

    if df.empty:
        raise ValueError("Invalid innovation level")

    row = df.iloc[0]

    return InnovationQAResponse(
        level=request.level,
        process_title=row["process_title"],
        answer_context={
            "input": row["input"],
            "process": row["process"],
            "output": row["output"],
        },
        question=request.question,
    )