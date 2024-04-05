from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_serializer

class TransactionType(str, Enum):
    credit = "c"
    debit = "d"


class Transaction(BaseModel):
    amount: int = Field(alias="valor", gt=0)
    type: TransactionType = Field(alias="tipo")
    description: str = Field(alias="descricao", min_length=1, max_length=10)
    created_at: datetime = Field(alias="realizada_em", default_factory=datetime.utcnow)

    @model_serializer
    def serialize_model(self):
            return{
                "valor":self.amount,
                "tipo":self.type.value, 
                "descricao":self.description,
                "realizada_em":self.created_at   
            }

class Client(BaseModel):
    id: int
    account_limit: int = Field(alias="limite")
    account_balance: int = Field(alias="saldo")
    transactions: list[Transaction] = Field(alias="ultimas_transacoes", default=[])

    @model_serializer
    def serialize_model(self):
        return{
            "saldo":{
                "total":self.account_balance,
                "data_extrato": datetime.utcnow().isoformat(),
                "limite":abs(self.account_limit)
            },
            "ultimas_transacoes":[
                {
                    "valor":transaction.amount,
                    "tipo":transaction.type.value, 
                    "descricao":transaction.description,
                    "realizada_em":transaction.created_at
                } for transaction in self.transactions
            ]
        }

class Error(BaseModel):
    code: int
    message: str