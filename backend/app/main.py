from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "SecureTrace Backend Running"
    }


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 'Database Connected Successfully'")
        )

        return {
            "message": result.scalar()
        }