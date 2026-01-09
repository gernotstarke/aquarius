from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: str = "OFFIZIELLER"
    is_active: bool = True
    totp_enabled: bool = False
    is_app_user: Optional[bool] = False
    can_read_all: Optional[bool] = True
    can_write_all: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_app_user: Optional[bool] = None
    can_read_all: Optional[bool] = None
    can_write_all: Optional[bool] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    requires_2fa_setup: Optional[bool] = None
    warning: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
