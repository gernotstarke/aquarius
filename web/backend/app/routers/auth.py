from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app import schemas, models, auth, totp

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


# Pydantic models for TOTP
class TOTPSetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: list[str]


class TOTPVerifyRequest(BaseModel):
    code: str


class TOTPEnableRequest(BaseModel):
    code: str


class BackupCodeVerifyRequest(BaseModel):
    backup_code: str


class TOTPLoginRequest(BaseModel):
    username: str
    password: str
    code: str


class BackupCodeLoginRequest(BaseModel):
    username: str
    password: str
    backup_code: str


class TOTPStatusResponse(BaseModel):
    totp_enabled: bool
    totp_setup_at: datetime | None
    requires_setup: bool


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if ROOT user requires 2FA setup or verification
    if user.role == "ROOT":
        if not user.totp_enabled:
            # ROOT user without 2FA - allow login but flag for setup
            access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = auth.create_access_token(
                data={"sub": user.username, "totp_verified": False},
                expires_delta=access_token_expires
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "requires_2fa_setup": True
            }
        else:
            # ROOT user with 2FA enabled - require TOTP code
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="TOTP code required",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Non-ROOT users - normal login
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/totp/verify", response_model=schemas.Token)
async def verify_totp_and_login(
    request: TOTPLoginRequest,
    db: Session = Depends(get_db)
):
    """Verify username/password + TOTP code and return access token."""
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.totp_enabled or not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not enabled for this user",
        )

    # Verify TOTP code
    if not totp.verify_totp_code(user.totp_secret, request.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP code",
        )

    # Success - generate token with totp_verified=true
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "totp_verified": True},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/totp/verify-backup", response_model=schemas.Token)
async def verify_backup_code_and_login(
    request: BackupCodeLoginRequest,
    db: Session = Depends(get_db)
):
    """Verify username/password + backup code and return access token."""
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.backup_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No backup codes available",
        )

    # Verify backup code
    is_valid, updated_codes = totp.verify_backup_code(user.backup_codes, request.backup_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid backup code",
        )

    # Update user's backup codes (remove used code)
    user.backup_codes = updated_codes
    db.commit()

    # Success - generate token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "totp_verified": True},
        expires_delta=access_token_expires
    )

    remaining = totp.get_remaining_backup_codes_count(updated_codes)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "warning": f"Backup code used. {remaining} codes remaining."
    }


@router.post("/totp/setup", response_model=TOTPSetupResponse)
async def setup_totp(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate TOTP secret and QR code for initial setup."""
    # Generate new secret and backup codes
    secret = totp.generate_totp_secret()
    qr_code = totp.generate_qr_code(secret, current_user.username)
    backup_codes = totp.generate_backup_codes(10)

    # Store secret temporarily (not enabled yet)
    current_user.totp_secret = secret
    current_user.backup_codes = totp.hash_backup_codes(backup_codes)
    db.commit()

    return {
        "secret": secret,
        "qr_code": qr_code,
        "backup_codes": backup_codes
    }


@router.post("/totp/enable")
async def enable_totp(
    request: TOTPEnableRequest,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enable TOTP after verifying the first code."""
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TOTP setup not initiated. Call /totp/setup first.",
        )

    # Verify the code
    if not totp.verify_totp_code(current_user.totp_secret, request.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP code",
        )

    # Enable TOTP
    current_user.totp_enabled = True
    current_user.totp_setup_at = datetime.utcnow()
    db.commit()

    return {"success": True, "message": "2FA enabled successfully"}


@router.get("/totp/status", response_model=TOTPStatusResponse)
async def get_totp_status(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get TOTP status for current user."""
    return {
        "totp_enabled": current_user.totp_enabled,
        "totp_setup_at": current_user.totp_setup_at,
        "requires_setup": current_user.role == "ROOT" and not current_user.totp_enabled
    }


@router.post("/totp/disable")
async def disable_totp(
    password: str,
    code: str,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Disable TOTP (requires password + current TOTP code)."""
    # Verify password
    if not auth.verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Verify TOTP code
    if not current_user.totp_secret or not totp.verify_totp_code(current_user.totp_secret, code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP code",
        )

    # Disable TOTP
    current_user.totp_enabled = False
    current_user.totp_secret = None
    current_user.backup_codes = None
    current_user.totp_setup_at = None
    db.commit()

    return {"success": True, "message": "2FA disabled"}


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user


@router.get("/app-me", response_model=schemas.User)
async def read_app_users_me(current_user: models.User = Depends(auth.get_current_app_user)):
    return current_user
