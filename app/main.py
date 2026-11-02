# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users

# >>> ADICIONAR ESTA LINHA (import só pelo efeito colateral de registrar
#     IndexedFile no Base.metadata; o nome é intencionalmente "não usado")
from app.filesearch import models as _filesearch_models  # noqa: F401

# Cria as tabelas no banco de dados (caso não existam)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth & User Management API",
    version="1.0.0"
)


# Definição das origens permitidas (CORS)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:63342",
    "http://localhost:63342",
    "null"
]

# Ignora a inspeção de tipos estritos do PyCharm no middleware do FastAPI
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os roteadores da aplicação
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health_check():
    """Rota de verificação de saúde da API."""
    return {"status": "ok"}