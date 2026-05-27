import requests
from unittest.mock import patch

BASE_URL = "http://localhost:5000"


def setup_module():
    requests.post(f"{BASE_URL}/reset")

def test_create_book_with_mocked_llm():
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
    author_lower = author.lower()
    return any(valid in author_lower for valid in VALID_AUTHORS)

def test_create_book_validates_semantic_correctness():
    response = requests.post(f"{BASE_URL}/books/auto", json={
        "unique_id": "design-patterns-semantic",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "price": 59.99
    })
    assert response.status_code == 201

    get_response = requests.get(f"{BASE_URL}/books/design-patterns-semantic")
    assert get_response.status_code == 200

    book = get_response.json()

    assert is_valid_design_patterns_author(book["author"]), \
        f"Author '{book['author']}' doesn't match any valid format"


def calculate_author_score(author):
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
    score = calculate_author_score(author)

    MIN_SCORE = 20
    assert score >= MIN_SCORE, \
        f"Author '{author}' scored {score}, minimum required is {MIN_SCORE}"

