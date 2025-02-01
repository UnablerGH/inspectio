import pytest
from unittest.mock import patch
from services.pracownik_service import get_pracownik

@pytest.fixture
def mock_query_db():
    with patch('repo.db.query_db') as mock_db:
        yield mock_db

def test_get_pracownik(mock_query_db):
    mock_query_db.return_value = {'imie': 'Jan', 'nazwisko': 'Kowalski'}

    result = get_pracownik(1)
    assert result['imie'] == 'Jan'
    assert result['nazwisko'] == 'Kowalski'