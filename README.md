# Bigger Better Bookstore - Flaky API Tests Demo

A demonstration project for the webinar **"Modern API Testing: Fighting Flakiness"**.

This project contains examples of seven types of flawed assumptions that cause flaky tests, each demonstrated with a real, runnable API test against a simple bookstore API.

## The Seven Suspects

| # | Suspect | The Flawed Assumption |
|---|---------|----------------------|
| 1 | State Pollution | "The system is clean before my test runs" |
| 2 | Test Order Dependency | "Test A always runs before my test" |
| 3 | Concurrency | "My test is the only thing touching the system" |
| 4 | Time & Locale | "Time and location are fixed" |
| 5 | Environment & Configuration | "The environment matches what I expect" |
| 6 | Third-Party Dependencies | "External services behave consistently" |
| 7 | AI Response Indeterminacy | "The AI returns the same answer for the same input" |

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

Start the Bigger Better Bookstore API:

```bash
python src/server.py
```

The server runs on http://localhost:5000 by default.

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /config | Feature flags |
| POST | /reset | Reset all data |
| GET | /books | List all books |
| POST | /books | Create a book |
| GET | /books/{id} | Get a book |
| DELETE | /books/{id} | Delete a book |
| GET | /books/count | Count books |
| GET | /users | List users |
| POST | /users | Create a user |
| GET | /users/{id} | Get a user |
| DELETE | /users/{id} | Delete a user |
| GET | /books/{id}/reviews | List reviews |
| POST | /books/{id}/reviews | Create a review |
| GET | /orders | List orders |
| POST | /orders | Create an order |
| GET | /orders/today | List today's orders |
| GET | /slow-search | Simulated slow endpoint |
| POST | /unreliable-payment | Simulated flaky payment |
| POST | /ai/recommend | Simulated AI endpoint |

## Running the Tests

```bash
# Run all tests
pytest

# Run a specific suspect's tests
pytest tests/test_01_state_pollution.py

# Run tests in parallel (to demonstrate concurrency issues)
pytest -n 4 tests/test_03_concurrency.py
```

## Project Structure

```
flaky-api-tests/
├── requirements.txt
├── README.md
├── pytest.ini
├── src/
│   └── server.py              # Flask API server
├── tests/
│   ├── conftest.py            # Shared fixtures
│   ├── test_01_state_pollution.py
│   ├── test_02_order_dependency.py
│   ├── test_03_concurrency.py
│   ├── test_04_time_locale.py
│   ├── test_05_environment_config.py
│   ├── test_06_third_party.py
│   └── test_07_ai_indeterminacy.py
└── utils/
    └── api_client.py          # API client helper
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | Server port | 5000 |
| FEATURE_PREMIUM_DISCOUNT | Enable premium user discounts | false |
| FEATURE_REVIEW_MODERATION | Enable review moderation | false |

## License

Demo code for educational purposes.
