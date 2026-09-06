from fastapi import FastAPI

from backend.routes.chat import router as chat_router

from backend.database.database import create_tables

app = FastAPI()

create_tables()

app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Enterprise AI Assistant API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
