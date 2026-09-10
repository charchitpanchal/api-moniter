from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.api.routes import auth, monitored_apis, incidents
from app.monitoring.scheduler import start_scheduler, stop_scheduler
from app.exceptions.handlers import register_exception_handlers
from app.db.database import SessionLocal
from app.cache.client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    description=(
        "A production-style backend that monitors external APIs, detects "
        "outages, manages incident lifecycles, and uses AI to explain root "
        "causes and recommend fixes. Built with FastAPI, PostgreSQL, Redis, "
        "and an LLM-powered analysis layer."
    ),
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
    contact={"name": "Charchit Panchal", "url": "https://github.com/charchitpanchal/api-moniter"},
)

origins = [origin.strip() for origin in settings.allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(monitored_apis.router)
app.include_router(incidents.router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Liveness check — is the app process alive."""
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check — verifies the app can actually serve traffic right now
    by confirming PostgreSQL and Redis are reachable.
    """
    checks = {"database": False, "redis": False}

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = True
    except Exception:
        pass

    try:
        await redis_client.ping()
        checks["redis"] = True
    except Exception:
        pass

    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503

    return JSONResponse(
        status_code=status_code,
        content={"ready": all_ready, "checks": checks},
    )