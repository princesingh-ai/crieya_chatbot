import pandas as pd
import yaml
from pathlib import Path

def load_config(file="config.yaml"):
    with open(file, "r") as f:
        config = yaml.safe_load(f)
    return config


def load_problem_statements():
    """Load and normalize SIH problem statements from Excel."""
    CONFIG = load_config()
    config = CONFIG["data"]["problem_statements"]
    df = pd.read_excel(config["path"], sheet_name=config["sheet"])
    return df.rename(columns={
        "Problem Creater's Organization": "organization",
        "Technology Bucket": "technology_bucket",
        "Category": "category",
        "Description": "description",
        "Title": "title",
        "ID": "problem_id",
    })


def load_innovation_process():
    """Load innovation process steps from Excel."""
    CONFIG = load_config()
    config = CONFIG["data"]["innovation_process"]
    df = pd.read_excel(config["path"], sheet_name=config["sheet"])
    return df.rename(columns={
        "Unnamed: 0": "process_no",
        "Unnamed: 1": "process_title",
        "Inputs": "input",
        "Process": "process",
        "Output": "output",
    })

def load_crieya_preincubation_hub():
    """Load CRIEYA pre-incubation hub text data."""
    CONFIG = load_config()
    config = CONFIG["data"]["crieya_preincubation_hub"]
    return Path(config["path"]).read_text(encoding="utf-8")

def load_crieya_focus():
    """Load CRIEYA focus areas text."""
    CONFIG = load_config()
    config = CONFIG["data"]["crieya_focus"]
    return Path(config["path"]).read_text(encoding="utf-8")

def load_trl_levels():
    """Load Technology Readiness Levels (TRL) text."""
    CONFIG = load_config()
    
    config = CONFIG["data"]["trl_levels"]
    return Path(config["path"]).read_text(encoding="utf-8")