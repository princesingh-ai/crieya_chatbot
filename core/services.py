import pandas as pd
from core.models import *
from core.loaders import load_problem_statements, load_innovation_process, load_crieya_preincubation_hub, load_crieya_focus, load_trl_levels

# Load datasets 
PS_DF = load_problem_statements()
IP_DF = load_innovation_process()
CRIEYA_HUB_DOC = load_crieya_preincubation_hub()
CRIEYA_FOCUS = load_crieya_focus()
TRL_LEVELS = load_trl_levels()

def get_problem_statements(filters: ProblemSearchFilters):
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

    return {
        "count": len(records),
        "results": records
    }


def get_innovation_process(filters: InnovationProcessFilters):
    df = IP_DF

    if filters.process_no is not None:
        df = df[df["process_no"] == filters.process_no]

    if filters.stages is True and filters.field is None:
        records = df[["process_no", "process_title"]].to_dict(orient="records")
        return {
        "count": len(records),
        "results": records
        }
    
    if filters.field == "title":
        df = df[["process_no", "process_title"]]

    elif filters.field == "input":
        df =df[["process_no", "input"]]
    
    elif filters.field == "process":
        df = df[["process_no", "process"]]
    
    elif filters.field == "output":
        df = df[["process_no", "output"]]

    records = df.to_dict(orient="records")

    return {
        "count": len(records),
        "results": records
    }


def get_crieya_preincubation_hub_qa(request: CrieyaPreincubationHubQARequest):
    """
    Return CRIEYA pre-incubation hub information.
    """
    return {
        "answer": CRIEYA_HUB_DOC,
        "source": "Crieya Pre-Incubation Hub Document"
    }


def get_crieya_focus_qa(request: CrieyaFocusQARequest):
    """
    Return CRIEYA focus areas and technologies.
    """
    return {
        "answer": CRIEYA_FOCUS,
        "source": "CRiEYA Focus Document"
    }

def get_trl_levels(request: TrlLevelRequest):
    """
    Return Technology Readiness Level (TRL) definitions.
    """
    return {
        "answer": TRL_LEVELS,
        "source": "TRL Levels Document"
    }