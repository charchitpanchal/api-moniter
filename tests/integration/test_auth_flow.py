def test_register_creates_user(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "New User", "email": "newuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "password" not in data


def test_register_rejects_duplicate_email(client, registered_user):
    response = client.post("/api/auth/register", json=registered_user)
    assert response.status_code == 400


def test_register_rejects_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "X", "email": "shortpw@example.com", "password": "123"},
    )
    assert response.status_code == 422


def test_login_succeeds_with_correct_credentials(client, registered_user):
    response = client.post(
        "/api/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fails_with_wrong_password(client, registered_user):
    response = client.post(
        "/api/auth/login",
        json={"email": registered_user["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_protected_route_rejects_missing_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_protected_route_accepts_valid_token(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200