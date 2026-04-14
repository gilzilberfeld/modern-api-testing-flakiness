# Flaky API Tests Demo Project

## Project Purpose
Demo project for Gil Zilberfeld's 60-minute webinar **"Modern API Testing: Fighting Flakiness"**. Each example demonstrates one type of flawed assumption that causes flaky tests.

## Domain
**Bigger Better Bookstore** - a simple bookstore API with books, users, reviews, and orders.

## Tech Stack
- Python 3.10+
- Flask (API server)
- pytest + requests (tests)
- pytest-xdist (parallel test execution for Suspect 3)

## Running the Project
```bash
# Start the server (Terminal 1)
python src/server.py

# Run tests (Terminal 2)
pytest
```

## The Seven Suspects

| # | File | Assumption | Status |
|---|------|------------|--------|
| 1 | `test_01_state_pollution.py` | "The system is clean before my test runs" | TODO |
| 2 | `test_02_order_dependency.py` | "Test A always runs before my test" | TODO |
| 3 | `test_03_concurrency.py` | "My test is the only thing touching the system" | TODO |
| 4 | `test_04_time_locale.py` | "Time and location are fixed" | TODO |
| 5 | `test_05_environment_config.py` | "The environment matches what I expect" | TODO |
| 6 | `test_06_third_party.py` | "External services behave consistently" | TODO |
| 7 | `test_07_ai_indeterminacy.py` | "The AI returns the same answer for the same input" | TODO |

## Key Server Endpoints
- `/reset` - Resets all data to initial state
- `/books`, `/users`, `/reviews`, `/orders` - Standard CRUD
- `/unreliable-payment` - 30% random failure rate (Suspect 6)
- `/ai/recommend` - Returns varied responses (Suspect 7)
- Feature flags via env vars: `FEATURE_PREMIUM_DISCOUNT`, `FEATURE_REVIEW_MODERATION` (Suspect 5)

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
