from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, monitored_apis, incidents
from app.monitoring.scheduler import start_scheduler, stop_scheduler


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

app.include_router(auth.router)
app.include_router(monitored_apis.router)
app.include_router(incidents.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "environment": settings.environment}