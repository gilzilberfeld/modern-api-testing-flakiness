import requests

from tests.conftest import BASE_URL


def test_create_and_get_book():
    book_id = "book-123"
    book_data = {
        "unique_id": book_id,
        "title": "The Lord Of The Rings: The Fellowship Of The Ring",
        "author": "J. R. R. Tolkien",
        "price": 12.99
    }

    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "The Lord Of The Rings"


    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "The Lord Of The Rings"