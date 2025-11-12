import yaml
from pathlib import Path


def load_config(config_path: str = "config.yaml") -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    print(f"Loaded config from {path}")
    return config


# Get project root Path
def get_project_root() -> Path:
    return Path(__file__).parent.parent


# Paths
project_root = get_project_root()
config = load_config()

input_path = project_root / config["paths"]["input_file"]

output_dir = project_root / config["paths"]["output_dir"]
output_dir.mkdir(parents=True, exist_ok=True)
chunks_path = output_dir / config["paths"]["chunks_file"]

cache_dir = project_root / config["paths"]["cache_dir"]
cache_dir.mkdir(parents=True, exist_ok=True)

mapping_path = output_dir / "index_mapping.json"