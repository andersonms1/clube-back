import json
import pytest
from bson import ObjectId
import bcrypt
from datetime import datetime, UTC
from unittest.mock import patch
from app.api.auth.services import send_password_reset_email


class TestAuthEndpoints:
    """Test class for auth endpoints."""

    def test_login_success(self, client, mongodb, test_user):
        """Test successful login."""
        # Prepare login data
        login_data = {
            "email": test_user.email,
            "password": "password123",  # This matches the password in the test_user fixture
        }

        # Send login request
        response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify token and user data
        assert "access_token" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == test_user.email
        assert response_data["user"]["username"] == test_user.username

    def test_login_invalid_credentials(self, client, mongodb, test_user):
        """Test login with invalid credentials."""
        # Prepare login data with wrong password
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword",
        }

        # Send login request
        response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "inválidos" in response_data["message"]

    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        # Prepare login data with missing password
        login_data = {
            "email": "test@example.com",
        }

        # Send login request
        response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "obrigatórios" in response_data["message"]

    def test_logout(self, client, auth_headers, redis_cache):
        """Test logout functionality."""
        # Send logout request
        response = client.post(
            "/api/auth/logout",
            headers=auth_headers,
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "sucesso" in response_data["message"]

        # Verify JWT is in blocklist
        jwt_token = auth_headers["Authorization"].split(" ")[1]
        jti = jwt_token.split(".")[
            2
        ]  # This is a simplification, actual JTI extraction is more complex

        # Check if the token is in the blocklist
        blocklist_key = f"blocklist:{jti}"
        assert redis_cache.get(blocklist_key) is not None

    def test_password_reset_request(self, client, test_user, redis_cache):
        """Test password reset request."""
        # Mock the email sending function to avoid actual email sending
        with patch(
            "app.api.auth.services.send_password_reset_email", return_value=True
        ) as mock_send_email:
            # Prepare reset request data
            reset_data = {
                "email": test_user.email,
            }

            # Send reset request
            response = client.post(
                "/api/auth/reset-password",
                data=json.dumps(reset_data),
                content_type="application/json",
            )

            # Assert response
            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert "message" in response_data
            assert "receberá um link" in response_data["message"]

            # Verify email was "sent"
            mock_send_email.assert_called_once()

            # Check if a reset token was stored in Redis
            # We can't directly check the token since it's generated randomly
            # But we can check if any key with the prefix exists
            keys = redis_cache.redis_client.keys("password_reset:*")
            assert len(keys) > 0

    def test_password_reset_nonexistent_email(self, client, redis_cache):
        """Test password reset request with non-existent email."""
        # Mock the email sending function
        with patch(
            "app.api.auth.services.send_password_reset_email", return_value=True
        ) as mock_send_email:
            # Prepare reset request data with non-existent email
            reset_data = {
                "email": "nonexistent@example.com",
            }

            # Send reset request
            response = client.post(
                "/api/auth/reset-password",
                data=json.dumps(reset_data),
                content_type="application/json",
            )

            # Assert response - should still be 200 for security reasons
            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert "message" in response_data
            assert "receberá um link" in response_data["message"]

            # Verify email was NOT sent
            mock_send_email.assert_not_called()

            # Check that no reset token was stored
            keys = redis_cache.redis_client.keys("password_reset:*")
            assert len(keys) == 0

    def test_password_reset_with_token(
        self, client, redis_with_reset_token, reset_token, test_user, mongodb
    ):
        """Test password reset with token."""
        # Prepare new password data
        new_password_data = {
            "password": "newpassword123",
        }

        # Send password reset request with token
        response = client.post(
            f"/api/auth/reset-password/{reset_token}",
            data=json.dumps(new_password_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "sucesso" in response_data["message"]

        # Verify password was updated in the database
        updated_user = mongodb.get_collection("users").find_one(
            {"_id": ObjectId(test_user.id)}
        )
        assert updated_user is not None

        # Verify the password was changed by checking if we can login with the new password
        login_data = {
            "email": test_user.email,
            "password": "newpassword123",
        }

        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json",
        )

        assert login_response.status_code == 200

    def test_password_reset_invalid_token(self, client):
        """Test password reset with invalid token."""
        # Prepare new password data
        new_password_data = {
            "password": "newpassword123",
        }

        # Send password reset request with invalid token
        response = client.post(
            "/api/auth/reset-password/invalid-token",
            data=json.dumps(new_password_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert "inválido ou expirado" in response_data["message"]
