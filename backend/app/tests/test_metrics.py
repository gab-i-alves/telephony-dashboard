from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.call import Call
from datetime import datetime

def test_read_kpis(client: TestClient, db_session: Session):
    # Cria um usuário e obtém o token para acessar a  rota protegida
    client.post("/users/", json={"email": "kpiuser@example.com", "password": "password"})
    login_response = client.post("/login", data={"username": "kpiuser@example.com", "password": "password"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Adiciona dados de teste ao banco de dados de teste
    call1 = Call(external_id="1", start_time=datetime.now(), duration=120, status_code=200, call_status="OK")
    call2 = Call(external_id="2", start_time=datetime.now(), duration=60, status_code=200, call_status="OK")
    call3 = Call(external_id="3", start_time=datetime.now(), duration=30, status_code=486, call_status="BUSY")
    db_session.add_all([call1, call2, call3])
    db_session.commit()

    # Faz a chamada a API
    response = client.get("/metrics/kpis", headers=headers)
    assert response.status_code == 200
    kpis = response.json()

    assert kpis["total_calls"] == 3
    assert kpis["answered_calls"] == 2
    assert kpis["asr"] == round(2 / 3 * 100, 2)
    assert kpis["acd"] == round((120 + 60) / 2, 2)