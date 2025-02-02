import pytest
from unittest.mock import patch
from services.hospitacja_service import get_hospitacje_pracownika, get_hospitacja_details, zaakceptuj_hospitacje

@pytest.fixture
def mock_query_db():
    with patch('services.hospitacja_service.query_db') as mock_db:
        yield mock_db

def test_get_hospitacje_pracownika_pending(mock_query_db):
    mock_query_db.return_value = [
        {'id_hospitacji': 1, 'termin': '2025-04-15', 'data_zatwierdzenia': None, 'nazwa': 'Techniki efektywnego programowania'}
    ]

    result = get_hospitacje_pracownika(1)

    assert len(result) == 1
    assert result[0]['id'] == 1
    assert result[0]['termin'] == '2025-04-15'
    assert result[0]['status'] == 'pending'
    assert result[0]['nazwa'] == 'Techniki efektywnego programowania'

def test_get_hospitacje_pracownika_completed(mock_query_db):
    mock_query_db.return_value = [
        {'id_hospitacji': 2, 'termin': '2025-05-10', 'data_zatwierdzenia': '2025-05-15', 'nazwa': 'Algorytmy i Struktury Danych'}
    ]

    result = get_hospitacje_pracownika(1)

    assert len(result) == 1
    assert result[0]['id'] == 2
    assert result[0]['termin'] == '2025-05-10'
    assert result[0]['status'] == 'completed'
    assert result[0]['nazwa'] == 'Algorytmy i Struktury Danych'

def test_get_hospitacje_pracownika_mixed(mock_query_db):
    mock_query_db.return_value = [
        {'id_hospitacji': 1, 'termin': '2025-04-15', 'data_zatwierdzenia': None, 'nazwa': 'Techniki efektywnego programowania'},
        {'id_hospitacji': 2, 'termin': '2025-05-10', 'data_zatwierdzenia': '2025-05-15', 'nazwa': 'Algorytmy i Struktury Danych'}
    ]

    result = get_hospitacje_pracownika(1)

    assert len(result) == 2

    assert result[0]['id'] == 1
    assert result[0]['status'] == 'pending'

    assert result[1]['id'] == 2
    assert result[1]['status'] == 'completed'

def test_get_hospitacje_pracownika_no_hospitacje(mock_query_db):
    mock_query_db.return_value = []

    result = get_hospitacje_pracownika(1)

    assert result == []

def test_get_hospitacja_details_pending(mock_query_db):
    mock_query_db.return_value = {
        'przedmiot_nazwa': 'Techniki efektywnego programowania',
        'przedmiot_kod': 'W041ST-S10018L',
        'termin': '2025-04-15',
        'miejsce': 'Sala 107b, bud. D-2',
        'protokol': 'some protocol',
        'zespol_hospitujacy': 'Jan Kowalski, Anna Nowak',
        'data_zatwierdzenia': None 
    }

    result = get_hospitacja_details(1)

    assert result['przedmiot_nazwa'] == 'Techniki efektywnego programowania'
    assert result['status'] == 'pending'
    assert result['zespol_hospitujacy'] == ['Jan Kowalski', 'Anna Nowak']

def test_get_hospitacja_details_completed(mock_query_db):
    mock_query_db.return_value = {
        'przedmiot_nazwa': 'Techniki efektywnego programowania',
        'przedmiot_kod': 'W041ST-S10018L',
        'termin': '2025-04-15',
        'miejsce': 'Sala 107b, bud. D-2',
        'protokol': 'some protocol',
        'zespol_hospitujacy': 'Jan Kowalski, Anna Nowak',
        'data_zatwierdzenia': '2025-04-20'
    }

    result = get_hospitacja_details(1)

    assert result['przedmiot_nazwa'] == 'Techniki efektywnego programowania'
    assert result['status'] == 'completed'
    assert result['zespol_hospitujacy'] == ['Jan Kowalski', 'Anna Nowak']

def test_get_hospitacja_details_no_team(mock_query_db):
    mock_query_db.return_value = {
        'przedmiot_nazwa': 'Techniki efektywnego programowania',
        'przedmiot_kod': 'W041ST-S10018L',
        'termin': '2025-04-15',
        'miejsce': 'Sala 107b, bud. D-2',
        'protokol': 'some protocol',
        'zespol_hospitujacy': None,
        'data_zatwierdzenia': None
    }

    result = get_hospitacja_details(1)
    print(result)

    assert result['przedmiot_nazwa'] == 'Techniki efektywnego programowania'
    assert result['status'] == 'pending'
    assert result['zespol_hospitujacy'] == []

def test_get_hospitacja_details_not_found(mock_query_db):
    mock_query_db.return_value = None

    result = get_hospitacja_details(999) 

    assert result is None

def test_zaakceptuj_hospitacje_success(mock_query_db):
    mock_query_db.return_value = 1

    result = zaakceptuj_hospitacje(1)

    mock_query_db.assert_called_once_with('''
        UPDATE hospitacje
        SET data_zatwierdzenia = CURRENT_TIMESTAMP
        WHERE id_hospitacji = ?
    ''', (1,))

    assert result == {'message': 'Hospitacja została zaakceptowana'}

def test_zaakceptuj_hospitacje_failure(mock_query_db):
    mock_query_db.return_value = 0

    result = zaakceptuj_hospitacje(999)

    mock_query_db.assert_called_once_with('''
        UPDATE hospitacje
        SET data_zatwierdzenia = CURRENT_TIMESTAMP
        WHERE id_hospitacji = ?
    ''', (999,))

    assert result == {'message': 'Hospitacja nie istnieje lub już zatwierdzona'}