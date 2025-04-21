import pytest
import json
import os
from flask_jwt_extended import create_access_token
from app.api import create_app
from app.infrastructure.database.mongodb import MongoDB
from app.infrastructure.redis.rediscache import RedisCache
from app.api.users.models import UserModel
from datetime import datetime, UTC
import bcrypt


@pytest.fixture
def second_test_user(mongodb):
    """Create a second test user for testing user interactions."""
    user_data = {
        "email": "second@example.com",
        "username": "seconduser",
        "password": bcrypt.hashpw(
            "password456".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    result = mongodb.get_collection("users").insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return UserModel(**user_data)


@pytest.fixture
def second_user_auth_headers(second_test_user):
    """Generate JWT token and headers for the second test user."""
    access_token = create_access_token(identity=str(second_test_user.id))
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers
