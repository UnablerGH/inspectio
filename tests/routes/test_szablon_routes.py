import pytest
import json
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_get_szablon():
    with patch('routes.szablon_routes.get_szablon') as mock_service:
        yield mock_service

@pytest.fixture
def mock_save_szablon():
    with patch('routes.szablon_routes.save_szablon') as mock_service:
        yield mock_service

def test_get_szablon(mock_get_szablon, client):
    mock_get_szablon.return_value = {"klucz": "wartość"}

    response = client.get('/api/szablon')

    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data["klucz"] == "wartość"

def test_post_szablon_success(mock_save_szablon, client):
    mock_save_szablon.return_value = ({"message": "Szablon został zapisany pomyślnie"}, 201)

    response = client.post('/api/szablon', json={"new_key": "new_value"})

    assert response.status_code == 201
    data = json.loads(response.get_data(as_text=True))
    assert data["message"] == "Szablon został zapisany pomyślnie"


def test_post_szablon_invalid_data(mock_save_szablon, client):
    mock_save_szablon.return_value = ({"error": "Dane muszą być w formacie JSON"}, 400)

    response = client.post('/api/szablon', json="invalid_data")

    assert response.status_code == 400
    # Assert the error message in the response body
    data = json.loads(response.get_data(as_text=True))
    assert data["error"] == "Dane muszą być w formacie JSON"

def test_post_szablon_internal_server_error(mock_save_szablon, client):
    mock_save_szablon.return_value = ({"error": "Coś poszło nie tak: Some file error"}, 500)

    response = client.post('/api/szablon', json={"new_key": "new_value"})

    assert response.status_code == 500
    data = json.loads(response.get_data(as_text=True))
    assert data["error"] == "Coś poszło nie tak: Some file error"