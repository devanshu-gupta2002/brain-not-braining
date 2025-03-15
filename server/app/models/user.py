from sqlalchemy import Column, Integer, String, Text
from ..database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    document = Column(Text, nullable=True, default=None)  # Optional field, defaults to None
