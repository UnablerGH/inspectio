import pytest
from unittest.mock import patch, MagicMock
from repo.db import query_db, get_db_connection, create_tables, insert_initial_data

@pytest.fixture
def mock_db_connection():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn

def test_get_db_connection(mock_db_connection):
    conn = get_db_connection()
    assert conn == mock_db_connection

def test_query_db(mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [{'id_hospitacji': 1, 'termin': '2025-04-15', 'data_zatwierdzenia': None, 'nazwa': 'Techniki efektywnego programowania'}]

    result = query_db('SELECT * FROM hospitacje', one=True)
    assert result['id_hospitacji'] == 1
    assert result['termin'] == '2025-04-15'
    assert result['data_zatwierdzenia'] is None
    assert result['nazwa'] == 'Techniki efektywnego programowania'

def test_create_tables(mock_db_connection):
    with patch.object(mock_db_connection, 'cursor') as mock_cursor:
        mock_cursor.return_value.execute = MagicMock()
        
        create_tables()
        
        assert mock_cursor.return_value.execute.call_count == 8

def test_insert_initial_data(mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value

    with patch('repo.db.get_db_connection', return_value=mock_db_connection):
        insert_initial_data()

    assert mock_cursor.execute.call_count > 0 
    assert mock_cursor.executemany.call_count > 0  
    mock_db_connection.commit.assert_called_once()  
    mock_db_connection.close.assert_called_once()  