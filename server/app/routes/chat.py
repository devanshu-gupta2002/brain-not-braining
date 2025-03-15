from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from ..models.user import User
from ..utils.security import get_current_user
from ..schemas.user import UserDocument
from ..services.nlp_processing import parse_document, query_document, get_parsed_doc
from ..database.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request body schema for asking a question
class QuestionRequest(BaseModel):
    question: str

@router.get("/chat")
def get_document(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return get_parsed_doc(db, current_user)

@router.post("/chat/upload")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    parsed_data = parse_document(file_location, db, current_user)

    # Remove the file after updating the database
    try:
        os.remove(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    return {"filename": file.filename, "data": parsed_data}

@router.post("/chat/ask")
def get_answer(
    request: QuestionRequest,  # Expect request body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = query_document(request.question, db, current_user)  # Use request.question
    return {"answer": answer}
