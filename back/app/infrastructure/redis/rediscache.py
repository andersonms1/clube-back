import json
import redis
from datetime import datetime
from bson import ObjectId
from app.config import BaseConfig as Config


class RedisCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisCache, cls).__new__(cls)
            cls._instance.redis_client = redis.from_url(
                Config.REDIS_URI, password=Config.DOCKER_REDIS_PASSWORD
            )
        return cls._instance

    def set(self, key, value, expiration=Config.REDIS_EXPIRATION):
        """Armazena um valor no cache com expiração"""
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
