def create_api_payload(**overrides):
    payload = {
        "name": "Test API",
        "url": "https://httpbin.org/status/200",
        "method": "GET",
        "expected_status_code": 200,
        "monitoring_interval": 60,
        "timeout": 5,
    }
    payload.update(overrides)
    return payload


def test_create_monitored_api(client, auth_headers):
    response = client.post("/api/monitored-apis", json=create_api_payload(), headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test API"
    assert data["active"] is True


def test_list_monitored_apis_returns_only_owned(client, auth_headers):
    client.post("/api/monitored-apis", json=create_api_payload(), headers=auth_headers)
    response = client.get("/api/monitored-apis", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_nonexistent_api_returns_404(client, auth_headers):
    response = client.get("/api/monitored-apis/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_monitored_api_partial_update(client, auth_headers):
    created = client.post("/api/monitored-apis", json=create_api_payload(), headers=auth_headers).json()
    response = client.put(
        f"/api/monitored-apis/{created['id']}",
        json={"name": "Updated Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["url"] == created["url"]  # unchanged fields preserved


def test_delete_monitored_api(client, auth_headers):
    created = client.post("/api/monitored-apis", json=create_api_payload(), headers=auth_headers).json()
    response = client.delete(f"/api/monitored-apis/{created['id']}", headers=auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/api/monitored-apis/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 404


def test_cannot_access_another_users_api(client, auth_headers):
    created = client.post("/api/monitored-apis", json=create_api_payload(), headers=auth_headers).json()

    other_user = {"name": "Other", "email": "other@example.com", "password": "otherpass123"}
    client.post("/api/auth/register", json=other_user)
    login = client.post("/api/auth/login", json={"email": other_user["email"], "password": other_user["password"]})
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.get(f"/api/monitored-apis/{created['id']}", headers=other_headers)
    assert response.status_code == 403