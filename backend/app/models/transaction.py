from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    sender_account_id = Column(
        Integer,
        ForeignKey("accounts.id")
    )

    receiver_account_id = Column(
        Integer,
        ForeignKey("accounts.id")
    )

    amount = Column(Integer)

    transaction_type = Column(
        String,
        default="TRANSFER"
    )