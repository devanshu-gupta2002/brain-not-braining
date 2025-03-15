from llama_index.readers.llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from dotenv import load_dotenv
import nest_asyncio
from fastapi import HTTPException
from sqlalchemy.orm import Session
import json
from ..models.user import User

nest_asyncio.apply()
load_dotenv()

def get_parsed_doc(db: Session, current_user):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.document:
        return {"message": "Document is empty", "file": False}

    try:
        document_data = json.loads(user.document)
        document = Document(**document_data)
        return document
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse stored document")


def query_document(question: str, db: Session, current_user):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.document:
        raise HTTPException(status_code=404, detail="Document is empty")

    try:
        document_data = json.loads(user.document)
        document = Document(**document_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse stored document")

    index = VectorStoreIndex.from_documents([document])
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    
    return str(response)


def parse_document(filepath: str, db: Session, current_user):
    """Parse the document, store it as a JSON string in the database."""
    parser = LlamaParse(result_type="markdown")
    file_extractor = {".pdf": parser}
    
    documents = SimpleDirectoryReader(
        input_files=[filepath],
        file_extractor=file_extractor
    ).load_data()

    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    document_dict = documents[0].dict()  # Convert Document object to a dictionary
    document_json = json.dumps(document_dict)  # Convert dictionary to JSON string
    user.document = document_json  # Store JSON string in the database
    
    db.commit()
    db.refresh(user)
    
    return {"message": "Document stored successfully"}
