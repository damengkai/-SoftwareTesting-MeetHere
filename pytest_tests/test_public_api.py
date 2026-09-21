import pytest


@pytest.mark.smoke
def test_login_page_is_available(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert "html" in response.text.lower()


@pytest.mark.venue
@pytest.mark.smoke
def test_venue_list_api_returns_paged_json(client):
    response = client.get("/venuelist/getVenueList", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert "content" in body
    assert isinstance(body["content"], list)


@pytest.mark.news
@pytest.mark.smoke
def test_news_list_api_returns_paged_json(client):
    response = client.get("/news/getNewsList", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert "content" in body
    assert isinstance(body["content"], list)


@pytest.mark.message
@pytest.mark.smoke
def test_public_message_list_api_returns_array(client):
    response = client.get("/message/getMessageList", {"page": 1})
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)
