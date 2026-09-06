from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, monitored_apis, incidents
from app.monitoring.scheduler import start_scheduler, stop_scheduler
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
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