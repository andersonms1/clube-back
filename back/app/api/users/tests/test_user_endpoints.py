import json
import pytest
from bson import ObjectId
import bcrypt
from datetime import datetime, UTC


class TestUserEndpoints:
    """Test class for user endpoints."""

    def test_create_user(self, client, mongodb):
        """Test creating a new user."""
        # Prepare user data
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepassword123",
        }

        # Send request to create user
        response = client.post(
            "/api/users",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 201
        response_data = json.loads(response.data)

        # Verify user was created in database
        created_user = mongodb.get_collection("users").find_one(
            {"email": "newuser@example.com"}
        )
        assert created_user is not None
        assert created_user["username"] == user_data["username"]

        # Verify password was hashed
        assert created_user["password"] != user_data["password"]
        assert bcrypt.checkpw(
            user_data["password"].encode("utf-8"),
            created_user["password"].encode("utf-8"),
        )

        # Verify response doesn't contain password
        assert "password" not in response_data

    def test_create_user_duplicate_email(self, client, test_user):
        """Test creating a user with an email that already exists."""
        # Prepare user data with existing email
        user_data = {
            "email": test_user.email,
            "username": "differentusername",
            "password": "securepassword123",
        }

        # Send request to create user
        response = client.post(
            "/api/users",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "email já está em uso" in response_data["message"]

    def test_create_user_duplicate_username(self, client, test_user):
        """Test creating a user with a username that already exists."""
        # Prepare user data with existing username
        user_data = {
            "email": "different@example.com",
            "username": test_user.username,
            "password": "securepassword123",
        }

        # Send request to create user
        response = client.post(
            "/api/users",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "nome de usuário já está em uso" in response_data["message"]

    def test_get_current_user(self, client, auth_headers, test_user):
        """Test retrieving the current user's profile."""
        # Send request to get current user
        response = client.get(
            "/api/users",
            headers=auth_headers,
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify user data
        assert response_data["email"] == test_user.email
        assert response_data["username"] == test_user.username
        assert "password" not in response_data

    def test_get_specific_user(self, client, auth_headers, test_user):
        """Test retrieving a specific user's profile."""
        # Send request to get specific user
        response = client.get(
            f"/api/users/{test_user.id}",
            headers=auth_headers,
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify user data
        assert response_data["email"] == test_user.email
        assert response_data["username"] == test_user.username
        assert "password" not in response_data

    def test_get_other_user_unauthorized(self, client, auth_headers, second_test_user):
        """Test retrieving another user's profile without authorization."""
        # Send request to get another user
        response = client.get(
            f"/api/users/{second_test_user.id}",
            headers=auth_headers,
        )

        # Assert response - should be forbidden
        assert response.status_code == 403
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "não autorizado" in response_data["message"].lower()

    def test_update_user(self, client, auth_headers, test_user, mongodb):
        """Test updating a user's profile."""
        # Prepare update data
        update_data = {
            "username": "updatedusername",
        }

        # Send request to update user
        response = client.put(
            "/api/users",
            headers=auth_headers,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify user was updated in database
        updated_user = mongodb.get_collection("users").find_one(
            {"_id": ObjectId(test_user.id)}
        )
        assert updated_user is not None
        assert updated_user["username"] == update_data["username"]

        # Verify response data
        assert response_data["username"] == update_data["username"]
        assert "password" not in response_data

    def test_update_user_with_email_password(self, client, auth_headers):
        """Test updating a user's email or password, which should be disallowed."""
        # Prepare update data with email and password
        update_data = {
            "email": "newemail@example.com",
            "password": "newpassword123",
        }

        # Send request to update user
        response = client.put(
            "/api/users",
            headers=auth_headers,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert response - should be bad request
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert (
            "não é possível alterar email ou senha" in response_data["message"].lower()
        )

    def test_update_other_user_unauthorized(
        self, client, auth_headers, second_test_user
    ):
        """Test updating another user's profile without authorization."""
        # Prepare update data
        update_data = {
            "username": "hackedusername",
        }

        # Send request to update another user
        response = client.put(
            f"/api/users/{second_test_user.id}",
            headers=auth_headers,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert response - should be forbidden
        assert response.status_code == 403
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "não autorizado" in response_data["message"].lower()
