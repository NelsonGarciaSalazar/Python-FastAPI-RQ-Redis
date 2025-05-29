from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Endpoint ficticio que lanza excepción genérica
@app.get("/error/generic")
def raise_generic():
    raise Exception("Something went wrong")

# Endpoint ficticio que lanza HTTPException
from fastapi import HTTPException
@app.get("/error/http")
def raise_http():
    raise HTTPException(status_code=400, detail="Invalid input")

# Endpoint ficticio que lanza error de validación
@app.get("/error/validation")
def raise_validation(a: int):
    return {"a": a}

def test_http_exception():
    response = client.get("/error/http")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input"

