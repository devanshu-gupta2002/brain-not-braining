from fastapi import HTTPException, status
from ..database.session import SessionLocal
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin
from ..utils.security import get_password_hash, verify_password

def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(user: UserLogin):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return db_user