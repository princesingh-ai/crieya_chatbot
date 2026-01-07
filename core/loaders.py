import pandas as pd
import yaml


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