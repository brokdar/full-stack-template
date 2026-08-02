"""Request/response schemas for the items domain."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pagination import Page


class ItemCreate(BaseModel):
    """Payload for creating an item."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)


class ItemUpdate(BaseModel):
    """Payload for partially updating an item."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)


class ItemRead(BaseModel):
    """Item as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


ItemsPage = Page[ItemRead]
