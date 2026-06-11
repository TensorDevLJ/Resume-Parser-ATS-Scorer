import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepass123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First signup
        await ac.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepass123"
            }
        )
        
        # Then login
        response = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "securepass123"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
