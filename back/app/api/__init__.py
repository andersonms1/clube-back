from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .tasks import views as tasks_routes
from .users import views as users_routes
from .auth import views as auth_routes
from app.infrastructure.database.init import init_mongodb
from app.config import config_by_name
from app.infrastructure.redis.init import init_redis as init_redis_with_config

import logging

logger = logging.getLogger(__name__)


def create_app(config_name="development"):
    configuration = config_by_name.get(config_name)
    app = Flask(__name__)

    # Set the environment in the app configuration
    app.config["ENV"] = config_name

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    mongo = _init_mongodb(app)
    redis_client = init_redis(configuration)

    # Configuração JWT
    app.config["JWT_SECRET_KEY"] = configuration.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = configuration.JWT_ACCESS_TOKEN_EXPIRES

    jwt = JWTManager(app)

    # Configuração do callback do JWT para verificar Token no Redis
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = redis_client.get(f"blocklist:{jti}")
        return token_in_redis is not None

    # Configuração do callback do JWT para adicionar claims ao token
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = mongo.get_collection("users").find_one({"_id": identity})
        if user:
            return {"username": user["username"], "email": user["email"]}
        return {}

    api = Api(app)
    tasks_routes.init_routes(api)
    users_routes.init_routes(api)
    auth_routes.init_routes(api)
    return app


def _init_mongodb(app):
    """
    Inicializa a conexão com o MongoDB

    Args:
        app: Instância da aplicação Flask
    """
    try:
        logger.info("Inicializando conexão com MongoDB...")
        # Get the current configuration
        config_name = app.config.get("ENV", "development")
        configuration = config_by_name.get(config_name)

        # Initialize MongoDB with the correct configuration
        mongodb = init_mongodb(configuration)

        # Testa a conexão com o banco de dados
        db = mongodb.get_database()
        app.mongodb = mongodb

        logger.info(f"MongoDB inicializado com sucesso. Banco de dados: {db.name}")
        return mongodb
    except Exception as e:
        logger.error(f"Erro ao inicializar MongoDB: {str(e)}")
        # Em produção, pode ser desejável tratar isso como um erro fatal
        if app.config.get("FLASK_ENV") == "production":
            raise


def init_redis(configuration):
    """Initialize Redis connection"""

    try:
        # Initialize Redis with the correct configuration
        redis_client = init_redis_with_config(configuration).redis_client

        # Test connection
        redis_client.ping()
        logger.info(f"Connected to Redis: {configuration.REDIS_URI}")

        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
