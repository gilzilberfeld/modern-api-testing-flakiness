"""
Bigger Better Bookstore - API Client

A simple wrapper for making API calls to the bookstore.
Used by tests to interact with the server.
"""

import requests
from typing import Optional


class BookstoreClient:
    """Client for interacting with the Bigger Better Bookstore API."""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    # -------------------------------------------------------------------------
    # Health & Config
    # -------------------------------------------------------------------------

    def health(self) -> dict:
        return self.session.get(f"{self.base_url}/health").json()

    def config(self) -> dict:
        return self.session.get(f"{self.base_url}/config").json()

    def reset(self) -> dict:
        return self.session.post(f"{self.base_url}/reset").json()

    # -------------------------------------------------------------------------
    # Books
    # -------------------------------------------------------------------------

    def list_books(self) -> list:
        return self.session.get(f"{self.base_url}/books").json()

    def get_book(self, book_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/books/{book_id}")

    def create_book(self, unique_id: str, title: str, author: str = "Unknown",
                    price: float = 0.0, stock: int = 0) -> requests.Response:
        data = {"unique_id": unique_id, "title": title, "author": author, "price": price, "stock": stock}
        return self.session.post(f"{self.base_url}/books", json=data)

    def delete_book(self, book_id: str) -> requests.Response:
        return self.session.delete(f"{self.base_url}/books/{book_id}")

    def count_books(self) -> int:
        return self.session.get(f"{self.base_url}/books/count").json()["count"]

    # -------------------------------------------------------------------------
    # Users
    # -------------------------------------------------------------------------

    def list_users(self) -> list:
        return self.session.get(f"{self.base_url}/users").json()

    def get_user(self, user_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/users/{user_id}")

    def create_user(self, email: str, name: str = "",
                    is_premium: bool = False) -> requests.Response:
        data = {"email": email, "name": name, "is_premium": is_premium}
        return self.session.post(f"{self.base_url}/users", json=data)

    def delete_user(self, user_id: int) -> requests.Response:
        return self.session.delete(f"{self.base_url}/users/{user_id}")

    # -------------------------------------------------------------------------
    # Reviews
    # -------------------------------------------------------------------------

    def list_reviews(self, book_id: str) -> list:
        return self.session.get(f"{self.base_url}/books/{book_id}/reviews").json()

    def create_review(self, book_id: str, rating: int,
                      comment: str = "", user_id: Optional[int] = None) -> requests.Response:
        data = {"rating": rating, "comment": comment}
        if user_id:
            data["user_id"] = user_id
        return self.session.post(f"{self.base_url}/books/{book_id}/reviews", json=data)

    # -------------------------------------------------------------------------
    # Orders
    # -------------------------------------------------------------------------

    def list_orders(self) -> list:
        return self.session.get(f"{self.base_url}/orders").json()

    def create_order(self, book_id: str, user_id: int) -> requests.Response:
        data = {"book_id": book_id, "user_id": user_id}
        return self.session.post(f"{self.base_url}/orders", json=data)

    def list_todays_orders(self) -> list:
        return self.session.get(f"{self.base_url}/orders/today").json()

    # -------------------------------------------------------------------------
    # Special Endpoints
    # -------------------------------------------------------------------------

    def slow_search(self, delay: float = 0.5) -> requests.Response:
        return self.session.get(f"{self.base_url}/slow-search", params={"delay": delay})

    def unreliable_payment(self, amount: float = 0.0) -> requests.Response:
        return self.session.post(f"{self.base_url}/unreliable-payment", json={"amount": amount})

    def ai_recommend(self, genre: str = "fiction") -> requests.Response:
        return self.session.post(f"{self.base_url}/ai/recommend", json={"genre": genre})
