from http import HTTPStatus

import pytest
from httpx import AsyncClient

from fastapi_crud_demo.models.team import TeamCreate, TeamUpdate


@pytest.mark.asyncio
async def test_list_all(client: AsyncClient, create_team):
    team1 = await create_team(name="Team 1", description="Team 1 description")
    team2 = await create_team(name="Team 2", description="Team 2 description")

    response = await client.get(url="/api/team/")

    assert response.status_code == HTTPStatus.OK
    teams = response.json()
    assert len(teams) == 2

    assert teams[0] == {**team1.model_dump(), "id": str(team1.id)}
    assert teams[1] == {**team2.model_dump(), "id": str(team2.id)}


@pytest.mark.asyncio
async def test_get(client: AsyncClient, create_team):
    team = await create_team(name="Team 1", description="Team 1 description")

    response = await client.get(url=f"/api/team/{team.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": str(team.id),
        "name": "Team 1",
        "description": "Team 1 description",
    }


@pytest.mark.asyncio
async def test_create(client: AsyncClient):
    payload = TeamCreate(
        name="New Team",
        description="New Team description"
    )
    response = await client.post(
        url="/api/team/",
        content=payload.model_dump_json(),
    )

    assert response.status_code == HTTPStatus.CREATED
    response_model = response.json()
    assert response_model["id"] is not None
    assert len(response_model["id"]) == 36
    assert response_model["name"] == "New Team"
    assert response_model["description"] == "New Team description"


@pytest.mark.asyncio
async def test_update(client: AsyncClient, create_team):
    team = await create_team(name="Team 1", description="Team 1 description")

    payload = TeamUpdate(
        name="Team 1 Updated",
        description="Team 1 Description Updated",
    )

    response = await client.patch(
        f"/api/team/{team.id}",
        content=payload.model_dump_json(),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": str(team.id),
        "name": "Team 1 Updated",
        "description": "Team 1 Description Updated",
    }


@pytest.mark.asyncio
async def test_delete(client: AsyncClient, create_team):
    team = await create_team(name="Team 1", description="Team 1 description")

    response = await client.delete(f"/api/team/{team.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT
