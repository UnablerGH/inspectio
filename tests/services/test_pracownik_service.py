import pytest
from unittest.mock import patch
from services.pracownik_service import get_pracownik

@pytest.fixture
def mock_query_db():
    with patch('services.pracownik_service.query_db') as mock_db:
        yield mock_db

def test_get_pracownik_found(mock_query_db):
    mock_query_db.return_value = {"imie": "Jan", "nazwisko": "Kowalski"}

    result = get_pracownik(1)

    mock_query_db.assert_called_once_with('''
        SELECT p.imie, p.nazwisko 
        FROM pracownicy p
        WHERE p.id_pracownika = ?
    ''', (1,), one=True)

    assert result == {"imie": "Jan", "nazwisko": "Kowalski"}

def test_get_pracownik_not_found(mock_query_db):
    mock_query_db.return_value = None

    result = get_pracownik(999)

    mock_query_db.assert_called_once_with('''
        SELECT p.imie, p.nazwisko 
        FROM pracownicy p
        WHERE p.id_pracownika = ?
    ''', (999,), one=True)

    assert result is None