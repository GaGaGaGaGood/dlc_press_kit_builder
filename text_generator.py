from text_utils import remove_invalid_surrogates


def generate_press_text(event: dict, output_path: str) -> None:
    """
    Generate a short press text / event summary.
    """

    safe_event = {
        key: remove_invalid_surrogates(value) if isinstance(value, str) else value
        for key, value in event.items()
    }

    press_text = f"""Press text / Event summary

Title: {safe_event["title"]}

The Digital Learning Campus offers the learning activity "{safe_event["title"]}" on {safe_event["date"]} at {safe_event["time"]} in {safe_event["location"]}.

Description:
{safe_event["description"]}

Skill level: {safe_event["level"]}
Language: {safe_event["language"]}

More information and registration:
{safe_event["url"]}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(press_text)