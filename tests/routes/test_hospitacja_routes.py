import pytest
import json
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_get_hospitacje_pracownika():
    with patch('routes.hospitacja_routes.get_hospitacje_pracownika') as mock_service:
        yield mock_service

@pytest.fixture
def mock_get_hospitacja_details():
    with patch('routes.hospitacja_routes.get_hospitacja_details') as mock_service:
        yield mock_service

@pytest.fixture
def mock_zaakceptuj_hospitacje():
    with patch('routes.hospitacja_routes.zaakceptuj_hospitacje') as mock_service:
        yield mock_service

def test_get_hospitacje(mock_get_hospitacje_pracownika, client):
    mock_get_hospitacje_pracownika.return_value = [{'id': 1, 'termin': '2025-02-01', 'status': 'completed', 'nazwa': 'Matematyka'}]
    
    response = client.get('/api/hospitacje/1')
    
    assert response.status_code == 200
    assert 'Matematyka' in response.get_data(as_text=True)

def test_get_hospitacja_details(mock_get_hospitacja_details, client):
    mock_get_hospitacja_details.return_value = {
        'przedmiot_nazwa': 'Algorytmy',
        'status': 'pending'
    }

    response = client.get('/api/hospitacja/1')

    assert response.status_code == 200
    assert 'Algorytmy' in response.get_data(as_text=True)

def test_get_hospitacja_details_not_found(mock_get_hospitacja_details, client):
    mock_get_hospitacja_details.return_value = None

    response = client.get('/api/hospitacja/999')

    assert response.status_code == 404
    assert 'Hospitacja not found' in response.get_data(as_text=True)

def test_zaakceptuj_hospitacje(mock_zaakceptuj_hospitacje, client):
    mock_zaakceptuj_hospitacje.return_value = {'message': 'Hospitacja została zaakceptowana'}

    response = client.post('/api/hospitacja/1/zaakceptuj')

    assert response.status_code == 200

    data = json.loads(response.get_data(as_text=True))
    assert data["message"] == "Hospitacja została zaakceptowana"