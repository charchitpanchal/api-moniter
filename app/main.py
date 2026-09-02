from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Liveness check — is the app process alive."""
    return {"status": "ok", "environment": settings.environment}