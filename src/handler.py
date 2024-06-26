import re
import orjson

from http import HTTPStatus
from pydantic import ValidationError

from database import add_transaction, get_client
from exceptions import ClientNotFound, InsufficientBalance, SqliteError
from model import Transaction, Error

get_client_url = re.compile(r"/clientes/\d+/extrato")
add_transaction_url = re.compile(r"/clientes/\d+/transacoes")

errors = {
    "invalid_transaction_inputs": Error(code=1, message="dados inválidos da transação"),
    "client_not_found": Error(code=2, message="cliente não encontrado"),
    "insufficient_balance": Error(code=3, message="saldo insuficiente"),
    "url_not_found": Error(code=4, message="url não encontrada"),
    "internal_server_error": Error(code=5, message="erro interno no servidor")
}

class Handler:
    def __init__(self, environ, start_response):
        self.request_method = environ["REQUEST_METHOD"]

        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0
        self.request_body = environ["wsgi.input"].read(request_body_size)

        self.path_info = environ["PATH_INFO"]
        self.start_response = start_response

    def _make_response(self, http_status, response_body):
        response_headers = [("Content-Type", "application/json")]
        status = f"{http_status.value} {http_status.phrase}"
        self.start_response(status, response_headers)
        if isinstance(response_body, bytes):
            return [response_body]
        return [response_body.encode("utf-8")]
    
    def _add_transaction(self, id):
        try:
            transaction = Transaction.model_validate_json(self.request_body)
        except ValidationError:
            return self._make_response(
                HTTPStatus.BAD_REQUEST, errors["invalid_transaction_inputs"].model_dump_json()
            )

        try:
            result = add_transaction(id, transaction)
        except ClientNotFound:
            return self._make_response(HTTPStatus.NOT_FOUND, errors["client_not_found"].model_dump_json())
        except InsufficientBalance:
            return self._make_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, errors["insufficient_balance"].model_dump_json()
            )
        except SqliteError:
            return self._make_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, errors["internal_server_error"].model_dump_json()
            )
        
        return self._make_response(HTTPStatus.OK, orjson.dumps(result))
        
    def _get_client(self, id):
        try:
            client = get_client(id)
        except ClientNotFound:
            return self._make_response(HTTPStatus.NOT_FOUND, errors["client_not_found"].model_dump_json())
        except SqliteError:
            return self._make_response(
                HTTPStatus.INTERNAL_SERVER_ERROR, errors["internal_server_error"].model_dump_json()
            )

        return self._make_response(HTTPStatus.OK, client.model_dump_json())

    
    def run(self):
        if self.request_method == "POST" and re.search(add_transaction_url, self.path_info):
            id = int(self.path_info.split("/")[2])
            return self._add_transaction(id)

        if self.request_method == "GET" and re.search(get_client_url, self.path_info):
            id = int(self.path_info.split("/")[2])
            return self._get_client(id)

        return self._make_response(HTTPStatus.NOT_FOUND, errors["url_not_found"].model_dump_json())