from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_mangas():
    response = client.get("/mangas")
    assert response.status_code == 200
    assert "colecao" in response.json()

def test_bloquear_cadastro_sem_titulo():
    response = client.post("/mangas?titulo=&volume=5&editora=JBC")

    assert response.status_code == 400
    assert response.json()["detail"] == "Dados incompletos"

def test_busca_inexistente():
    response = client.get("/mangas/buscar?termo=NomeQueNaoExiste")
    assert response.status_code == 200
    assert len(response.json()["colecao"]) == 0