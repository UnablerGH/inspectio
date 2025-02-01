import pytest
from unittest.mock import patch
from services.hospitacja_service import get_hospitacje_pracownika, get_hospitacja_details, zaakceptuj_hospitacje

# ✅ Patch the correct path
@pytest.fixture
def mock_query_db():
    with patch('services.hospitacja_service.query_db') as mock_db:
        yield mock_db

def test_get_hospitacje_pracownika(mock_query_db):
    # ✅ Ensure the mock is used
    mock_query_db.return_value = [
        {'id_hospitacji': 1, 'termin': '2025-04-15', 'data_zatwierdzenia': None, 'nazwa': 'Techniki efektywnego programowania'}
    ]

    result = get_hospitacje_pracownika(1)

    print("Mocked result:", result)  # Debugging output
    assert len(result) == 1
    assert result[0]['status'] == 'pending'

def test_get_hospitacja_details(mock_query_db):
    mock_query_db.return_value = {
        'przedmiot_nazwa': 'Techniki efektywnego programowania',
        'przedmiot_kod': 'W041ST-S10018L',
        'termin': '2025-04-15',
        'miejsce': 'Sala 107b, bud. D-2',
        'protokol': 'some protocol',
        'zespol_hospitujacy': 'Jan Kowalski, Anna Nowak',
        'data_zatwierdzenia': None,
        'status': 'pending'
    }

    result = get_hospitacja_details(1)
    assert result['przedmiot_nazwa'] == 'Techniki efektywnego programowania'
    assert result['status'] == 'pending'

def test_zaakceptuj_hospitacje(mock_query_db):
    mock_query_db.return_value = None

    result = zaakceptuj_hospitacje(1)
    assert result['message'] == 'Hospitacja została zaakceptowana'