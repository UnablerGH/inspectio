from unittest.mock import mock_open, patch
from services.szablon_service import get_szablon, save_szablon
import json

mock_json_data = [
    {
        "info": [
            {"odpowiedz": "", "pytanie": "Prowadzący zajęcia jednostka organizacyjna:"},
            {"odpowiedz": "", "pytanie": "Kod przedmiotu:"},
            {"odpowiedz": "", "pytanie": "Sposób realizacji (tradycyjny, zdalny):"}
        ],
        "nazwa": "Informacje wstępne",
        "opis": ""
    },
    {
        "info": [
            {"odpowiedz": "", "pytanie": "Czy zajęcia zaczęły się punktualnie (tak, nie, ile spóźnienia):"},
            {"odpowiedz": "", "pytanie": "Czy sprawdzono obecność studentów. Jeżeli tak podać liczbę obecnych:"},
            {"odpowiedz": "", "pytanie": "Czy sala i jej wyposażenie są przystosowane do formy prowadzonych zajęć. Jeżeli nie to z jakich powodów:"}
        ],
        "nazwa": "Ocena formalna zajęć",
        "opis": ""
    },
    {
        "info": [{"odpowiedz": "", "pytanie": "Fajność"}],
        "nazwa": "Ocena merytoryczna i metodyczna przeprowadzonych zajęć",
        "opis": "5,5 - wzorowa, 5 - bardzo dobra, 4 - dobra, 3 - dostateczna, 2 - negatywna, 0 - nie dotyczy"
    }
]

def test_get_szablon():
    mock_json_data_str = json.dumps(mock_json_data, ensure_ascii=False, indent=4)

    with patch("builtins.open", mock_open(read_data=mock_json_data_str)):
        result = get_szablon()

        assert result == mock_json_data

def test_save_szablon_success():
    mock_data = mock_json_data

    with patch("builtins.open", mock_open()) as mock_file, patch("json.dump") as mock_json_dump:
        mock_json_dump.return_value = None

        response = save_szablon(mock_data)

        mock_json_dump.assert_called_once_with(mock_data, mock_file(), ensure_ascii=False, indent=4)

        assert response[0] == {"message": "Szablon został zapisany pomyślnie"}
        assert response[1] == 201

def test_save_szablon_invalid_data():
    mock_invalid_data = "invalid_data"

    response = save_szablon(mock_invalid_data)

    assert response[0] == {"error": "Dane muszą być w formacie JSON"}
    assert response[1] == 400

def test_save_szablon_exception_handling():
    mock_data = mock_json_data

    with patch("builtins.open", side_effect=Exception("Some file error")):
        response = save_szablon(mock_data)

        assert response[0] == {"error": "Coś poszło nie tak: Some file error"}
        assert response[1] == 500