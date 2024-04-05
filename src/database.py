import sqlite3

from src.config import settings
from src.exceptions import ClientNotFound, InsufficientBalance, SqliteError
from src.model import Client, Transaction, TransactionType

def init_database(init_sql_file):

    try:
        with open(init_sql_file, 'r') as init_file:
            sql = init_file.read()
    except FileNotFoundError:
        print("O arquivo init.sql nao foi encontrado")
        raise SqliteError
    except IOError:
        print("Erro ao ler o arquivo init.sql")
        raise SqliteError

    try:
        with sqlite3.connect(settings.database_file) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql)
            conn.commit()
            print("Init.sql foi executado sem erros")
    except sqlite3.Error as e:
        print(f"Erro ao iniciar o banco de dados: {e}")
        raise SqliteError

def get_client(id):

    get_client_query = """
        SELECT id, limite, saldo FROM clientes WHERE id = ?
    """

    get_transaction_query = """
        SELECT valor, tipo, descricao, realizada_em FROM transactions WHERE id_cliente = ? 
        ORDER BY strftime('%Y-%m-%d %H:%M:%S', realizada_em) DESC
        LIMIT 10;
    """

    try:
        with sqlite3.connect(settings.database_file) as conn:
            cursor = conn.cursor()
            try:
                client = cursor.execute(get_client_query, (id,)).fetchone()
            except sqlite3.Error as e:
                print(f"Houve uma falha ao buscar um cliente {e}")
                raise SqliteError
            
            if client is None:
                raise ClientNotFound
            
            try:
                transactions = cursor.execute(get_transaction_query, (id,)).fetchall()
            except sqlite3.Error as e:
                print(f"Houve uma falha ao buscar o historico de transacoes {e}")
                raise SqliteError
            
            if transactions is None:
                transactions = []
            
            cliente = Client(
                id = client[0],
                limite = client[1],
                saldo = client[2],
                ultimas_transacoes=[
                    Transaction(
                        valor = transaction[0],
                        tipo = TransactionType(transaction[1]),
                        descricao = transaction[2]
                        ) 
                    for transaction in transactions
                ]
            )

            return cliente
    except sqlite3.Error as e:
                print(f"Houve uma falha criar a conexao com o banco {e}")
                raise SqliteError


def add_transaction(id, transaction):

    client_balance_query = """
        SELECT limite, saldo FROM clientes WHERE id = ?
    """

    update_balance_query = """
        UPDATE clientes SET saldo = ? WHERE id = ?
    """

    insert_transactions_query = """
        INSERT INTO transactions (id_cliente, valor, tipo, descricao, realizada_em)
        VALUES (?, ?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(settings.database_file) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(client_balance_query, (id,))
            except sqlite3.Error as e:
                print(f"Houve uma falha ao buscar o cliente {e}")
                raise SqliteError

            cliente = cursor.fetchone()
            if cliente is None:
                raise ClientNotFound

            limit, balance = cliente[0], cliente[1]

            if transaction.type.value == "c":
                balance += transaction.amount
            elif transaction.type.value == "d":
                new_balance = balance - transaction.amount
                if new_balance < limit:
                    raise InsufficientBalance

                balance = new_balance

            try:
                cursor.execute(update_balance_query,(balance, id))          
            except sqlite3.IntegrityError:
                raise InsufficientBalance
            
            try:
                cursor.execute(
                    insert_transactions_query, 
                    (
                        id,
                        transaction.amount,
                        transaction.type.value,
                        transaction.description,
                        transaction.created_at
                    )
                )
            except sqlite3.Error as e:
                print(f"Houve uma falha ao inserir transacao {e}")
                raise SqliteError
            
    except sqlite3.Error as e:
            print(f"Houve uma falha ao se conectar com o banco {e}")
            raise SqliteError
            
    return {
        "limite":limit,
        "saldo":balance
    }
