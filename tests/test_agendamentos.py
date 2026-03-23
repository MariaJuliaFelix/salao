from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_listar_servicos():
    response = client.get("/servicos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_criar_agendamento():
    payload = {
        "cliente_nome": "Maria Julia",
        "servicos": [1, 2],
        "data": "2099-12-20",
        "horario": "10:00",
        "observacao": "Teste"
    }

    response = client.post("/agendamentos/", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["cliente_nome"] == "Maria Julia"
    assert len(body["servicos"]) == 2


def test_impedir_conflito_horario():
    primeiro = {
        "cliente_nome": "Cliente A",
        "servicos": [1],
        "data": "2099-12-21",
        "horario": "10:00"
    }

    segundo = {
        "cliente_nome": "Cliente B",
        "servicos": [4],
        "data": "2099-12-21",
        "horario": "10:20"
    }

    response1 = client.post("/agendamentos/", json=primeiro)
    assert response1.status_code == 200

    response2 = client.post("/agendamentos/", json=segundo)
    assert response2.status_code == 400


def test_historico_periodo():
    response = client.get("/agendamentos/historico?data_inicio=2099-12-01&data_fim=2099-12-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)