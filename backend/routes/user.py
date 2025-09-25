from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..core.database import get_db
from ..services.user import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate
):
    """
    Cria um novo usuário no sistema.
    """
    user = user_service.create_user(db=db, user_in=user_in)
    return user