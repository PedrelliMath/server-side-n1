# SERVER SIDE N1 - Matheus Mauricio

Conteúdo apresentado para obtenção de nota na matéria de Server Side
no curso de Engenhearia de Software pela Universidade Católica de Santa Catarina.

## RESUMO

Este repositório apresenta uma implementação simples de um Handler WSGI que permite 
a execução de código Python no lado do servidor ao receber uma requisição HTTP. 
O Handler WSGI inclui funcionalidades básicas para realizar transações financeiras com as requisições HTTP.

## Mod_python

O mod_python é um módulo do Apache que permite executar código python no lado do servidor
fazendo com que o web app python tenha acesso aos recursor do Apache, porém não ganhou
tanta popularidade quanto o WSGI pois era difícil de implementar e manter.

## WSGI

WSGI é uma especificação que padroniza a comunicação entre servidores e aplicações web,
desta forma, as aplicações podem ser desenvolvidas independente do servidor, permitindo
maior portabildiade, isso quer dizer que, o mesmo web app pode utilizar diversos servidores
web diferentes, desde que todos implementem a específicação

A PEP 333, escrita por `Phillip J. Eby` , lançada em `22 de fevereiro de 2003` e entitulado
`"Python Web Server Gateway Interface (WSGI)"`, define a específicação WSGI.


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

![rinha](https://github.com/zanfranceschi/rinha-de-backend-2024-q1/blob/main/misc/arte.jpg)

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

### `/src/'

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

## `/test/'

### `test_models.py`

Contém testes para testar a criação das classes de Transações e Clientes.

## `/.github/workflows'

### `tests.yml`

Contém um job para ser executado no github actions, esse job testa a criação das classes Transaction e Client,
caso ocorra um erro, o commit para a branch main é bloquado.


















