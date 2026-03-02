from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

# --- Schemas ---

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(
        min_length=3,
        max_length=50,
        description="Unique username for the user"
    )
    email: str = Field(
        min_length=5,
        max_length=100,
        description="Email address of the user"
    )
    password: str = Field(
        min_length=8,
        description="Password for the user account"
    )

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

