import os

import pytest


@pytest.mark.order
@pytest.mark.requires_login
def test_user_order_list_requires_valid_session(user_client):
    response = user_client.get("/getOrderList.do", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)


@pytest.mark.order
def test_user_order_list_without_login_is_blocked(client):
    response = client.get("/getOrderList.do", {"page": 1})

    assert response.status_code in (302, 401, 403, 500)


@pytest.mark.order
def test_venue_order_calendar_returns_json_or_server_error_for_bad_data(client):
    venue_name = os.getenv("MEETHERE_TEST_VENUE_NAME", "武汉洪山场馆")
    response = client.get(
        "/order/getOrderList.do",
        {"venueName": venue_name, "date": "2026-06-09"},
    )

    assert response.status_code in (200, 500)
    if response.status_code == 200:
        body = response.json()
        assert "venue" in body
        assert "orders" in body


@pytest.mark.order
@pytest.mark.destructive
@pytest.mark.requires_login
def test_add_order_redirects_to_order_manage(user_client):
    venue_name = os.getenv("MEETHERE_TEST_VENUE_NAME", "武汉洪山场馆")
    response = user_client.post_form(
        "/addOrder.do",
        {
            "venueName": venue_name,
            "date": "",
            "startTime": "2026-06-10 10:00",
            "hours": 2,
        },
    )

    assert response.status_code in (200, 302)
    assert "order_manage" in response.url or "order_manage" in response.text
