from sqlalchemy.orm import Session
from app import models
from app.core.security import verify_password
from app.repositories.user import user_repo

class AuthService:
    def authenticate_user(
        self,
        db: Session,
        *, 
        email: str,
        password: str
    ) -> models.User | None:
        user = user_repo.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

auth_service = AuthService()