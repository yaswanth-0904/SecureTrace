from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action = Column(
        String(100),
        nullable=False
    )

    dna_code = Column(
        String(100),
        nullable=False
    )

    performed_by = Column(
        String(100),
        nullable=False
    )