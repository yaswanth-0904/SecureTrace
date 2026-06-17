from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.base import Base


class DNARecord(Base):
    __tablename__ = "dna_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dna_code = Column(
        String(100),
        unique=True,
        nullable=False
    )

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id")
    )

    parent_dna = Column(
        String(100),
        nullable=True,
        index=True
    )

    amount = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        default="ACTIVE",
        nullable=False
    )

    child_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    remaining_amount = Column(
        Integer,
        default=0,
        nullable=False
    )

    is_flagged = Column(
        Integer,
        default=0,
        nullable=False
    )

    is_frozen = Column(
        Integer,
        default=0,
        nullable=False
    )

    risk_score = Column(
        Integer,
        default=0,
        nullable=False
    )
    
    recovered_amount = Column(
        Integer,
        default=0,
        nullable=False
    )

    