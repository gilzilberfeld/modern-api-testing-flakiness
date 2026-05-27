import json
import os
import requests
from pathlib import Path

def get_config_path():
    if os.environ.get("CONFIG_PATH"):
        return Path(os.environ["CONFIG_PATH"])

    return Path(__file__).parent.parent.parent / "config" / "server_config.json"

def get_server_url():
    config_path = get_config_path()

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("server_url", "http://localhost:5000")

    return "http://localhost:5000"

def test_get_books_from_configured_server():
    server_url = get_server_url()

    response = requests.get(f"{server_url}/books")
    assert response.status_code == 200

    books = response.json()
    assert len(books) >= 1, "Should have at least one book"

