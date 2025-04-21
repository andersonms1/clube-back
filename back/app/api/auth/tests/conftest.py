import pytest
import json
import os
from flask_jwt_extended import create_access_token
from app.api import create_app
from app.infrastructure.database.mongodb import MongoDB
from app.infrastructure.redis.rediscache import RedisCache
from app.api.users.models import UserModel
from datetime import datetime, timedelta, UTC
import uuid


@pytest.fixture
def reset_token():
    """Generate a password reset token."""
    return str(uuid.uuid4())


@pytest.fixture
def redis_with_reset_token(redis_cache, test_user, reset_token):
    """Redis with a stored reset token for testing."""
    from app.config import BaseConfig as Config

    # Store the reset token in Redis
    redis_cache.setex(
        f"password_reset:{reset_token}",
        Config.PASSWORD_RESET_EXPIRATION,
        str(test_user.id),
    )

    return redis_cache
