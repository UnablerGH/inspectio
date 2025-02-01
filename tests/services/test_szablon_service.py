import pytest
from unittest.mock import patch, mock_open, MagicMock
from services.szablon_service import get_szablon, save_szablon

def test_get_szablon():
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')) as mock_file:
        result = get_szablon()
        assert result == {"key": "value"}
        mock_file.assert_called_once_with('szablon.json', 'r', encoding='utf-8')

def test_save_szablon():
    with patch("builtins.open", mock_open()) as mock_file, patch('json.dump') as mock_json_dump:
        mock_json_dump.return_value = None  # Simulate successful JSON write

        data = {"new_key": "new_value"}
        result = save_szablon(data)

        assert result == {"message": "Szablon został zapisany pomyślnie"}  # Check dictionary structure