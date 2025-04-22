import uuid
import bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from bson import ObjectId
from . import services
from .models import PasswordResetModel
from app.infrastructure.database.mongodb import MongoDB
from app.infrastructure.redis.rediscache import RedisCache
import traceback
import logging

logger = logging.getLogger(__name__)


class LoginResource(Resource):
    def __init__(self, **kwargs):
        self.db = MongoDB()
        self.redis = RedisCache()
        self.collection = self.db.get_collection("users")

    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return {"message": "Email e senha são obrigatórios"}, 400

            # Buscar usuário no MongoDB
            user = self.collection.find_one({"email": email})

            if not user:
                return {"message": "Email ou senha inválidos"}, 401

            # Verificar senha
            if not bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            ):
                return {"message": "Email ou senha inválidos "}, 401

            # Criar token JWT com identity sendo o ID do usuário em string
            user_id = str(user["_id"])
            access_token = create_access_token(identity=user_id)

            return {
                "access_token": access_token,
                "user": {
                    "id": user_id,
                    "email": user["email"],
                    "username": user["username"],
                },
            }, 200
        except Exception as e:
            return {"message": f"Erro ao fazer login: {str(e)}"}, 500


class LogoutResource(Resource):
    def __init__(self, **kwargs):
        self.db = MongoDB()
        self.redis = RedisCache()
        self.collection = self.db.get_collection("users")

    @jwt_required()
    def post(self):
        try:
            # Obter o JTI (JWT ID) para blocklist
            jti = get_jwt()["jti"]

            # Armazenar JTI no Redis com TTL igual ao tempo de expiração do token
            self.redis.set(f"blocklist:{jti}", "1")

            return {"message": "Logout realizado com sucesso"}, 200
        except Exception as e:
            return {"message": f"Erro ao fazer logout: {str(e)}"}, 500


class PasswordResetRequestResource(Resource):
    def __init__(self, **kwargs):
        self.db = MongoDB()
        self.redis = RedisCache()
        self.collection = self.db.get_collection("users")

    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")

            if not email:
                return {"message": "Email é obrigatório"}, 400

            # Validar dados com Pydantic
            user = PasswordResetModel(email=email)

            # Buscar usuário no MongoDB
            user = self.collection.find_one({"email": email})

            if not user:
                # Não revelamos se o email existe ou não por razões de segurança
                return {
                    "message": "Se seu email estiver registrado, você receberá um link para redefinir sua senha"
                }, 200

            # Gerar token de redefinição
            reset_token = str(uuid.uuid4())
            user_id = str(user["_id"])

            # Armazenar token no Redis com TTL
            redis_key = f"password_reset:{reset_token}"
            self.redis.set(redis_key, user_id, "PASSWORD_RESET_TOKEN_EXPIRES")

            return {"reset_token": reset_token}, 200

            # Enviar email
            if services.send_password_reset_email(email, reset_token):
                return {
                    "message": "Se seu email estiver registrado, você receberá um link para redefinir sua senha"
                }, 200
            else:
                return {"message": "Erro ao enviar email de redefinição"}, 500
        except Exception as e:
            logger.error(traceback.format_exc())

            return {"message": f"Erro ao solicitar redefinição de senha: {str(e)}"}, 500


class PasswordResetResource(Resource):
    def __init__(self, **kwargs):
        self.db = MongoDB()
        self.redis = RedisCache()
        self.collection = self.db.get_collection("users")

    def post(self, token):
        try:
            data = request.get_json()
            password = data.get("password")

            if not password:
                return {"message": "Nova senha é obrigatória"}, 400

            # Verificar se o token existe no Redis
            redis_key = f"password_reset:{token}"
            user_id = self.redis.get(redis_key)

            if not user_id:
                return {"message": "Token inválido ou expirado"}, 400

            # Hash da nova senha
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            # Atualizar senha no MongoDB
            self.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"password": hashed_password}}
            )

            # Remover token do Redis
            self.redis.delete(redis_key)

            return {"message": "Senha redefinida com sucesso"}, 200
        except Exception as e:
            return {"message": f"Erro ao redefinir senha: {str(e)}"}, 500


def init_routes(api):
    api.add_resource(
        LoginResource,
        "/api/auth/login",
    )
    api.add_resource(
        LogoutResource,
        "/api/auth/logout",
    )
    api.add_resource(
        PasswordResetRequestResource,
        "/api/auth/reset-password",
    )
    api.add_resource(
        PasswordResetResource,
        "/api/auth/reset-password/<string:token>",
    )
