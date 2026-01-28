#!/usr/bin/env python3
"""
Interactive admin user creation script.
Production-safe with password validation.
"""
import getpass
import sys
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash


def main():
    print("This will create or update a ROOT admin user.")
    print("")

    # Get username
    username = input("Admin username [admin]: ").strip() or "admin"

    # Get password with validation loop
    while True:
        password = getpass.getpass("Admin password: ")

        password2 = getpass.getpass("Confirm password: ")

        if password != password2:
            print("❌ Passwords do not match")
            continue

        break

    # Create or update user
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()

        if user:
            user.hashed_password = get_password_hash(password)
            user.role = "ROOT"
            user.is_active = True
            db.commit()
            print("")
            print(f"✅ Updated password for user: {username}")
        else:
            user = User(
                username=username,
                full_name="System Administrator",
                hashed_password=get_password_hash(password),
                role="ROOT",
                is_active=True
            )
            db.add(user)
            db.commit()
            print("")
            print(f"✅ Created admin user: {username}")

        print("")
        print("Next steps:")
        print("  1. Log in at /admin/login")
        print("  2. Setup 2FA (when implemented)")
        print("  3. Save backup codes securely")

    finally:
        db.close()


if __name__ == "__main__":
    main()
