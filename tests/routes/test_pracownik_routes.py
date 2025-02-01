import pytest
import json
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_get_pracownik():
    with patch('routes.pracownik_routes.get_pracownik') as mock_service:
        yield mock_service

def test_get_pracownik(mock_get_pracownik, client):
    mock_get_pracownik.return_value = {'imie': 'Jan', 'nazwisko': 'Kowalski'}

    response = client.get('/api/pracownik/1')

    assert response.status_code == 200
    assert 'Jan' in response.get_data(as_text=True)
    assert 'Kowalski' in response.get_data(as_text=True)

def test_get_pracownik_not_found(mock_get_pracownik, client):
    mock_get_pracownik.return_value = None

    response = client.get('/api/pracownik/999')

    assert response.status_code == 404

    data = json.loads(response.get_data(as_text=True))
    assert data["error"] == "Użytkownik nie znaleziony"