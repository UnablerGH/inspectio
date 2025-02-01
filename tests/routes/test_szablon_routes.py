import pytest
import json
from unittest.mock import patch, MagicMock
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

def test_post_szablon(mock_save_szablon, client):
    mock_save_szablon.return_value = ("{\"message\": \"Szablon został zapisany pomyślnie\"}", 201)

    response = client.post('/api/szablon', json={"new_key": "new_value"})

    assert response.status_code == 201
    assert 'Szablon został zapisany pomyślnie' in response.get_data(as_text=True)