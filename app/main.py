from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import auth, users

# Cria as tabelas na base de dados (caso não existam)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth & User Management API",
    description="API para gestão de utilizadores e autenticação segura.",
    version="0.1.0",
)

# Configuração de CORS para permitir requisições da interface web
app.add_middleware(  # type: ignore
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers de autenticação e de utilizadores
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "API de Autenticação Ativa e Operacional!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}