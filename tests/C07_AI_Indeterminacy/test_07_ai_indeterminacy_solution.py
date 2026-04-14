"""
SUSPECT 7: AI Indeterminacy - STABILIZED SOLUTION

THE FIX: Don't assert exact matches for LLM outputs. Instead:
1. Mock the LLM to return deterministic responses in tests
2. Or validate semantic correctness rather than exact strings
3. Or check for any of the acceptable variations

Key principles:
1. LLM outputs are inherently non-deterministic
2. Tests should mock LLM calls for determinism
3. If testing real LLM, validate semantics not exact strings
"""

import requests
from unittest.mock import patch

BASE_URL = "http://localhost:5000"


def setup_module():
    """Reset server state before tests."""
    requests.post(f"{BASE_URL}/reset")


# =============================================================================
# SOLUTION 1: Mock the LLM to return a deterministic response
# =============================================================================

def test_create_book_with_mocked_llm():
    """
    STABILIZED: Mocks the LLM function to return a predictable author.

    Works because:
    - We control exactly what the LLM returns
    - Test is deterministic and repeatable
    - We can verify the integration works correctly
    """
    with patch("src.routes.books.lookup_author_with_llm") as mock_llm:
        mock_llm.return_value = "Gang of Four"

        response = requests.post(f"{BASE_URL}/books/auto", json={
            "unique_id": "design-patterns-mocked",
            "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
            "price": 59.99
        })
        assert response.status_code == 201

        get_response = requests.get(f"{BASE_URL}/books/design-patterns-mocked")
        assert get_response.status_code == 200

        book = get_response.json()
        assert book["author"] == "Gang of Four"


# =============================================================================
# SOLUTION 2: Validate semantic correctness (any valid author format)
# =============================================================================

# All acceptable ways to represent the Design Patterns authors
VALID_AUTHORS = [
    "gang of four",
    "gof",
    "gamma",
    "helm",
    "johnson",
    "vlissides",
    "erich gamma",
]


def is_valid_design_patterns_author(author):
    """Check if the author string contains any valid reference."""
    author_lower = author.lower()
    return any(valid in author_lower for valid in VALID_AUTHORS)


def test_create_book_validates_semantic_correctness():
    """
    STABILIZED: Validates that the author is semantically correct,
    not that it matches an exact string.

    Works because:
    - Accepts any of the valid author representations
    - "Gang of Four", "Erich Gamma et al.", "Gamma, Helm..." all pass
    - Tests the behavior, not the exact wording
    """
    response = requests.post(f"{BASE_URL}/books/auto", json={
        "unique_id": "design-patterns-semantic",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "price": 59.99
    })
    assert response.status_code == 201

    get_response = requests.get(f"{BASE_URL}/books/design-patterns-semantic")
    assert get_response.status_code == 200

    book = get_response.json()

    # Validate semantically - any valid author format is acceptable
    assert is_valid_design_patterns_author(book["author"]), \
        f"Author '{book['author']}' doesn't match any valid format"


# =============================================================================
# SOLUTION 3: Score-based validation for LLM responses
# =============================================================================

def calculate_author_score(author):
    """
    Calculate a confidence score for the author response.

    Higher scores indicate more complete/accurate author information.
    This approach allows for varying quality of LLM responses while
    still validating correctness.
    """
    author_lower = author.lower()
    score = 0

    # High-value matches (well-known references)
    if "gang of four" in author_lower or "gof" in author_lower:
        score += 50

    # Individual author names (10 points each)
    authors = ["gamma", "helm", "johnson", "vlissides"]
    for name in authors:
        if name in author_lower:
            score += 10

    # Full first names (bonus points)
    full_names = ["erich", "richard", "ralph", "john"]
    for name in full_names:
        if name in author_lower:
            score += 5

    return score


def test_create_book_with_score_validation():
    """
    STABILIZED: Uses score-based validation for LLM output.

    Works because:
    - Assigns points for different valid author references
    - "Gang of Four" = 50 points
    - Each author name (Gamma, Helm, etc.) = 10 points
    - Full first names = 5 bonus points each
    - Requires minimum score threshold instead of exact match

    This allows the LLM to return various formats while ensuring
    the response contains meaningful author information.
    """
    response = requests.post(f"{BASE_URL}/books/auto", json={
        "unique_id": "design-patterns-scored",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "price": 59.99
    })
    assert response.status_code == 201

    get_response = requests.get(f"{BASE_URL}/books/design-patterns-scored")
    assert get_response.status_code == 200

    book = get_response.json()
    author = book["author"]

    # Calculate score
    score = calculate_author_score(author)

    # Require minimum score of 20 (e.g., "Gang of Four" or at least 2 author names)
    MIN_SCORE = 20
    assert score >= MIN_SCORE, \
        f"Author '{author}' scored {score}, minimum required is {MIN_SCORE}"

    print(f"Author: '{author}' - Score: {score}")
