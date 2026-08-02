"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.domains.health.endpoints import router as health_router
from app.domains.items.endpoints import router as items_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application startup/shutdown."""
    configure_logging()
    get_logger(__name__).info("application_started")
    yield


def create_app() -> FastAPI:
    """Build the FastAPI application with all routers and middleware."""
    settings = get_settings()
    app = FastAPI(
        title=settings.application_name,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)

    # Unversioned health endpoint for Docker/load-balancer probes.
    app.include_router(health_router)

    api = APIRouter(prefix=settings.api_path)
    api.include_router(items_router)
    app.include_router(api)

    return app


app = create_app()
