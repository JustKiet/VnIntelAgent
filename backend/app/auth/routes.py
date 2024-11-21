from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta, datetime
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from ..database.base import SessionLocal
from ..schemas.auth import CreateUserRequest
from ..schemas.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

db_dependency = Annotated[Session, Depends(get_database)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        email = create_user_request.email,
        locale = create_user_request.locale,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

    db.add(create_user_model)
    db.commit()