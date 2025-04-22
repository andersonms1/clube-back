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
        "secret-key",
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
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
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Application settings
    PASSWORD_RESET_TOKEN_EXPIRES = int(
        os.getenv("PASSWORD_RESET_TOKEN_EXPIRES", 3600)
    )  # 1 hour

    FRONT_URL = os.getenv("FRONT_URL", "http://localhost:80")


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
