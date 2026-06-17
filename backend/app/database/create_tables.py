from app.database.database import engine

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.dna_record import DNARecord
from app.models.audit_log import AuditLog
from app.database.base import Base

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")