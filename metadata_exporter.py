import json
from text_utils import remove_invalid_surrogates


def save_metadata(event: dict, output_path: str) -> None:
    """
    Save the structured event metadata as a JSON file.
    This file documents the input data used for asset generation.
    """

    safe_event = {
        key: remove_invalid_surrogates(value) if isinstance(value, str) else value
        for key, value in event.items()
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(safe_event, f, ensure_ascii=False, indent=4)