from app.lib.redis.rediscache import RedisCache


def init_redis(config):
    """
    Initialize Redis connection with the specified configuration

    Args:
        config: Configuration object with Redis settings

    Returns:
        RedisCache instance
    """
    redis_cache = RedisCache(config)
    return redis_cache
