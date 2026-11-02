# app/main.py (Trecho atualizado)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, filesearch  # <-- Adicionado filesearch
from app.filesearch import models as _filesearch_models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth & User Management API",
    version="1.0.0"
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:63342",
    "http://localhost:63342"
]

# Ignora a inspeção de tipos estritos do PyCharm/VS Code no middleware do FastAPI
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(filesearch.router)  # <-- Adicionado filesearch.router


@app.get("/health")
def health_check():
    return {"status": "ok"}