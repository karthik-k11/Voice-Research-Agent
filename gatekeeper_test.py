from app.agents.gatekeeper import (
    is_content_valid,
    score_sources,
    allow_response
)

def test_valid_content():
    text = "Python is a programming language created by Guido van Rossum."
    assert is_content_valid(text) is True


def test_invalid_content_short():
    text = "Too short"
    assert is_content_valid(text) is False


def test_invalid_content_error():
    text = "Wikipedia error: page not found"
    assert is_content_valid(text) is False


def test_score_sources_all_valid():
    research_payload = {
        "WIKIPEDIA": (
            "Python is a high-level, interpreted programming language widely used "
            "for web development, data science, and automation."
        ),
        "ARXIV": (
            "This paper explores deep learning methods and evaluates neural network "
            "performance across multiple benchmark datasets."
        ),
        "WEB": (
            "Python is widely used in industry for building scalable backend systems "
            "and machine learning pipelines."
        )
    }

    score = score_sources(research_payload)
    assert score >= 0.65

def test_score_sources_none_valid():
    research_payload = {
        "WIKIPEDIA": "Error not found",
        "WEB": "",
        "ARXIV": "No results found"
    }

    score = score_sources(research_payload)
    assert score == 0.0


def test_allow_response_pass():
    research_payload = {
        "WIKIPEDIA": (
            "Python is a high-level, interpreted programming language known for its "
            "readability and broad library support. It is widely used in web development, "
            "data science, automation, and artificial intelligence."
        ),
        "WEB": (
            "Python is used in AI and data science for building intelligent systems "
            "and scalable backend services."
        )
    }

    allowed, confidence = allow_response(research_payload)
    assert allowed is True
    assert confidence >= 0.65

def test_allow_response_block():
    research_payload = {
        "WIKIPEDIA": "Error not found",
        "WEB": "No results found"
    }

    allowed, confidence = allow_response(research_payload)
    assert allowed is False
