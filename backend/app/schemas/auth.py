from datetime import datetime
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    locale: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = None
    updated_at: datetime = None

class Token(BaseModel):
    access_token: str
    token_type: str