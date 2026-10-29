from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Secure Auth API"
    PROJECT_VERSION: str = "0.1.0"

    # Configuração da Base de Dados (SQLite para desenvolvimento local)
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # Configurações de Segurança (JWT)
    SECRET_KEY: str = "sua_chave_secreta_super_segura_aqui_para_desenvolvimento"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()