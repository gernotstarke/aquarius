from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os
import logging

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# App authentication mode
ENABLE_APP_AUTH = os.getenv("ENABLE_APP_AUTH", "false").lower() == "true"
DEFAULT_APP_USER = os.getenv("DEFAULT_APP_USER", "testuser")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
optional_http_bearer = HTTPBearer(auto_error=False)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last_active timestamp
    now = datetime.utcnow()
    # Only update if last_active is None or older than 60 seconds to reduce DB writes
    if not current_user.last_active or (now - current_user.last_active).total_seconds() > 60:
        current_user.last_active = now
        db.commit()
        
    return current_user

async def get_current_admin_user(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != "ROOT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to access admin resources"
        )
    return current_user


def get_or_create_default_app_user(db: Session) -> models.User:
    """Get or create default app user for development mode (ENABLE_APP_AUTH=false)."""
    user = db.query(models.User).filter(models.User.username == DEFAULT_APP_USER).first()
    
    if not user:
        user = models.User(
            username=DEFAULT_APP_USER,
            full_name="Default App User (Dev Mode)",
            hashed_password=get_password_hash("dev-password"),
            role="OFFIZIELLER",
            is_app_user=True,
            can_read_all=True,
            can_write_all=True,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


async def get_current_app_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_http_bearer),
) -> models.User:
    """
    Get current app user. 
    In dev mode (ENABLE_APP_AUTH=false), returns default app user if no token provided.
    In production (ENABLE_APP_AUTH=true), requires valid token.
    """
    token = credentials.credentials if credentials else None
    
    # Development mode: allow access without token using default user
    if not ENABLE_APP_AUTH:
        if not token:
            logger.info(f"App auth disabled, using default user: {DEFAULT_APP_USER}")
            return get_or_create_default_app_user(db)
    
    # Production mode: require valid token
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate token and get user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Check if user has app access (admin users always have access)
    if user.role != "ROOT" and not user.is_app_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access app resources",
        )
    
    return user


async def require_app_read_permission(
    current_user: models.User = Depends(get_current_app_user),
) -> models.User:
    """Require read permission for app operations."""
    # Admin (ROOT) always has read access
    if current_user.role == "ROOT":
        return current_user
    
    # App users must have read permission
    if not current_user.can_read_all:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No read permission",
        )
    
    return current_user


async def require_app_write_permission(
    current_user: models.User = Depends(get_current_app_user),
) -> models.User:
    """Require write permission for app operations (create, update, delete)."""
    # Admin (ROOT) always has write access
    if current_user.role == "ROOT":
        return current_user
    
    # App users must have write permission
    if not current_user.can_write_all:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No write permission",
        )
    
    return current_user
