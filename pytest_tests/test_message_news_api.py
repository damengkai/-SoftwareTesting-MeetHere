import time

import pytest


@pytest.mark.message
@pytest.mark.requires_login
def test_my_message_list_requires_valid_session(user_client):
    response = user_client.get("/message/findUserList", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)


@pytest.mark.message
def test_my_message_list_without_login_is_blocked(client):
    response = client.get("/message/findUserList", {"page": 1})

    assert response.status_code in (302, 401, 403, 500)


@pytest.mark.message
@pytest.mark.destructive
def test_send_message_redirects_to_message_list(client):
    response = client.post_form(
        "/sendMessage",
        {
            "userID": "test",
            "content": f"pytest message {int(time.time())}",
        },
    )

    assert response.status_code in (200, 302)
    assert "message_list" in response.url or "message_list" in response.text


@pytest.mark.news
@pytest.mark.destructive
def test_add_news_redirects_to_news_manage(admin_client):
    response = admin_client.post_form(
        "/addNews.do",
        {
            "title": f"pytest news {int(time.time())}",
            "content": "created by pytest automation",
        },
    )

    assert response.status_code in (200, 302)
    assert "news_manage" in response.url or "news_manage" in response.text
