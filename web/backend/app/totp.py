"""
TOTP (Time-based One-Time Password) utility functions for 2FA.
Compatible with Google Authenticator, Authy, Microsoft Authenticator.
"""
import pyotp
import qrcode
import io
import base64
import json
import secrets
from passlib.context import CryptContext
from typing import List, Tuple

# Password context for hashing backup codes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TOTP Configuration
TOTP_ISSUER = "Aquarius Admin"


def generate_totp_secret() -> str:
    """
    Generate a new TOTP secret (base32 encoded).

    Returns:
        str: Base32 encoded secret key
    """
    return pyotp.random_base32()


def generate_qr_code(secret: str, username: str) -> str:
    """
    Generate a QR code for TOTP setup.

    Args:
        secret: The TOTP secret (base32)
        username: Username for the account

    Returns:
        str: Base64 encoded PNG image
    """
    # Create TOTP URI for Google Authenticator
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=username,
        issuer_name=TOTP_ISSUER
    )

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_base64}"


def verify_totp_code(secret: str, code: str) -> bool:
    """
    Verify a TOTP code against the secret.

    Args:
        secret: The TOTP secret (base32)
        code: The 6-digit code to verify

    Returns:
        bool: True if code is valid
    """
    totp = pyotp.TOTP(secret)
    # Allow for ±1 time window (90 seconds total)
    return totp.verify(code, valid_window=1)


def generate_backup_codes(count: int = 10) -> List[str]:
    """
    Generate backup codes for account recovery.

    Args:
        count: Number of backup codes to generate

    Returns:
        List[str]: List of backup codes (e.g., "ABCD-1234-EFGH")
    """
    codes = []
    for _ in range(count):
        # Generate 12-character code in format XXXX-XXXX-XXXX
        part1 = secrets.token_hex(2).upper()
        part2 = secrets.token_hex(2).upper()
        part3 = secrets.token_hex(2).upper()
        code = f"{part1}-{part2}-{part3}"
        codes.append(code)
    return codes


def hash_backup_codes(codes: List[str]) -> str:
    """
    Hash backup codes for secure storage.

    Args:
        codes: List of plain text backup codes

    Returns:
        str: JSON string of hashed codes
    """
    hashed = []
    for code in codes:
        hashed_code = pwd_context.hash(code)
        hashed.append(hashed_code)
    return json.dumps(hashed)


def verify_backup_code(hashed_codes_json: str, code: str) -> Tuple[bool, str]:
    """
    Verify a backup code and return updated list if valid.

    Args:
        hashed_codes_json: JSON string of hashed backup codes
        code: Plain text backup code to verify

    Returns:
        Tuple[bool, str]: (is_valid, updated_hashed_codes_json)
    """
    try:
        hashed_codes = json.loads(hashed_codes_json)
    except (json.JSONDecodeError, TypeError):
        return False, hashed_codes_json

    # Check each hashed code
    for i, hashed_code in enumerate(hashed_codes):
        if pwd_context.verify(code, hashed_code):
            # Valid code found - remove it (one-time use)
            hashed_codes.pop(i)
            updated_json = json.dumps(hashed_codes)
            return True, updated_json

    return False, hashed_codes_json


def get_remaining_backup_codes_count(hashed_codes_json: str) -> int:
    """
    Get count of remaining backup codes.

    Args:
        hashed_codes_json: JSON string of hashed backup codes

    Returns:
        int: Number of remaining codes
    """
    try:
        hashed_codes = json.loads(hashed_codes_json)
        return len(hashed_codes)
    except (json.JSONDecodeError, TypeError):
        return 0
