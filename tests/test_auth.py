"""Tests for authentication endpoints."""


class TestRegister:
    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "securepass123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data

    def test_register_duplicate_email(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "email": test_user["email"],
                "username": "different",
                "password": "securepass123",
            },
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "email": "different@example.com",
                "username": test_user["username"],
                "password": "securepass123",
            },
        )
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        response = client.post(
            "/auth/register",
            json={
                "email": "not-an-email",
                "username": "validuser",
                "password": "securepass123",
            },
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "validuser",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={
                "username": test_user["username"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={
                "username": test_user["username"],
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    def test_login_wrong_username(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent",
                "password": test_user["password"],
            },
        )
        assert response.status_code == 401
