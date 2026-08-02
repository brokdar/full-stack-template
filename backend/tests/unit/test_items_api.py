"""CRUD flow tests for the example items domain."""

import uuid

from httpx import AsyncClient

ITEMS = "/api/v1/items"


async def _create(client: AsyncClient, name: str = "widget") -> dict:
    response = await client.post(ITEMS, json={"name": name, "description": "a thing"})
    assert response.status_code == 201
    return response.json()


async def test_create_returns_item_with_generated_fields(client: AsyncClient) -> None:
    item = await _create(client)

    assert item["name"] == "widget"
    assert item["description"] == "a thing"
    assert uuid.UUID(item["id"])
    assert item["created_at"]


async def test_create_duplicate_name_conflicts(client: AsyncClient) -> None:
    await _create(client)

    response = await client.post(ITEMS, json={"name": "widget"})

    assert response.status_code == 409


async def test_list_returns_page(client: AsyncClient) -> None:
    await _create(client, "one")
    await _create(client, "two")

    response = await client.get(ITEMS)

    assert response.status_code == 200
    page = response.json()
    assert page["total"] == 2
    assert {item["name"] for item in page["items"]} == {"one", "two"}


async def test_get_returns_item(client: AsyncClient) -> None:
    created = await _create(client)

    response = await client.get(f"{ITEMS}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "widget"


async def test_get_unknown_id_returns_404(client: AsyncClient) -> None:
    response = await client.get(f"{ITEMS}/{uuid.uuid4()}")

    assert response.status_code == 404


async def test_update_changes_fields(client: AsyncClient) -> None:
    created = await _create(client)

    response = await client.patch(
        f"{ITEMS}/{created['id']}", json={"description": "updated"}
    )

    assert response.status_code == 200
    assert response.json()["description"] == "updated"
    assert response.json()["name"] == "widget"


async def test_update_rename_to_taken_name_conflicts(client: AsyncClient) -> None:
    await _create(client, "taken")
    created = await _create(client, "renameme")

    response = await client.patch(f"{ITEMS}/{created['id']}", json={"name": "taken"})

    assert response.status_code == 409


async def test_delete_removes_item(client: AsyncClient) -> None:
    created = await _create(client)

    response = await client.delete(f"{ITEMS}/{created['id']}")
    assert response.status_code == 204

    response = await client.get(f"{ITEMS}/{created['id']}")
    assert response.status_code == 404
