# tests/test_filesearch_api.py
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def test_filesearch_unauthorized():
    """Garante que as rotas do filesearch exigem autenticação (JWT)."""
    response = client.get("/filesearch/search")
    assert response.status_code == 401

    response = client.post("/filesearch/scan", json={"path": "."})
    assert response.status_code == 401


def test_filesearch_invalid_path_authenticated():
    """Testa se a rota de scan barra caminhos inválidos mesmo com usuário autenticado."""
    user_data = {"email": "filesearch_test@example.com", "username": "fs_user", "password": "securepassword123"}
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", data={"username": "fs_user", "password": "securepassword123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/filesearch/scan",
        json={"path": "./pasta_que_nao_existe_12345"},
        headers=headers
    )

    assert response.status_code == 400
    assert "não existe ou não é uma pasta válida" in response.json()["detail"]


def test_filesearch_scan_and_search_success(tmp_path):
    """Testa o fluxo completo de sucesso: varredura (scan) de uma pasta temporária com imagem e busca (search)."""
    img_path = tmp_path / "foto_teste.jpg"
    img = Image.new('RGB', (100, 100), color='red')
    img.save(img_path)

    user_data = {"email": "positive_test@example.com", "username": "pos_user", "password": "securepassword123"}
    client.post("/auth/register", json=user_data)

    login_response = client.post("/auth/login", data={"username": "pos_user", "password": "securepassword123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    scan_response = client.post(
        "/filesearch/scan",
        json={"path": str(tmp_path)},
        headers=headers
    )
    assert scan_response.status_code == 200
    data = scan_response.json()
    assert data["files_changed"] >= 1

    search_response = client.get(
        "/filesearch/search?q=foto_teste",
        headers=headers
    )
    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results) >= 1
    assert results[0]["filename"] == "foto_teste.jpg"