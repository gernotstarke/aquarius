"""CLI helper for creating and deleting test users for E2E testing."""

import sys
import os
from datetime import timedelta

# Add the app directory to path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, DATABASE_URL
from app import models, auth


def create_test_user(username: str = "e2e_test_user", password: str = "test_password_123"):
    """Create a test user for E2E testing and return username."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Check if user already exists
        existing = db.query(models.User).filter(models.User.username == username).first()
        if existing:
            db.delete(existing)
            db.commit()

        # Create new test user with full app permissions
        hashed_password = auth.get_password_hash(password)
        test_user = models.User(
            username=username,
            full_name="E2E Test User",
            hashed_password=hashed_password,
            role="APP_USER",
            is_active=True,
            is_app_user=True,
            can_read_all=True,
            can_write_all=True,
        )
        db.add(test_user)
        db.commit()

        print(f"OK:{username}:{password}")
        return username

    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)
    finally:
        db.close()


def delete_test_user(username: str = "e2e_test_user"):
    """Delete a test user."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user:
            db.delete(user)
            db.commit()

        print(f"OK:deleted")
        return True

    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)
    finally:
        db.close()


def get_user_token(username: str, password: str):
    """Get JWT token for a test user (called from E2E setup)."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user or not auth.verify_password(password, user.hashed_password):
            print(f"ERROR:Invalid credentials")
            sys.exit(1)

        # Generate token
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        print(f"OK:{access_token}")
        return access_token

    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_user_cli.py <create|delete|token> [username] [password]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        username = sys.argv[2] if len(sys.argv) > 2 else "e2e_test_user"
        password = sys.argv[3] if len(sys.argv) > 3 else "test_password_123"
        create_test_user(username, password)

    elif command == "delete":
        username = sys.argv[2] if len(sys.argv) > 2 else "e2e_test_user"
        delete_test_user(username)

    elif command == "token":
        username = sys.argv[2] if len(sys.argv) > 2 else "e2e_test_user"
        password = sys.argv[3] if len(sys.argv) > 3 else "test_password_123"
        get_user_token(username, password)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
