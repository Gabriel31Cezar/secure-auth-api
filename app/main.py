from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import auth, users

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth & User Management API",
    description="API para gestão de utilizadores e autenticação segura.",
    version="0.1.0",
)

# Inclui os routers de autenticação e de usuários
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "API de Autenticação Ativa e Operacional!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}