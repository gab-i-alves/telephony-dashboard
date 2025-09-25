from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_login_for_access_token(client: TestClient):
    # Cria usuário
    client.post(
        "/users/",
        json={"email": "testlogin@example.com", "password": "testpassword"},
    )
    
    # Teste de login com sucesso
    response = client.post(
        "/login",
        data={"username": "testlogin@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

    # Teste de login com senha errada
    response = client.post(
        "/login",
        data={"username": "testlogin@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

def test_read_users_me_protected(client: TestClient):
    # Tenta aceesar sem token
    response = client.get("/users/me")
    assert response.status_code == 401

    # Cria usuário e faz login para obter o token
    client.post("/users/", json={"email": "me@example.com", "password": "password"})
    login_response = client.post("/login", data={"username": "me@example.com", "password": "password"})
    token = login_response.json()["access_token"]

    # Acessa com o token
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"