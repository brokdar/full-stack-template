"""Integration test fixtures — require a real Postgres.

Run via `just test-int`, which starts the docker compose test database and
sets POSTGRES__* env vars before invoking pytest with this directory.
"""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings
from app.core.db import Base
from app.main import create_app


@pytest.fixture(scope="session", autouse=True)
def _fresh_settings() -> None:
    """Settings are cached at import time; clear so env vars apply."""
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
async def _clean_schema() -> AsyncIterator[None]:
    """Recreate the schema around every test for full isolation."""
    engine = create_async_engine(get_settings().postgres.async_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """HTTP client against the app using the real database."""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        yield http
