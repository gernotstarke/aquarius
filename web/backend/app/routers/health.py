import os
import time
import platform
import psutil
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app import schemas, auth, models

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
)

START_TIME = time.time()

@router.get("/")
async def health_check(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """
    Get system health status. 
    Requires Admin privileges.
    """
    
    # 1. Uptime
    current_time = time.time()
    uptime_seconds = current_time - START_TIME
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    
    # 2. Database Connection & Stats
    db_status = "ok"
    db_latency = 0
    db_size_bytes = 0
    table_count = 0
    
    try:
        start_db = time.time()
        # Basic check
        db.execute(text("SELECT 1"))
        db_latency = (time.time() - start_db) * 1000  # ms
        
        # SQLite Stats
        # Get table count (excluding sqlite internal tables)
        table_count = db.execute(text("SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")).scalar()
        
        # Get DB size (page_count * page_size)
        page_count = db.execute(text("PRAGMA page_count")).scalar()
        page_size = db.execute(text("PRAGMA page_size")).scalar()
        if page_count and page_size:
            db_size_bytes = page_count * page_size
            
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    # 3. System Info
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    
    # Detect database type from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./aquarius.db")
    db_type = "turso" if database_url.startswith(("libsql://", "sqlite+libsql://")) else "sqlite"

    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": uptime_str,
        "system": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_usage_mb": round(memory_usage, 2),
        },
        "database": {
            "status": db_status,
            "latency_ms": round(db_latency, 2),
            "type": db_type,
            "size_bytes": db_size_bytes,
            "table_count": table_count
        }
    }
