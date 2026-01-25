import pandas as pd
from core.models import *
from core.loaders import load_problem_statements, load_innovation_process, load_crieya_preincubation_hub, load_crieya_focus, load_trl_levels, load_annexure_registry

# Load datasets 
PS_DF = load_problem_statements()
IP_DF = load_innovation_process()
CRIEYA_HUB_DOC = load_crieya_preincubation_hub()
CRIEYA_FOCUS = load_crieya_focus()
TRL_LEVELS = load_trl_levels()
ANNEXURE_REGISTRY_DF = load_annexure_registry()

def get_problem_statements(filters: ProblemSearchFilters) -> ProblemSearchResponse:
    """
    Search SIH problem statements using optional filters.
    Exact match is used for problem_id, others are partial and case-insensitive.
    """
    df = PS_DF
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
    """
    Retrieve innovation process data.
    Can return full steps or only stage numbers and titles.
    """
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
    """
    Return CRIEYA pre-incubation hub information.
    """
    return CrieyaPreincubationHubQAResponse(answer=CRIEYA_HUB_DOC, source="Crieya Pre-Incubation Hub Document")


def get_crieya_focus_qa(request: CrieyaFocusQARequest) -> CrieyaFocusQAResponse:
    """
    Return CRIEYA focus areas and technologies.
    """
    return CrieyaFocusQAResponse(
        answer=CRIEYA_FOCUS,
        source="CRiEYA Focus Document"
    )

def get_trl_levels(request: TrlLevelRequest) -> TrlLevelResponse:
    """
    Return Technology Readiness Level (TRL) definitions.
    """
    return TrlLevelResponse(
        answer=TRL_LEVELS,
        source="TRL Levels Document"
    )

def get_annexure_registry(request: AnnexureRegistryRequest) -> AnnexureRegistryResponse:
    df = ANNEXURE_REGISTRY_DF

    if request.annexure_id:
        df = df[df["annexure_id"] == request.annexure_id.upper().strip()]

    if request.keyword:
        df = df[df.apply(lambda row: row.astype(str).str.contains(request.keyword, case=False, na=False).any(), axis=1)]

    results = [
        AnnexureRegistry(
            annexure_id=row["annexure_id"],
            title=row["title"],
            file_name=row["file_name"],
            url=None if pd.isna(row.get("url")) else row.get("url")
        )for _, row in df.iterrows()
    ]

    return AnnexureRegistryResponse(
        count=len(results),
        results=results,
    )