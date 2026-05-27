import json
import requests

CONFIG_PATH = "/etc/bookstore/server_config.json"


def get_server_url():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config["server_url"]


def test_get_books_from_configured_server():
    server_url = get_server_url()

    response = requests.get(f"{server_url}/books")
    assert response.status_code == 200

    books = response.json()
    assert len(books) >= 1, "Should have at least one book"

