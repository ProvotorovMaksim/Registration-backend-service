from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Status": "Healthy"}

def test_register_user():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"Status": "User registered"}

def test_login_user():
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert response.json() == {"Status": "User logged in"}
