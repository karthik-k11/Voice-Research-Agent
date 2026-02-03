import re
from typing import Tuple

# Deterministic source confidence (NO LLM HERE)
SOURCE_CONFIDENCE = {
    "WIKIPEDIA": 0.75,
    "ARXIV": 0.90,
    "WEB": 0.60
}

MIN_CONFIDENCE_THRESHOLD = 0.65


def is_content_valid(text: str) -> bool:
    if not text:
        return False

    lowered = text.lower()
    bad_signals = [
        "error",
        "not found",
        "no results",
        "captcha",
        "rate limit"
    ]

    if any(signal in lowered for signal in bad_signals):
        return False

    # Too short = unreliable
    if len(text.strip()) < 50:
        return False

    return True

##Scores all valid sources and then returns average confidence
def score_sources(research_payload: dict) -> float:
    """
    Scores all valid sources and returns average confidence.
    """
    scores = []

    for source, content in research_payload.items():
        if source not in SOURCE_CONFIDENCE:
            continue

        if is_content_valid(content):
            scores.append(SOURCE_CONFIDENCE[source])

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)


def allow_response(research_payload: dict) -> Tuple[bool, float]:
    confidence = score_sources(research_payload)
    return confidence >= MIN_CONFIDENCE_THRESHOLD, confidence
