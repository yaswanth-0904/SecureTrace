from fastapi import FastAPI
from sqlalchemy import text
import app.models


from app.database.database import engine
from app.api.transaction_api import router as transaction_router

app = FastAPI()

app.include_router(transaction_router)


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