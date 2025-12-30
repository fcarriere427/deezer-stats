"""FastAPI application entry point."""

from fastapi import FastAPI

from deezer_stats import __version__
from deezer_stats.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="Personal Deezer data exploration API",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": __version__}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check for monitoring."""
    return {"status": "healthy"}
