import requests

from tests.conftest import BASE_URL

SHARED_BOOK_ID = "book-to-delete"

def test_create_book_to_delete():
    # Creates a book
    book_data = {
        "unique_id": SHARED_BOOK_ID,
        "title": "Temporary Book",
        "author": "Some Author",
        "price": 25.99
    }

    response = requests.post(f"{BASE_URL}/books", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Temporary Book"


def test_delete_book_created_by_previous_test():
    # Delete the book created by the previous test
    response = requests.delete(f"{BASE_URL}/books/{SHARED_BOOK_ID}")
    assert response.status_code == 204

    # Verify it's gone
    response = requests.get(f"{BASE_URL}/books/{SHARED_BOOK_ID}")
    assert response.status_code == 404