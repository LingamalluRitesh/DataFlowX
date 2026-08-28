"""
Integration Tests: FastAPI REST Endpoints & Authentication
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_and_root_endpoints(client: AsyncClient):
    # Test Root
    res_root = await client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["status"] == "operational"

    # Test Health Probe
    res_health = await client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_registration_and_login_flow(client: AsyncClient):
    # 1. Register new user
    register_payload = {
        "email": "tester@dataflowx.io",
        "username": "tester",
        "full_name": "Test Engineer",
        "password": "SecurePassword123!"
    }
    reg_res = await client.post("/api/v1/auth/register", json=register_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    access_token = reg_data["access_token"]

    # 2. Login
    login_res = await client.post("/api/v1/auth/login", json={
        "username_or_email": "tester@dataflowx.io",
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data

    # 3. Call authenticated /me endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "tester@dataflowx.io"


@pytest.mark.asyncio
async def test_sources_and_connectors_api(client: AsyncClient):
    # Register & get auth token
    reg_res = await client.post("/api/v1/auth/register", json={
        "email": "src_tester@dataflowx.io",
        "username": "src_tester",
        "password": "Password123!"
    })
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # List connectors
    conn_res = await client.get("/api/v1/sources/connectors", headers=headers)
    assert conn_res.status_code == 200
    assert "postgres" in conn_res.json()
    assert "csv" in conn_res.json()
