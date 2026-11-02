# app/routers/auth.py
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, security

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Dicionário em memória para controlo de tentativas falhadas e bloqueio temporal
# Estrutura: {username: {"attempts": int, "lock_until": datetime}}
FAILED_LOGIN_ATTEMPTS: dict[str, dict] = {}
MAX_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 5


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Regista um novo utilizador no sistema com senha hasheada."""
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já registado no sistema."
        )

    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de utilizador já em uso."
        )

    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica o utilizador, valida bloqueio por força bruta e emite o token JWT."""
    username = form_data.username
    now = datetime.now(timezone.utc)

    # Verifica se o utilizador está atualmente bloqueado
    if username in FAILED_LOGIN_ATTEMPTS:
        lock_info = FAILED_LOGIN_ATTEMPTS[username]
        if lock_info["lock_until"] and now < lock_info["lock_until"]:
            remaining_minutes = int((lock_info["lock_until"] - now).total_seconds() / 60) + 1
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Conta temporariamente bloqueada devido a excesso de tentativas falhadas. Tente novamente em {remaining_minutes} minuto(s)."
            )
        elif lock_info["lock_until"] and now >= lock_info["lock_until"]:
            # Reseta o bloqueio se o tempo já expirou
            FAILED_LOGIN_ATTEMPTS[username] = {"attempts": 0, "lock_until": None}

    # Procura o utilizador na base de dados
    user = db.query(models.User).filter(models.User.username == username).first()

    # Validação de credenciais
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # Regista a tentativa falhada
        if username not in FAILED_LOGIN_ATTEMPTS:
            FAILED_LOGIN_ATTEMPTS[username] = {"attempts": 1, "lock_until": None}
        else:
            FAILED_LOGIN_ATTEMPTS[username]["attempts"] += 1

        attempts_left = MAX_ATTEMPTS - FAILED_LOGIN_ATTEMPTS[username]["attempts"]

        if FAILED_LOGIN_ATTEMPTS[username]["attempts"] >= MAX_ATTEMPTS:
            FAILED_LOGIN_ATTEMPTS[username]["lock_until"] = now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Demasiadas tentativas falhadas. Conta bloqueada por {LOCKOUT_DURATION_MINUTES} minutos."
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Credenciais inválidas. Restam {attempts_left} tentativa(s) antes do bloqueio temporal.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Login bem-sucedido: limpa o registo de falhas
    if username in FAILED_LOGIN_ATTEMPTS:
        FAILED_LOGIN_ATTEMPTS[username] = {"attempts": 0, "lock_until": None}

    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}