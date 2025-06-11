from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.api.tasks import views as tasks_routes
from app.api.users import views as users_routes
from app.api.auth import views as auth_routes
from app.lib.database.init import init_mongodb
from app.config import config_by_name
from app.lib.redis.init import init_redis

import logging

logger = logging.getLogger(__name__)


def create_app(config_name="development"):
    configuration = config_by_name.get(config_name)
    app = Flask(__name__)

    # Set the environment in the app configuration
    app.config["ENV"] = config_name

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    mongo = init_mongodb(app)
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
