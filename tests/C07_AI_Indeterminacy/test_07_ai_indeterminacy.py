"""
SUSPECT 7: AI Indeterminacy

THE ASSUMPTION: "The AI returns the same answer for the same input."

These tests demonstrate flakiness caused by:
1. LLMs returning different phrasings for the same question
2. Non-deterministic responses even with the same prompt
3. Multiple valid answers (e.g., author names can be formatted many ways)

To simulate the flakiness:
- Run the test multiple times - it will randomly fail
- The LLM returns different author formats for "Design Patterns"
"""

import requests

BASE_URL = "http://localhost:5000"


def setup_module():
    """Reset server state before tests."""
    requests.post(f"{BASE_URL}/reset")


# =============================================================================
# TEST: Create book with LLM-provided author and verify exact match
# =============================================================================

def test_create_book_with_llm_author():
    # Create a book - LLM will look up the author
    response = requests.post(f"{BASE_URL}/books/auto", json={
        "unique_id": "design-patterns-test",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "price": 59.99
    })
    assert response.status_code == 201

    get_response = requests.get(f"{BASE_URL}/books/design-patterns-test")
    assert get_response.status_code == 200

    book = get_response.json()

    # FLAKY: Expects exact match, but LLM returns different formats!
    assert book["author"] == "Gang of Four", \
        f"Expected 'Gang of Four' but got '{book['author']}'"
