"""
SUSPECT 2: Test Order Dependency

THE ASSUMPTION: "Test A always runs before test B."
"""

import requests

from tests.conftest import BASE_URL


BOOK_ID1 = "book-to-create"
BOOK_ID2 = "book-to-delete"


def test_create_book_to_delete():
    book_data = {
        "unique_id": BOOK_ID1,
        "title": "Temporary Book",
        "author": "Some Author",
        "price": 25.99
    }

    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Temporary Book"


def test_delete_book_created_by_previous_test():
    book_data = {
        "unique_id": BOOK_ID2,
        "title": "Temporary Book",
        "author": "Some Author",
        "price": 25.99
    }

    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201

    response = requests.delete(f"{BASE_URL}/books/{BOOK_ID2}")
    assert response.status_code == 204

    # Verify it's gone
    response = requests.get(f"{BASE_URL}/books/{BOOK_ID2}")
    assert response.status_code == 404