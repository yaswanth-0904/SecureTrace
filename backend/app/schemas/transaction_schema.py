from pydantic import BaseModel


class TransactionCreate(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: int