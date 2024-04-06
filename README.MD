# SERVER SIDE N1 - Matheus Mauricio

Conteúdo apresentado para obtenção de nota na matéria de Server Side
no curso de Engenhearia de Software pela Universidade Católica de Santa Catarina.

## RESUMO

Este repositório apresenta uma implementação simples de um Handler WSGI que permite 
a execução de código Python no lado do servidor ao receber uma requisição HTTP. 
O Handler WSGI inclui funcionalidades básicas para realizar transações financeiras com as requisições HTTP.

## Mod_python

![mod_python](https://modpython.org/mp_long.gif)

O mod_python é um módulo do Apache que permite executar código python no lado do servidor
fazendo com que o web app python tenha acesso aos recursor do Apache, porém não ganhou
tanta popularidade quanto o WSGI pois era difícil de implementar e manter.

## WSGI

![wsgi](https://assets.toptal.io/images?url=https%3A%2F%2Fbs-uploads.toptal.io%2Fblackfish-uploads%2Fuploaded_file%2Ffile%2F192775%2Fimage-1582505123212-d71812e36fd836399c48a034f9e70128.png)
fonte: [https://www.toptal.com/python/pythons-wsgi-server-application-interface](https://www.toptal.com/python/pythons-wsgi-server-application-interface)

WSGI é uma especificação que padroniza a comunicação entre servidores e aplicações web,
desta forma, as aplicações podem ser desenvolvidas independente do servidor, permitindo
maior portabildiade, isso quer dizer que, o mesmo web app pode utilizar diversos servidores
web diferentes, desde que todos implementem a específicação

A PEP 333, escrita por `Phillip J. Eby` , lançada em `22 de fevereiro de 2003` e entitulado
`"Python Web Server Gateway Interface (WSGI)"`, define a específicação WSGI.

[Mais detalhes da PEP333 aqui](https://peps.python.org/pep-0333/)

## COMO FUNCIONA?

O servidor que implementa a especificação WSGI precisa receber como argumentos de execução
qual arquivo e qual função do aplicativo web respondem as requisições.

- o arquivo `wsgi.py` contem uma função `app`, esta que serve como chamável para o servidor web

A cada requisição, o servidor web cria uma instancia da aplicação, chamando a função e passando
dois argumentos para ela. `environ` e `start_response`.

- `environ` é um objeto com os dados da requisição, como cabeçalhos, corpo e etc.
- `start_response` é uma função de callback que o web app precisa executar para retornar a reposta

O web app executa lógica de negócio utilizando `environ`, executa `start_response` passando
os cabeçalhos da resposta e depois, retorna um `ITERÁVEL DE BYTES` com os dados da resposta.

- o arquivo `handler.py` implementa essa lógica.


## RINHA DE BACKEND 2024 Q1

![rinha](https://raw.githubusercontent.com/zanfranceschi/rinha-de-backend-2024-q1/main/misc/arte.jpg)

A rinha de backend é um evento de programação competitiva que busca comparar implementações
de API que respondam requests HTTP.

Cada rinha possue uma específicação diferente e a em questão foi realizada no mês
de fevereiro de 2024.

[Mais detalhes da rinha aqui](https://github.com/zanfranceschi/rinha-de-backend-2024-q1)

### Específicação da rinha

Básicamente, precisa ser implementado 2 endpoints, sendo eles:

## ENDPOINT - TRANSAÇÕES

`POST /clientes/{id}/transacoes`: 

```
{
    "valor": 1000,
    "tipo" : "c",
    "descricao" : "descricao"
}
```

Enviando um JSON no corpo da requisição, onde:

`valor`:quantidade de dinheiro
`tipo`:tipo da transação, détitar ou creditar
`descricao`:uma breve descrição

## Resposta

Se o cliente tiver limite o suficiente, a resposta deve ser

`HTTP 200 OK`

Retornando um JSON no corpo da resposta com as seguintes informações:

```
{
    "limite" : 100000,
    "saldo" : -9098
}
```

`limite`:limite atual do cliente que fez a transacao
`saldo`:saldo atual do cliente apos a transacao

## ENDPOINT - EXTRATO

`GET /clientes/{id}/extrato`

## Resposta

`HTTP 200 OK`

```
{
  "saldo": {
    "total": -9098,
    "data_extrato": "2024-01-17T02:34:41.217753Z",
    "limite": 100000
  },
  "ultimas_transacoes": [
    {
      "valor": 10,
      "tipo": "c",
      "descricao": "descricao",
      "realizada_em": "2024-01-17T02:34:38.543030Z"
    },
    {
      "valor": 90000,
      "tipo": "d",
      "descricao": "descricao",
      "realizada_em": "2024-01-17T02:34:38.543030Z"
    }
  ]
}
```

Onde
- `saldo`
    - `total` deve ser o saldo total atual do cliente (não apenas das últimas transações seguintes exibidas).
    - `data_extrato` deve ser a data/hora da consulta do extrato.
    - `limite` deve ser o limite cadastrado do cliente.
- `ultimas_transacoes` é uma lista ordenada por data/hora das transações de forma decrescente contendo até as 10 últimas transações com o seguinte:
    - `valor` deve ser o valor da transação.
    - `tipo` deve ser `c` para crédito e `d` para débito.
    - `descricao` deve ser a descrição informada durante a transação.
    - `realizada_em` deve ser a data/hora da realização da transação.

## COMO O CÓDIGO FUNCIONA

### `src/`

### `wsgi.py`

Esse arquivo cria uma instância de FastWSGI, um servidor web wsgi, passando como parâmetros a função `app`
que irá lidar com a requisição.

Essa função cria uma instância de um objeto `Handler` e chama o método `run()`.

### `handler.py`

Esse arquivo possui a definição da classe `Handler`, esta classe possuí `run()` para receber requisições, `_add_transaction()` e  `_get_client()` para lidar com as requisições acessando o banco de dados e `_make_response()` para retornar a resposta para o servidor web FastWSGI.

`_make_response(http_status, response_body)` recebe como parâmetros o http status gerado pelas funções de acesso ao banco de dados, e a resposta à ser enviada, executa `start_response` enviando os cabeçalhos como descreve na específicação, e retorna um iterável de bytes com o corpo da resposta. 

### `database.py`

Esse arquivo possuí as funções de acesso ao banco de dados para realizar a busca do histórico de transações do cliente e realizar a inserção de uma nova transação. Caso ocorra algum tipo de violação, de acordo com a específicação, as funções levantam as respectivas exeções. 

### `model.py`

Esse arquivo possui os classes do domínio da aplicação, que são Clientes e Transaçõe. Quando chega uma requisição, ocorre uma tentativa de criar um objeto a partir dessas classes, caso não seja possível, significa que os dados enviados estão incorretos e é retornado status de erro. Além de tamber contarem com métodos de serialização para facilitar o modelo de retorno de dados como solicitado na específicação. 

### `config.py`

Esse arquivo possuí algumas configurações do servidor web e do banco de dados, como o caminho para o arquivo do banco e em qual porta e qual host o servidor web estará esperando requisições.

### `exceptions.py`

Esse arquivo possue algumas classes de erros que serão levantados pelas funções no arquivo `database.py`.

### `__init__.py`

Cria variáveis de ambiente para facilitar a importação das funções.

## `test/`

### `test_models.py`

Contém testes para testar a criação das classes de Transações e Clientes.

## `.github/workflows/`

### `tests.yml`

Contém um job para ser executado no github actions, esse job testa a criação das classes Transaction e Client,
caso ocorra um erro, o commit para a branch main é bloquado.

## MODELO DO BANCO DE DADOS

O banco de dados possue 2 tabelas, uma para clientes e outra para transações

### Tabela `clientes`

| id | limite  | saldo |
|----|---------|-------|
| 1  | -100000 | 0     |
| 2  | -80000  | 0     |
| 3  | -1000000| 0     |
| 4  | -10000000| 0    |
| 5  | -500000 | 0     |

### Tabela `transactions`

| id_cliente | valor | tipo | descricao | realizada_em |
|------------|-------|------|-----------|--------------|
|            |       |      |           |              |

## COMO INSTALAR

* Clone o este repositório na sua máquina

```
git clone https://codeberg.org/PedrelliMath/server-side-n1.git
```

* Entre no diretório do respitório

```
cd server-side-n1
```

* Crie um ambiente virtual

```
python -m venv venv
```

* Ative o ambiente virtual

```
source venv/bin/activate
```

* Instale as depências do projeto

```
pip install -r requirements.txt
```

* Instale se quiser o pytest pelas depências de desenvolvimento

```
pip install -r requirements-dev.txt
```

## COMO RODAR O SERVIDOR WEB

* Execute o arquivo `wsgi.py`, isso vai criar uma instância do servidor web FastWSGI

```
➜ python wsgi.py 
FastWSGI server running on PID: 141019
FastWSGI server listening at http://0.0.0.0:9999
```

## COMO FAZER REQUISIÇÕES

* Utilize um cliente para fazer requisições como Curl, httpie, postman, etc. Estou usando httpie

### CRIANDO TRANSAÇÃO CRÉDITO VAĹIDA

* Faça uma requisição com método `POST` em `http://0.0.0.0:9999/clientes/{id}/transacoes` trocando {id} pelo id do cliente e passando no corpo da requisição o JSON com os dados.

A resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/clientes/3/transacoes valor=100 tipo="c" descricao="teste"

POST /clientes/3/transacoes HTTP/1.1
Accept-Encoding: gzip
Content-Length: 46
Content-Type: application/json
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0

{
    "descricao": "teste",
    "tipo": "c",
    "valor": "100"
}

HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 31
Content-Type: application/json
Date: Sat, 6 Apr 2024 21:40:10 GMT

{
    "limite": -1000000,
    "saldo": 200
}
```

O saldo cliente era 100 e aumentou para 200

### CRIANDO TRANSAÇÃO DÉBITO VÁLIDA

* Faça uma requisição com método `POST` em `http://0.0.0.0:9999/clientes/{id}/transacoes` trocando {id} pelo id do cliente e passando no corpo da requisição o JSON com os dados.

Se houver limite, a resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/clientes/3/transacoes valor=100 tipo="d" descricao="teste"

POST /clientes/3/transacoes HTTP/1.1
Accept-Encoding: gzip
Content-Length: 46
Content-Type: application/json
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0

{
    "descricao": "teste",
    "tipo": "d",
    "valor": "100"
}

HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 31
Content-Type: application/json
Date: Sat, 6 Apr 2024 21:46:28 GMT

{
    "limite": -1000000,
    "saldo": 100
}
```

O saldo era 200 e voltou para 100

### CRIANDO TRANSAÇÃO DÉBITO INVÁLIDA

* Faça uma requisição com método `POST` em `http://0.0.0.0:9999/clientes/{id}/transacoes` trocando {id} pelo id do cliente e passando no corpo da requisição o JSON com os dados e coloque o valor a debitar maior que o saldo + limite

A resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/clientes/3/transacoes valor=2000000 tipo="d" descricao="teste"

POST /clientes/3/transacoes HTTP/1.1
Accept-Encoding: gzip
Content-Length: 50
Content-Type: application/json
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0

{
    "descricao": "teste",
    "tipo": "d",
    "valor": "2000000"
}

HTTP/1.1 422 UNPROCESSABLE_ENTITY
Connection: keep-alive
Content-Length: 41
Content-Type: application/json
Date: Sat, 6 Apr 2024 21:50:39 GMT

{
    "code": 3,
    "message": "saldo insuficiente"
}
```

422 UNPROCESSABLE_ENTITY é o http response que significa que os dados foram recebidos mas não podem ser processados devido à uma falha de validação

### SOLICITANDO HISTÓRICO DE TRANSAÇÕES

* Faça uma requisição `GET` em `http://0.0.0.0:9999/clientes/{id}/extrato` trocando {id} pelo id do cliente.

A resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/clientes/3/extrato

GET /clientes/3/extrato HTTP/1.1
Accept-Encoding: gzip
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0


HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 374
Content-Type: application/json
Date: Sat, 6 Apr 2024 21:56:08 GMT

{
    "saldo": {
        "total": 100,
        "data_extrato": "2024-04-06T21:56:08.770221",
        "limite": 1000000
    },
    "ultimas_transacoes": [
        {
            "valor": 100,
            "tipo": "d",
            "descricao": "teste",
            "realizada_em": "2024-04-06T21:56:08.770144"
        },
        {
            "valor": 100,
            "tipo": "c",
            "descricao": "teste",
            "realizada_em": "2024-04-06T21:56:08.770169"
        }
    ]
}
```
O histórico está limitado em 10 transações

### ENVIANDO JSON INVÁLIDO

* Faça uma requisição com método `POST` em `http://0.0.0.0:9999/clientes/{id}/transacoes` trocando {id} pelo id do cliente e passando no corpo da requisição o JSON com campos inválidos.

A resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/clientes/3/transacoes alor=2000000 tipo="d" descricao="teste"

POST /clientes/3/transacoes HTTP/1.1
Accept-Encoding: gzip
Content-Length: 49
Content-Type: application/json
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0

{
    "alor": "2000000",
    "descricao": "teste",
    "tipo": "d"
}

HTTP/1.1 400 BAD_REQUEST
Connection: keep-alive
Content-Length: 54
Content-Type: application/json
Date: Sat, 6 Apr 2024 22:00:06 GMT

{
    "code": 1,
    "message": "dados inválidos da transação"
}
```
400 BAD_REQUEST é o http response que significa que o cliete enviou dados incorretos

### SOLICITANDO UM ENDPOINT INVÁLIDO

* Faça uma requisição com método `GET` em `http://0.0.0.0:9999/{qualquer-coisa-aqui}`

A resposta deve se parecer com isso:

```
➜ ht -v 0.0.0.0:9999/teste

GET /teste HTTP/1.1
Accept-Encoding: gzip
Host: 0.0.0.0:9999
User-Agent: httpie-go/0.7.0


HTTP/1.1 404 NOT_FOUND
Connection: keep-alive
Content-Length: 42
Content-Type: application/json
Date: Sat, 6 Apr 2024 22:03:26 GMT

{
    "code": 4,
    "message": "url não encontrada"
}
```
404 NOT_FOUND é o http response que significa que o cliente tentou acessar o um recurso que não existe

## TESTES

Para realizar os testes digite o comando `pytest -v` na raiz do projeto

```
➜ pytest -v
============================= test session starts ==============================
platform linux -- Python 3.11.5, pytest-8.1.1, pluggy-1.4.0 -- /home/matheus/faculdade/server-side/python_projects/wsgi_handler/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/matheus/faculdade/server-side/python_projects/wsgi_handler
plugins: mock-3.14.0, cov-5.0.0
collected 3 items                                                              

test/test_models.py::test_transaction_model PASSED                       [ 33%]
test/test_models.py::test_client_model PASSED                            [ 66%]
test/test_models.py::test_error_model PASSED                             [100%]

============================== 3 passed in 0.10s ===============================
```
Os testes criam instâncias cliente, transaction, e erros.

## CI/CD

Criei uma implementação básica de um job para rodar no github actions, os pushs que serão feitos para o github e não para o codeberg, serão testados antes de subirem, segue o resultado:

```
"workflow_runs": [
        {
            "id": 8571594964,
            "name": "Run Tests",
            "head_branch": "main",
            "path": ".github/workflows/tests.yml",
            "display_title": "actions melhorado",
            "run_number": 2,
            "event": "push",
            "status": "completed",
            "conclusion": "success",
            "workflow_id": 92563419,
        }
]
```
