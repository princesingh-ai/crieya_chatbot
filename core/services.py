from core.models import *
from core.loaders import load_problem_statements, load_innovation_process, load_crieya_preincubation_hub, load_crieya_focus

# Load datasets 
PS_DF = load_problem_statements()
IP_DF = load_innovation_process()
CRIEYA_HUB_DOC = load_crieya_preincubation_hub()


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

    process_id = filters.process_no
    if process_id is not None:
        df = df[df["process_no"] == process_id]

    if filters.stages:
        records = df[["process_no", "process_title"]].to_dict(orient="records")
        return InnovationProcessResponse(count=len(records), results=records)

    return InnovationProcessResponse(
        count=len(df),
        results=df.to_dict(orient="records")
    )


def get_crieya_preincubation_hub_qa(request: CrieyaPreincubationHubQARequest) -> CrieyaPreincubationHubQAResponse:
    return CrieyaPreincubationHubQAResponse(answer=CRIEYA_HUB_DOC, source="Crieya Pre-Incubation Hub Document")


def get_crieya_focus_qa(request: CrieyaFocusQARequest) -> CrieyaFocusQAResponse:
    text = load_crieya_focus()

    return CrieyaFocusQAResponse(
        answer=text,
        source="CRiEYA Focus Document"
    )