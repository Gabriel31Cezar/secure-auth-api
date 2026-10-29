from datetime import datetime
from pydantic import BaseModel, EmailStr


# Schema base para partilhar atributos comuns de utilizador
class UserBase(BaseModel):
    email: EmailStr
    username: str


# Schema utilizado na criação de um utilizador (recebe a senha em texto limpo)
class UserCreate(UserBase):
    password: str


# Schema de resposta (retorna os dados sem a senha por motivos de segurança)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas para Autenticação JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None