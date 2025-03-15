from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..services.auth import create_user, authenticate_user
from ..utils.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup", response_model=UserResponse)
def signup(user: UserCreate):
    return create_user(user)

@router.post("/auth/login", response_model=dict)
def login(login_data: LoginRequest):
    user = authenticate_user(UserLogin(email=login_data.email, password=login_data.password))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "token_type": "bearer"}
