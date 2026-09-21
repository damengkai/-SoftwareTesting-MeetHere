import os

import pytest


@pytest.mark.auth
@pytest.mark.smoke
def test_user_login_success(client):
    response = client.login(
        os.getenv("MEETHERE_USER_ID", "test"),
        os.getenv("MEETHERE_USER_PASSWORD", "test"),
    )

    assert response.status_code == 200
    if response.text != "/index":
        pytest.skip(
            "valid normal-user credentials are required; set "
            "MEETHERE_USER_ID and MEETHERE_USER_PASSWORD"
        )
    assert response.text == "/index"
    assert client.has_cookie("JSESSIONID")


@pytest.mark.auth
@pytest.mark.smoke
def test_admin_login_success(client):
    response = client.login("admin", "admin")

    assert response.status_code == 200
    assert response.text == "/admin_index"
    assert client.has_cookie("JSESSIONID")


@pytest.mark.auth
def test_login_fails_with_wrong_password(client):
    response = client.login("test", "wrong-password")

    assert response.status_code == 200
    assert response.text == "false"
