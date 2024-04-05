import pytest
from unittest.mock import patch, Mock
from src.handler import get_client, add_transaction, Client, Transaction, TransactionType, ClientNotFound, InsufficientBalance, SqliteError

@pytest.fixture
def mock_db_connect():
    with patch('sqlite3.connect') as mock_connect:
        yield mock_connect

def test_get_client(mock_db_connect):
    # Defina o comportamento esperado do objeto mock de conexão
    mock_cursor = mock_db_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1, -100000, 0)

    # Chame a função que você está testando
    client = get_client(1)

    # Verifique se a função retorna o cliente esperado
    assert isinstance(client, Client)
    assert client.id == 1
    assert client.limite == -100000
    assert client.saldo == 0

def test_add_transaction(mock_db_connect):
    # Defina o comportamento esperado do objeto mock de conexão
    mock_cursor = mock_db_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1, -100000, 0)

    # Defina o objeto de transação mock
    mock_transaction = Mock(spec=Transaction)
    mock_transaction.amount = 5000
    mock_transaction.type.value = "c"
    mock_transaction.description = "Depósito"
    mock_transaction.created_at = "2024-03-27 10:00:00"

    # Chame a função que você está testando
    result = add_transaction(1, mock_transaction)

    # Verifique se a função retorna o resultado esperado
    assert result == {"limite": -100000, "saldo": 5000}
