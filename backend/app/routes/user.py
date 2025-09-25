from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.core.database import get_db
from app.services.user import user_service

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