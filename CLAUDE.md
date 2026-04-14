# Flaky API Tests Demo Project

## Project Purpose
Demo project for Gil Zilberfeld's 60-minute webinar **"Modern API Testing: Fighting Flakiness"**. Each example demonstrates one type of flawed assumption that causes flaky tests.

## Domain
**Bigger Better Bookstore** - a simple bookstore API with books, reviews, and orders.

## Tech Stack
- Python 3.10+
- Flask (API server)
- pytest + requests (tests)
- pytest-xdist (parallel test execution for Suspect 3)
- httpx + respx (HTTP client and mocking for Suspect 6)

## Running the Project
```bash
# Start the server (Terminal 1)
python src/server.py

# Run tests (Terminal 2)
pytest
```

## The Seven Suspects

| # | Folder | Assumption | Status |
|---|--------|------------|--------|
| 1 | `C01_State_Polution` | "The system is clean before my test runs" | Done |
| 2 | `C02_Dependency` | "Test A always runs before my test" | Done |
| 3 | `C03_Concurrency` | "My test is the only thing touching the system" | Done |
| 4 | `C04_Time_Locale` | "Time and location are fixed" | Done |
| 5 | `C05_Environment_Config` | "The environment matches what I expect" | Done |
| 6 | `C06_Third_Party` | "External services behave consistently" | Done |
| 7 | `C07_AI_Indeterminacy` | "The AI returns the same answer for the same input" | Done |

## Key Server Endpoints
- `/health` - Health check
- `/reset` - Resets all data to initial state
- `/books` - CRUD for books
- `/books/auto` - Create book with LLM author lookup (Suspect 7)
- `/books/{id}/reviews` - Reviews for a book
- `/orders` - Create orders (calls payment service internally)
- `/orders/today` - Get today's orders (Suspect 4)
- `/unreliable-payment` - 30% random failure rate (Suspect 6)

## Test Requirements
Each test example must:
1. Be a real, runnable API test
2. Clearly demonstrate one specific flawed assumption
3. Show what happens when the assumption breaks
4. Be simple enough to explain in 3-4 minutes

## Workflow
1. Gil specifies which suspect to work on
2. Claude proposes the test code
3. Gil reviews and adjusts
4. Claude implements the agreed version
5. Verify the test demonstrates the flakiness correctly
