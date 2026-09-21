# MeetHere pytest automation

This directory contains Python pytest API tests for the MeetHere venue booking
project.

## Run

Start the Spring Boot app first, then run:

```powershell
pytest
```

Run only smoke tests:

```powershell
pytest -m smoke
```

Run data-changing tests:

```powershell
pytest --run-destructive
```

## Environment variables

The default local server is `http://localhost:8888`.

You can override test settings:

```powershell
$env:MEETHERE_BASE_URL='http://localhost:8888'
$env:MEETHERE_USER_ID='test'
$env:MEETHERE_USER_PASSWORD='test'
$env:MEETHERE_ADMIN_ID='admin'
$env:MEETHERE_ADMIN_PASSWORD='admin'
$env:MEETHERE_TEST_VENUE_NAME='武汉洪山场馆'
```

## Structure

- `utils/api_client.py`: small HTTP client with cookie support.
- `conftest.py`: pytest fixtures for anonymous, user, and admin sessions.
- `test_auth.py`: login and session tests.
- `test_public_api.py`: public page/API smoke tests.
- `test_order_api.py`: user order tests.
- `test_admin_api.py`: admin API tests and permission-risk checks.
- `test_message_news_api.py`: message and news tests.
