"""
SUSPECT 3: Concurrency (SOLUTION)

THE FIX: 
1. Resource Isolation: Each test creates its own unique book rather than sharing 'book-1'.
Use the DataFactory to generate unique book IDs for each test.
"""

import requests
from tests.factories import DataFactory

BASE_URL = "http://localhost:5000"


def test_add_review_isolated():
    """
    FIX 1: Create a unique book for this test to ensure isolation from other concurrent tests.
    """
    # 1. Arrange: Create a unique book for this test
    book_id = DataFactory.unique_book_id()
    book_data = DataFactory.book_data(book_id=book_id, title="Concurrency Mastery")
    
    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201

    # 2. Act: Add a review
    review_data = {
        "rating": 5,
        "comment": "Excellent book on software craftsmanship!"
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    
    # 3. Assert: Verify the response
    assert response.status_code == 201
    assert response.json()["rating"] == 5


def test_count_reviews_incremented_correctly_isolated():
    """
    FIX 2: By using a unique book, this count check is now thread-safe.
    Even if other tests are adding reviews to other books, they won't affect this one.
    """
    # 1. Arrange: Create a unique book
    book_id = DataFactory.unique_book_id()
    book_data = DataFactory.book_data(book_id=book_id, title="Isolated Testing")
    
    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201

    # Verify initial count is 0
    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200
    reviews_before = response.json()
    count_before = len(reviews_before)
    assert count_before == 0

    # 2. Act: Add a review
    unique_comment = f"Great practical advice! {DataFactory.random_string()}"
    review_data = {
        "rating": 4,
        "comment": unique_comment
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 201

    # 3. Assert: Verify count incremented correctly
    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200
    reviews_after = response.json()
    count_after = len(reviews_after)

    assert count_after == count_before + 1, f"Expected {count_before + 1}, got {count_after}"
    
    # Double-check: verify our specific review is present
    comments = [r["comment"] for r in reviews_after]
    assert unique_comment in comments
