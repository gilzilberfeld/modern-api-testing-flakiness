"""
Data Factory for generating test data with unique identifiers.

Using randomized unique IDs prevents state pollution between test runs.
"""

import random
import string


class DataFactory:
    """Factory for generating unique test data."""

    @staticmethod
    def random_string(length: int = 8) -> str:
        """Generate a random alphanumeric string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @staticmethod
    def unique_book_id() -> str:
        """Generate a unique book ID."""
        return f"book-{DataFactory.random_string()}"

    @staticmethod
    def unique_user_email() -> str:
        """Generate a unique email address."""
        return f"user-{DataFactory.random_string()}@test.com"

    @staticmethod
    def unique_order_ref() -> str:
        """Generate a unique order reference."""
        return f"order-{DataFactory.random_string()}"

    @staticmethod
    def book_data(book_id: str = None, title: str = "Test Book", author: str = "Test Author", price: float = 9.99) -> dict:
        """Generate book data with optional unique ID."""
        return {
            "unique_id": book_id or DataFactory.unique_book_id(),
            "title": title,
            "author": author,
            "price": price
        }
