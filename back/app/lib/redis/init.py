from app.lib.redis.rediscache import RedisCache
import logging

logger = logging.getLogger(__name__)


def init_redis(configuration):
    """Initialize Redis connection"""

    try:
        # Initialize Redis with the correct configuration
        redis_client = RedisCache(configuration).redis_client

        # Test connection
        redis_client.ping()
        logger.info(f"Connected to Redis: {configuration.REDIS_URI}")

        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
