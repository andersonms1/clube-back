import pytest
import json
import os
from flask_jwt_extended import create_access_token
from app.api import create_app
from app.infrastructure.database.mongodb import MongoDB
from app.infrastructure.redis.rediscache import RedisCache
from app.api.users.models import UserModel
from app.api.tasks.models import TaskModel
from datetime import datetime, timedelta, UTC


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # Create the app context
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def mongodb(app):
    """MongoDB connection for testing."""
    from app.config import config_by_name

    # Get the testing configuration
    config = config_by_name.get("testing")

    # Initialize MongoDB with the testing configuration
    from app.infrastructure.database.init import init_mongodb

    mongo = init_mongodb(config)

    # Clear test collections before each test
    mongo.get_collection("users").delete_many({})
    mongo.get_collection("tasks").delete_many({})
    return mongo


@pytest.fixture
def redis_cache(app):
    """Redis cache for testing."""
    from app.config import config_by_name

    # Get the testing configuration
    config = config_by_name.get("testing")

    # Initialize Redis with the testing configuration
    from app.infrastructure.redis.init import init_redis

    redis = init_redis(config)

    # Clear test cache before each test
    redis.redis_client.flushdb()
    return redis


@pytest.fixture
def test_user(mongodb):
    """Create a test user."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    result = mongodb.get_collection("users").insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return UserModel(**user_data)


@pytest.fixture
def auth_headers(test_user):
    """Generate JWT token and headers for the test user."""
    access_token = create_access_token(identity=str(test_user.id))
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers


@pytest.fixture
def test_task(mongodb, test_user):
    """Create a test task."""
    task_data = {
        "titulo": "Test Task",
        "descricao": "This is a test task",
        "status": "pending",
        "data_vencimento": datetime.now(UTC) + timedelta(days=1),
        "user_id": str(test_user.id),
    }

    result = mongodb.get_collection("tasks").insert_one(task_data)
    task_data["_id"] = result.inserted_id
    return TaskModel(**task_data)
