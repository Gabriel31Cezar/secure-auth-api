from fastapi import APIRouter, Depends
from app import models, schemas, security

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(
    current_user: models.User = Depends(security.get_current_user),
):
    """Retorna os dados do utilizador atualmente autenticado via JWT."""
    return current_user