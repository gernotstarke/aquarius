from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="OFFIZIELLE") # ADMIN, CLEO, VERWALTUNG, OFFIZIELLE, TEILNEHMENDE
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 2FA / TOTP fields
    totp_secret = Column(String, nullable=True)  # Encrypted TOTP secret
    totp_enabled = Column(Boolean, default=False)  # Is 2FA enabled?
    backup_codes = Column(Text, nullable=True)  # JSON array of hashed backup codes
    totp_setup_at = Column(DateTime, nullable=True)  # When 2FA was enabled

    # Activity tracking
    last_active = Column(DateTime, nullable=True)

    # App user permissions (for non-admin users)
    is_app_user = Column(Boolean, default=False)  # Can access main app?
    can_read_all = Column(Boolean, default=True)  # Has read permission?
    can_write_all = Column(Boolean, default=False)  # Has write/edit permission?
