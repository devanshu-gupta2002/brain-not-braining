from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDocument(BaseModel):
    document: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    # document: str

    class Config:
        orm_mode = True