from fastapi import FastAPI

app = FastAPI(
    title="Secure Auth & User Management API",
    description="API para gestão de utilizadores e autenticação segura.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "API de Autenticação Ativa e Operacional!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}