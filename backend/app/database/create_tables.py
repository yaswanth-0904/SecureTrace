from app.database.database import engine

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

from app.database.base import Base

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")