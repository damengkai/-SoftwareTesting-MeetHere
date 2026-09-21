import pytest

from api_auto_framework.core.config import Settings, load_settings
from api_auto_framework.core.http_client import HttpClient


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def service_available(settings: Settings) -> None:
    client = HttpClient(settings.base_url, timeout=settings.timeout)
    response = client.get("/login")
    client.close()
    if response.status_code == 0:
        pytest.skip(f"MeetHere service is not reachable: {response.error}")


@pytest.fixture
def anonymous_client(
    settings: Settings, service_available: None
):
    client = HttpClient(settings.base_url, timeout=settings.timeout)
    yield client
    client.close()


@pytest.fixture(scope="session")
def user_client(settings: Settings, service_available: None):
    client = _create_logged_in_client(
        settings,
        settings.user_id,
        settings.user_password,
        expected_text="/index",
        role_name="normal user",
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def admin_client(settings: Settings, service_available: None):
    client = _create_logged_in_client(
        settings,
        settings.admin_id,
        settings.admin_password,
        expected_text="/admin_index",
        role_name="admin",
    )
    yield client
    client.close()


def _create_logged_in_client(
    settings: Settings,
    user_id: str,
    password: str,
    *,
    expected_text: str,
    role_name: str,
) -> HttpClient:
    client = HttpClient(settings.base_url, timeout=settings.timeout)
    response = client.login(user_id, password)
    if response.status_code != 200 or response.text.strip() != expected_text:
        client.close()
        pytest.skip(f"Valid {role_name} credentials are required")
    if not client.has_cookie("JSESSIONID"):
        client.close()
        pytest.skip(f"{role_name} login did not create JSESSIONID")
    return client
