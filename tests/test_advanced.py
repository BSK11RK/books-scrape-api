def test_scrape_requires_admin(client):
    client.post("/register", params={"username": "user", "password": "1234"})
    res = client.post(
        "/login",
        data={"username": "user", "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = res.json()["access_token"]

    response = client.post(
        "/scrape",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403

def test_books_pagination(client, admin_token):

    response = client.get(
        "/books?limit=5&offset=0",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert "limit" in response.json()

def test_books_filter(client, admin_token):

    response = client.get(
        "/books?min_price=10&max_price=50",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200