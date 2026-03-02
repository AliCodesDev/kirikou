from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import utils as db_utils
from auth.schemas import UserCreate, UserResponse, TokenResponse
from sqlalchemy.orm import Session
from database.db import get_db
from auth.jwt_handler import create_access_token
from auth.utils import hash_password, authenticate_user



router = APIRouter(prefix="/auth", tags=["Users"])

@router.post("/register", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint to register a new user."""
    existing_user = db_utils.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    if db_utils.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    new_user = db_utils.create_user(db, user.username, user.email, hashed)
    db.commit()
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint to authenticate a user and return a JWT token."""
    
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token_data = {"user_id": user['id'], "username": user['username']}
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token)








