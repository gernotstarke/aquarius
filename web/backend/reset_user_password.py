"""
Reset user password for development.
Usage: python reset_user_password.py <username>
Sets the password for the user to their username.
"""
import sys
from app.database import SessionLocal
from app.models.user import User
from app.auth import get_password_hash

def reset_user_password(username: str):
    """Reset a user's password to their username."""
    db = SessionLocal()

    try:
        # Find user
        user = db.query(User).filter(User.username == username).first()

        if not user:
            print(f"❌ User '{username}' not found!")
            print("\n📋 Available users:")
            all_users = db.query(User).all()
            for u in all_users:
                print(f"   - {u.username} ({u.role})")
            return False

        # Reset password to username
        new_password = username
        user.hashed_password = get_password_hash(new_password)

        # Disable TOTP/2FA for easier development access
        totp_was_enabled = user.totp_enabled
        user.totp_enabled = False
        user.totp_secret = None
        user.backup_codes = None
        user.totp_setup_at = None

        db.commit()

        print(f"✅ Password reset successful!")
        print(f"   User: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   New password: {new_password}")
        if totp_was_enabled:
            print(f"   2FA/TOTP: Disabled (was enabled)")

        return True

    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reset_user_password.py <username>")
        print("Example: python reset_user_password.py admin")
        sys.exit(1)

    username = sys.argv[1]
    success = reset_user_password(username)
    sys.exit(0 if success else 1)
