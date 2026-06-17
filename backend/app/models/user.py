from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    security_score = Column(
        Integer,
        default=100
    )

    role = Column(
        String,
        default="USER",
        nullable=False
    )
    auth_token = Column(
    String,
    nullable=True
)