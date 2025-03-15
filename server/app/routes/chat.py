from fastapi import APIRouter, Depends, HTTPException
from ..models.user import User
from ..utils.security import get_current_user

router = APIRouter()

@router.get("/chat")
def chat(current_user: User = Depends(get_current_user)):
    return {"document": current_user.document}