from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import verify_access_token
from database import utils as db_utils
from database.db import get_db
from sqlalchemy.orm import Session
from config import get_settings
import logging
from jwt import PyJWTError

settings = get_settings()
settings.setup_logging()
logger = logging.getLogger(__name__)

# This tells FastAPI to expect a Bearer token
security = HTTPBearer()
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> dict:

    """
    Dependency that extracts and verifies the JWT token.
    
    Runs before the route handler. If token is invalid,
    raises 401 and the route never executes.
    """

    token = credentials.credentials

    try:
        payload = verify_access_token(token)
        user = db_utils.get_user_by_id(db, int(payload["sub"]))
        
        if user is None:
            # This will now skip the next 'except' blocks and go straight to the client
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        elif user['is_active'] == False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
            
        return user

    # 1. Catch HTTPExceptions first and just re-raise them
    except HTTPException:
        raise

    except PyJWTError:
        # We know for sure it's a token problem
        raise HTTPException(status_code=401, detail="Token validation failed")
    except Exception as e:
        # This is a server/logic error, maybe a 500 is better here?
        logger.critical(f"System error in auth: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def require_role(required_role: str):
    """
    Factory that creates a role-checking dependency.
    
    Usage:
        @router.post("/admin-only")
        def admin_route(user: dict = Depends(require_role("admin"))):
            ...
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

