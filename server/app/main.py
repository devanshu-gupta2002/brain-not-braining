from fastapi import FastAPI
from .routes import auth, user, chat
from .database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)