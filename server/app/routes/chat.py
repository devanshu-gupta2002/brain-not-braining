from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from ..models.user import User
from ..utils.security import get_current_user
from ..schemas.user import UserDocument
from ..services.nlp_processing import parse_document, query_document, get_parsed_doc, remove_document
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
    response = get_parsed_doc(db, current_user)

    # Ensure response is a dictionary before adding the field
    if isinstance(response, dict):
        response["file"] = True
    else:
        response = {"data": response, "file": True}

    return response

ALLOWED_EXTENSIONS = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/chat/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check file type
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, and DOCX files are allowed")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")

    file_extension = file.filename.split(".")[-1]
    file_location = f"uploads/{current_user.id}_{file.filename}"  # Unique filename
    os.makedirs("uploads", exist_ok=True)

    with open(file_location, "wb") as file_object:
        file_object.write(content)

    parsed_data = parse_document(file_location, db, current_user)

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

@router.delete("/chat/delete")
def delete_document(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = remove_document(db, current_user)
    return response