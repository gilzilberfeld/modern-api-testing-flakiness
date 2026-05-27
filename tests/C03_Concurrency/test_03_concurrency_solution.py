import requests
from tests.factories import DataFactory

BASE_URL = "http://localhost:5000"

def test_add_review_isolated():
    # Create a unique book for this test
    book_id = DataFactory.unique_book_id()
    book_data = DataFactory.book_data(book_id=book_id, title="Concurrency Mastery")
    
    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201

    review_data = {
        "rating": 5,
        "comment": "Excellent book on software craftsmanship!"
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    
    assert response.status_code == 201
    assert response.json()["rating"] == 5


def test_count_reviews_incremented_correctly_isolated():
    # Create another unique book
    book_id = DataFactory.unique_book_id()
    book_data = DataFactory.book_data(book_id=book_id, title="Isolated Testing")
    
    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201

    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200

    reviews_before = response.json()
    count_before = len(reviews_before)
    assert count_before == 0

    unique_comment = f"Great practical advice! {DataFactory.random_string()}"
    review_data = {
        "rating": 4,
        "comment": unique_comment
    }
    response = requests.post(f"{BASE_URL}/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 201

    response = requests.get(f"{BASE_URL}/books/{book_id}/reviews")
    assert response.status_code == 200
    reviews_after = response.json()
    count_after = len(reviews_after)

    assert count_after == count_before + 1, f"Expected {count_before + 1}, got {count_after}"
    
    # Double-check: verify our specific review is present
    comments = [r["comment"] for r in reviews_after]
    assert unique_comment in comments
