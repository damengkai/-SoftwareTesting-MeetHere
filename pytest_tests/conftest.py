import os

import pytest

from pytest_tests.utils.api_client import ApiClient


def pytest_addoption(parser):
    parser.addoption(
        "--run-destructive",
        action="store_true",
        default=False,
        help="run tests that create, update, delete, or approve data",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-destructive"):
        return
    skip_destructive = pytest.mark.skip(
        reason="need --run-destructive option to run data-changing tests"
    )
    for item in items:
        if "destructive" in item.keywords:
            item.add_marker(skip_destructive)


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("MEETHERE_BASE_URL", "http://localhost:8888")


@pytest.fixture()
def client(base_url):
    return ApiClient(base_url)


@pytest.fixture()
def user_client(base_url):
    api = ApiClient(base_url)
    user_id = os.getenv("MEETHERE_USER_ID", "test")
    password = os.getenv("MEETHERE_USER_PASSWORD", "test")
    response = api.login(user_id, password)
    assert response.status_code == 200
    if response.text != "/index":
        pytest.skip(
            "valid normal-user credentials are required; set "
            "MEETHERE_USER_ID and MEETHERE_USER_PASSWORD"
        )
    if not api.has_cookie("JSESSIONID"):
        pytest.skip("normal-user login did not create JSESSIONID")
    return api


@pytest.fixture()
def admin_client(base_url):
    api = ApiClient(base_url)
    user_id = os.getenv("MEETHERE_ADMIN_ID", "admin")
    password = os.getenv("MEETHERE_ADMIN_PASSWORD", "admin")
    response = api.login(user_id, password)
    assert response.status_code == 200
    assert response.text == "/admin_index"
    assert api.has_cookie("JSESSIONID")
    return api
