from datetime import datetime, timedelta, timezone
import jwt, logging
from config import get_settings


settings = get_settings()
settings.setup_logging()
logger = logging.getLogger(__name__)



def create_access_token(data: dict) -> str:
    
    payload = {
        "sub": data.get("user_id"),  # Subject of the token (ex user ID)
        "username": data.get("username"),  # Additional user info
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),  # Expiration time
        "iat": datetime.now(timezone.utc)  # Issued at time
    }

    token = jwt.encode(payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)
    return token


def verify_access_token(token: str) -> dict:

    try:
        payload = jwt.decode(token, settings.jwt_secret_key.get_secret_value(), algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise jwt.InvalidTokenError("Token does not contain user ID")
        logger.info(f"Token verified successfully for user_id: {user_id}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired, user needs to log in again")
        raise
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e} - rejecting request")
        raise


