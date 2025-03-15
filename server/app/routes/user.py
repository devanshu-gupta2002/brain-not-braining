from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..models.user import User
from ..schemas.user import UserDocument
from ..utils.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.put("/user/document", response_model=UserDocument)
# def update_document(
#     document: UserDocument, 
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     user = db.query(User).filter(User.id == current_user.id).first()
#     if not user:
#         raise HTTPException(status_code=404, error="User not found")

#     user.document = document.document
#     db.commit()
#     db.refresh(user)
#     return user

# @router.get("/user/document", response_model=UserDocument)
# def get_document(
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     return current_user
