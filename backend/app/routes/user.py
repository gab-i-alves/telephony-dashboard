from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.core.database import get_db
from app.services.user import user_service
from app.routes.auth import get_current_user

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
    user = user_service.create_user(db=db, user_in=user_in)
    return user

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user