import sys
import os

# Adiciona diretório raiz ao path para imports funcionarem
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_text():
    print("Testing /api/process with productive text...")
    # Exemplo produtivo NÃO presente no dataset de treino
    response = client.post(
        "/api/process",
        data={"text": "Bom dia, segue comprovante de transferência referente à parcela de janeiro."}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"Result: {data}")
    assert "category" in data
    assert "confidence" in data
    assert "suggested_reply" in data
    assert "reply_source" in data
    assert data["category"] == "Produtivo"

def test_process_spam():
    print("\nTesting /api/process with spam text...")
    # Exemplo improdutivo NÃO presente no dataset de treino
    response = client.post(
        "/api/process",
        data={"text": "Parabéns, você foi o visitante 1.000.000! Clique para resgatar seu prêmio agora."}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"Result: {data}")
    assert data["category"] == "Improdutivo"

def test_feedback():
    print("\nTesting /api/feedback...")
    response = client.post(
        "/api/feedback",
        json={
            "text": "Teste feedback",
            "predicted": "Improdutivo",
            "correct": "Produtivo"
        }
    )
    assert response.status_code == 200
    print(f"Result: {response.json()}")

if __name__ == "__main__":
    try:
        test_process_text()
        test_process_spam()
        test_feedback()
        print("\n✅ Todos os testes passaram!")
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        exit(1)
