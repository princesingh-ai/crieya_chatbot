import pandas as pd
import yaml
from pathlib import Path


with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)


def load_problem_statements():
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
    config = CONFIG["data"]["crieya_preincubation_hub"]
    return Path(config["path"]).read_text(encoding="utf-8")

def load_crieya_focus():
    path = CONFIG["data"]["crieya_focus"]["path"]
    return Path(path).read_text(encoding="utf-8")