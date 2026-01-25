import re
from core.models import AnnexureRegistry
from core.services import get_annexure_registry

ANNEXURE_REGEX = re.compile(r"Annexure\s+([A-Z])", re.IGNORECASE)

def extract_annexure_ids(text: str) -> set[str]:
    return {
        match.group(1).upper() for match in ANNEXURE_REGEX.finditer(text)
    }

def attach_annexure_links(answer_text: str) -> dict:
    annexure_ids = extract_annexure_ids(answer_text)
    annexures = []

    for annexure_id in annexure_ids:
        response = get_annexure_registry(
            AnnexureRegistry(annexure_id=annexure_id)
        )
        annexures.extend(response.results)

    return {
        "answer": answer_text,
        "annexures": [a.model_dump() for a in annexures]
    }