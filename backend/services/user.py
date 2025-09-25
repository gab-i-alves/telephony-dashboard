from sqlalchemy.orm import Session
from .. import schemas, models
from ..repositories.user import user_repo
from core.security import get_password_hash
from fastapi import HTTPException

class UserService:
    def create_user(self, db: Session, *, user_in: schemas.UserCreate) -> models.User:
        user = user_repo.get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Um usuário com este e-mail já existe no sistema.",
            )
        
        hashed_password = get_password_hash(user_in.password)
        
        db_user = user_repo.create_user(
            db, email=user_in.email, hashed_password=hashed_password
        )
        return db_user

user_service = UserService()