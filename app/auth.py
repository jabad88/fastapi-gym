from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from db import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

#responsible for password hashing and unhashing
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

#validates the users input before submitting to the db
class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,db: db_dependency):
    new_user = User(username = create_user_request.username, hashed_password = bcrypt_context.hash(create_user_request.password))

    db.add(new_user)
    db.commit()
