import pytest
from datetime import datetime
from src.model import Transaction, TransactionType, Client, Error

def test_transaction_model():
    transaction_data = {
        "valor": 1000,
        "tipo": "c",
        "descricao": "compra"
    }
    transaction = Transaction(**transaction_data)
    assert transaction.amount == 1000
    assert transaction.type == TransactionType.credit
    assert transaction.description == "compra"
    assert isinstance(transaction.created_at, datetime)

    with pytest.raises(ValueError):
        transaction = Transaction(amount=-1000, type=TransactionType.debit, description="Compra")

    with pytest.raises(ValueError):
        transaction = Transaction(amount=1000, type=TransactionType.credit, description="Descrição muito longa")

def test_client_model():
    transaction_data = {
        "valor": 1000,
        "tipo": "c",
        "descricao": "Compra",
    }
    client_data = {
        "id": 1,
        "limite": 10000,
        "saldo": 5000,
        "ultimas_transacoes":[Transaction(**transaction_data)]
    }
    client = Client(**client_data)
    assert client.id == 1
    assert client.account_limit == 10000
    assert client.account_balance == 5000
    assert len(client.transactions) == 1
    assert isinstance(client.transactions[0], Transaction)

def test_error_model():
    error_data = {
        "code": 404,
        "message": "Cliente não encontrado"
    }
    error = Error(**error_data)
    assert error.code == 404
    assert error.message == "Cliente não encontrado"
