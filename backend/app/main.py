from fastapi import FastAPI
from sqlalchemy import text
import app.models
from app.database.database import engine
from app.api.transaction_api import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaction_router)


@app.get("/")
def home():
    return {
        "status": "Securetrace Backend Running"
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