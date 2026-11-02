# tests/test_auth.py
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Testa o registo bem-sucedido de um novo utilizador."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_user(client: TestClient):
    """Testa o login e a obtenção do token JWT."""
    # Regista primeiro o utilizador
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "securepassword123"
        }
    )

    # Tenta fazer login enviando dados no formato de formulário (application/x-www-form-urlencoded)
    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_users_me_success(client: TestClient):
    """Testa o acesso à rota protegida /users/me com um token válido."""
    # Regista e faz login para obter o token
    client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "securepassword123"
        }
    )
    login_response = client.post(
        "/auth/login",
        data={
            "username": "meuser",
            "password": "securepassword123"
        }
    )
    token = login_response.json()["access_token"]

    # Acede à rota protegida enviando o cabeçalho Authorization Bearer
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"


def test_get_users_me_unauthorized_no_token(client: TestClient):
    """Testa o acesso à rota /users/me sem enviar nenhum token."""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_users_me_invalid_token(client: TestClient):
    """Testa o acesso à rota /users/me enviando um token inválido/corrompido."""
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer token_falsificado_ou_invalido"}
    )
    assert response.status_code == 401