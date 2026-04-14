"""
Shared data store for the Bigger Better Bookstore API.
"""

# Books catalog (keyed by unique_id string)
books = {
    "book-1": {"unique_id": "book-1", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "price": 49.99, "stock": 10},
    "book-2": {"unique_id": "book-2", "title": "Clean Code", "author": "Robert Martin", "price": 39.99, "stock": 5},
    "book-3": {"unique_id": "book-3", "title": "Design Patterns", "author": "Gang of Four", "price": 59.99, "stock": 3},
}

# Book reviews
reviews = {}
next_review_id = 1

# Orders
orders = {}
next_order_id = 1

# Initial data for reset
INITIAL_BOOKS = {
    "book-1": {"unique_id": "book-1", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "price": 49.99, "stock": 10},
    "book-2": {"unique_id": "book-2", "title": "Clean Code", "author": "Robert Martin", "price": 39.99, "stock": 5},
    "book-3": {"unique_id": "book-3", "title": "Design Patterns", "author": "Gang of Four", "price": 59.99, "stock": 3},
}
