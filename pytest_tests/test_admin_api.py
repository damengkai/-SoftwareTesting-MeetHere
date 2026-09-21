import pytest


@pytest.mark.admin
@pytest.mark.requires_login
def test_admin_pending_order_list_returns_array(admin_client):
    response = admin_client.get("/admin/getOrderList.do", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)


@pytest.mark.admin
def test_pending_order_list_without_login_documents_current_permission_risk(client):
    response = client.get("/admin/getOrderList.do", {"page": 1})

    assert response.status_code == 200


@pytest.mark.admin
def test_admin_venue_list_returns_array(client):
    response = client.get("/venueList.do", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)


@pytest.mark.admin
def test_admin_news_list_returns_array(client):
    response = client.get("/newsList.do", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)


@pytest.mark.admin
def test_admin_message_list_returns_array(client):
    response = client.get("/messageList.do", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)
