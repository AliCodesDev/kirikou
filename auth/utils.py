from passlib.context import CryptContext
from database.utils import get_user_by_username
from typing import Optional, Dict
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"])




def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user by username and password.
    
    Args:
        db: Database session
        username: Username of the user
        password: Plaintext password to verify
    Returns:
        User dictionary if authentication is successful, None otherwise
    """

    user = get_user_by_username(db, username)
    if user and verify_password(password, user['hashed_password']):
        return user
    return None