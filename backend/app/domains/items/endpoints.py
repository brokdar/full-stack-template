"""HTTP endpoints for the items domain. Thin layer over the service.

NOTE: These example endpoints are unauthenticated. When you add auth, protect
your routers with a dependency (e.g. ``Depends(get_current_user)``) — don't
ship unauthenticated write endpoints to production.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.db import SessionDep
from app.core.pagination import PageParamsDep
from app.domains.items.repository import ItemRepository
from app.domains.items.schemas import ItemCreate, ItemRead, ItemsPage, ItemUpdate
from app.domains.items.service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


def get_service(session: SessionDep) -> ItemService:
    """Wire the service to a request-scoped session."""
    return ItemService(ItemRepository(session))


ServiceDep = Annotated[ItemService, Depends(get_service)]


@router.get("")
async def list_items(service: ServiceDep, page: PageParamsDep) -> ItemsPage:
    """List items, newest first."""
    return await service.list(page)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(service: ServiceDep, payload: ItemCreate) -> ItemRead:
    """Create a new item."""
    return await service.create(payload)


@router.get("/{item_id}")
async def get_item(service: ServiceDep, item_id: uuid.UUID) -> ItemRead:
    """Get a single item."""
    return await service.get(item_id)


@router.patch("/{item_id}")
async def update_item(
    service: ServiceDep, item_id: uuid.UUID, payload: ItemUpdate
) -> ItemRead:
    """Partially update an item."""
    return await service.update(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(service: ServiceDep, item_id: uuid.UUID) -> None:
    """Delete an item."""
    await service.delete(item_id)
