"""Admin endpoints for system management."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.database import get_db
from app import auth, models

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
)


@router.get("/users/active-count")
async def get_active_user_count(
    minutes: int = 15,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """
    Get count of users active in the last X minutes.
    Defaults to 15 minutes.
    """
    since = datetime.utcnow() - timedelta(minutes=minutes)
    
    count = db.query(models.User).filter(
        models.User.last_active >= since
    ).count()
    
    return {
        "active_users": count,
        "window_minutes": minutes,
        "timestamp": datetime.utcnow()
    }


@router.get("/database/stats")
async def get_database_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Get statistics about all database tables."""
    # Get all table names from the models
    inspector = inspect(db.bind)
    table_names = inspector.get_table_names()

    stats = []

    # Define a mapping of table names to their corresponding models
    table_model_map = {
        "user": models.User,
        "verband": models.Verband,
        "verein": models.Verein,
        "saison": models.Saison,
        "schwimmbad": models.Schwimmbad,
        "wettkampf": models.Wettkampf,
        "kind": models.Kind,
        "figur": models.Figur,
        "anmeldung": models.Anmeldung,
        "versicherung": models.Versicherung,
    }

    for table_name in sorted(table_names):
        # Skip association tables (many-to-many relationship tables)
        if "_" in table_name and table_name not in table_model_map:
            continue

        model = table_model_map.get(table_name)
        if model:
            try:
                count = db.query(model).count()
                stats.append({
                    "table_name": table_name,
                    "count": count
                })
            except Exception:
                # Skip tables that cause errors
                continue

    return {"tables": stats}
