from sqlalchemy.orm import Session
from .. import models, schemas

class UserRepository:
    def get_user_by_email(self, db: Session, *, email: str) -> models.User | None:
        return db.query(models.User).filter(models.User.email == email).first()

    def create_user(self, db: Session, *, user_in: schemas.UserCreate) -> models.User:
        db_user = models.User(
            email=user_in.email,
            hashed_password=f"fake_hashed_{user_in.password}" # placeholder
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_repo = UserRepository()