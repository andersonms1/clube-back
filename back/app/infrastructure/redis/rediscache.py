import json
import redis
from datetime import datetime
from bson import ObjectId


class RedisCache:
    _instances = {}
    _config = None

    def __new__(cls, config=None):
        # Use config as key for the instance to support different environments
        config_key = id(config) if config else "default"

        if config_key not in cls._instances:
            cls._instances[config_key] = super(RedisCache, cls).__new__(cls)
            cls._instances[config_key]._config = config
            cls._instances[config_key]._connect()
        return cls._instances[config_key]

    def _connect(self):
        """Establish connection to Redis"""
        if not self._config:
            from app.config import BaseConfig

            self._config = BaseConfig

        self.redis_client = redis.from_url(
            self._config.REDIS_URI, password=self._config.DOCKER_REDIS_PASSWORD
        )

    def set(self, key, value, expiration=None):
        """Armazena um valor no cache com expiração"""
        if expiration is None:
            expiration = self._config.REDIS_EXPIRATION

        serialized = json.dumps(value, default=self._json_serializer)
        self.redis_client.setex(key, expiration, serialized)

    def get(self, key):
        """Recupera um valor do cache"""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data, object_hook=self._json_deserializer)
        return None

    def delete(self, key):
        """Remove um valor do cache"""
        self.redis_client.delete(key)

    def clear_pattern(self, pattern):
        """Remove todos os valores que correspondem a um padrão"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

    def _json_serializer(self, obj):
        """Serializa tipos especiais para JSON"""
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.isoformat()}
        elif isinstance(obj, ObjectId):
            return {"__type__": "objectid", "value": str(obj)}
        raise TypeError(f"Objeto do tipo {obj.__class__.__name__} não é serializável")

    def _json_deserializer(self, obj):
        """Deserializa tipos especiais do JSON"""
        if "__type__" in obj:
            if obj["__type__"] == "datetime":
                return datetime.fromisoformat(obj["value"])
            elif obj["__type__"] == "objectid":
                return ObjectId(obj["value"])
        return obj
