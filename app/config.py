from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Secure Auth API"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "chave_padrao_apenas_para_desenvolvimento_local"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()