def test_register_user(client):
    """Testa o cadastro de um novo usuário com sucesso (Status 201)."""
    response = client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "Password123!",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data  # Garante que a senha pura não é retornada


def test_register_duplicate_username(client):
    """Testa se o sistema bloqueia usernames duplicados (Status 400)."""
    payload = {
        "email": "user1@example.com",
        "username": "sameuser",
        "password": "Password123!",
    }
    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/register",
        json={
            "email": "user2@example.com",
            "username": "sameuser",
            "password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Nome de utilizador já em uso."


def test_login_success(client):
    """Testa a geração do token JWT após autenticação com sucesso (Status 200)."""
    client.post(
        "/auth/register",
        json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "Password123!",
        },
    )

    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_read_users_me_success(client):
    """Testa o acesso à rota protegida /users/me enviando o Bearer Token JWT."""
    # 1. Cadastra o usuário
    client.post(
        "/auth/register",
        json={
            "email": "meuser@example.com",
            "username": "meuser",
            "password": "Password123!",
        },
    )

    # 2. Faz o login para obter o token
    login_res = client.post(
        "/auth/login",
        data={"username": "meuser", "password": "Password123!"},
    )
    token = login_res.json()["access_token"]

    # 3. Acessa a rota protegida com o cabeçalho Authorization
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "meuser@example.com"


def test_read_users_me_unauthorized(client):
    """Testa se a rota protegida bloqueia requisições sem token (Status 401)."""
    response = client.get("/users/me")
    assert response.status_code == 401