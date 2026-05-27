import re


def remove_invalid_surrogates(text: str) -> str:
    """
    Remove invalid Unicode surrogate characters.
    These characters can appear when copying emoji or rich text from webpages.
    They cannot be encoded properly in UTF-8.
    """
    if not text:
        return ""

    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def clean_text_for_image(text: str) -> str:
    """
    Clean text before rendering it into image-based assets.

    This function removes emoji and pictographic symbols that may not be
    supported by the default image-rendering font, while keeping normal
    German letters, punctuation, numbers, and whitespace.
    """
    if not text:
        return ""

    text = remove_invalid_surrogates(text)

    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\u2600-\u26FF"
        "\u2700-\u27BF"
        "]+",
        flags=re.UNICODE,
    )

    cleaned = emoji_pattern.sub("", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def shorten_text(text: str, max_chars: int) -> str:
    """
    Shorten text to a maximum number of characters.
    The function tries to cut at a sentence boundary or word boundary.
    """
    if not text:
        return ""

    text = remove_invalid_surrogates(text)
    text = " ".join(text.split())

    if len(text) <= max_chars:
        return text

    shortened = text[:max_chars]

    last_sentence_end = max(
        shortened.rfind("."),
        shortened.rfind("!"),
        shortened.rfind("?")
    )

    if last_sentence_end > max_chars * 0.5:
        return shortened[:last_sentence_end + 1]

    last_space = shortened.rfind(" ")

    if last_space > 0:
        return shortened[:last_space] + " ..."

    return shortened + " ..."