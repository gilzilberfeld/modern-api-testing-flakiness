"""
SUSPECT 3: Concurrency

THE ASSUMPTION: "The tests run in sequence."

"""

import requests

BASE_URL = "http://localhost:5000"


def test_add_review():
    """Gets a book by ID and adds a review to it."""
    book_id = "book-1"

    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200

    review_data = {
        "rating": 5,
        "comment": "Excellent book on software craftsmanship!"
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 201
    assert response.json()["rating"] == 5


def test_count_reviews_incremented_correctly():
    """Gets review count, adds a review, verifies count incremented by exactly 1."""
    book_id = "book-1"

    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200
    count_before = len(response.json())

    review_data = {
        "rating": 4,
        "comment": "Great practical advice!"
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 201

    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200
    count_after = len(response.json())

    assert count_after == count_before + 1, f"Expected {count_before + 1}, got {count_after}"
