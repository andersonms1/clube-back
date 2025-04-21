import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class BaseConfig:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = False
    TESTING = False

    # JWT
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "4b465a1a4b54b534071ec9b50097a87292d998a8a67cee27493852b77146d24e4c90a1a69d67d272518a09bf86f0dfda651db9dd19e1a213e89842ee1ca7faa6ce7fc9064125c2eea67415a6012e10c2e3a78a08a7a230e222d74d8fbf5abeeee67c8785c1a735f3960e8a12d3cb16b82cac90bb2bca9a6408d46ef687603b6623e0274c3f74b585ad44aa8465a2617388b316043f380a70c4da1f63d987bf99f918d1956ce001708979e79b584b0157920b07b3030a9507939f3986dba7adbf5c1ded98d93ee2c133d4c831724d220da248e6bac9799653aa3e3333a55c6a2826b17ee5dab6b6d8a530ca292e0550b77ee92b11bd27d0d5f537da4549e0c917",
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 300))
    )

    # MongoDB
    # MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/task_manager")
    MONGODB_URI = "mongodb://root:example@mongo:27017/tasks_manager?authSource=admin"
    MONGODB_DATABASE = "tasks_manager"
    # Redis
    REDIS_URI = os.getenv("REDIS_URI", "redis://redis:6379/0")
    DOCKER_REDIS_PASSWORD = os.getenv("DOCKER_REDIS_PASSWORD", "redis_password")
    REDIS_EXPIRATION = int(os.getenv("REDIS_EXPIRATION", "3600"))

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "t")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "t")

    # Application settings
    PASSWORD_RESET_TOKEN_EXPIRES = int(
        os.getenv("PASSWORD_RESET_TOKEN_EXPIRES", 3600)
    )  # 1 hour


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""

    DEBUG = True
    TESTING = True
    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb://root:example@mongo:27017/tasks_manager_test?authSource=admin",
    )
    MONGODB_DATABASE = "tasks_manager_test"
    REDIS_URI = os.getenv("REDIS_URI", "redis://redis:6379/1")
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    # In production, ensure all security-related environment variables are properly set


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
