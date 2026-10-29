from fastapi import FastAPI
from app.database import engine
from app import models

# Cria as tabelas na base de dados (caso ainda não existam)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth & User Management API",
    description="API para gestão de utilizadores e autenticação segura.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "API de Autenticação Ativa e Operacional!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}