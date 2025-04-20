from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import bcrypt
from .models import UserModel, UserResponse
from app.infrastructure.database.mongodb import MongoDB
from app.infrastructure.redis.rediscache import RedisCache


class UserResource(Resource):
    def __init__(self, **kwargs):
        self.db = MongoDB()
        self.redis = RedisCache()
        self.collection = self.db.get_collection("users")

    def post(self):
        try:
            data = request.get_json()

            # Verificar se o email já está em uso
            if self.collection.find_one({"email": data["email"]}):
                return {"message": "Este email já está em uso"}, 400

            # Verificar se o username já está em uso
            if self.collection.find_one({"username": data["username"]}):
                return {"message": "Este nome de usuário já está em uso"}, 400

            # Hash da senha
            password = data["password"].encode("utf-8")
            salt = bcrypt.gensalt()
            data["password"] = bcrypt.hashpw(password, salt).decode("utf-8")

            # Validar dados com Pydantic
            user = UserModel(**data)

            # Inserir no MongoDB
            result = self.collection.insert_one(user.model_dump())

            # Retornar usuário criado (sem a senha)
            created_user = self.collection.find_one({"_id": result.inserted_id})
            created_user["_id"] = str(created_user["_id"])
            del created_user["password"]
            del created_user["created_at"]

            return created_user, 201
        except Exception as e:
            return {"message": f"Erro ao criar usuário: {str(e)}"}, 500

    @jwt_required()
    def get(self, user_id=None):
        try:
            # Se nenhum ID for fornecido, retornar o usuário atual
            if not user_id:
                user_id = get_jwt_identity()

            # Verificar se o usuário tem permissão para visualizar este perfil
            if user_id != get_jwt_identity():
                return {"message": "Acesso não autorizado"}, 403

            # Buscar usuário no MongoDB
            user = self.collection.find_one({"_id": ObjectId(user_id)})

            if not user:
                return {"message": "Usuário não encontrado"}, 404

            # Validar e formatar resposta com Pydantic
            user["_id"] = str(user["_id"])
            response = UserResponse(**user).dict()

            return response, 200
        except Exception as e:
            return {"message": f"Erro ao buscar usuário: {str(e)}"}, 500

    @jwt_required()
    def put(self, user_id=None):
        try:
            # Se nenhum ID for fornecido, atualizar o usuário atual
            if not user_id:
                user_id = get_jwt_identity()

            # Verificar se o usuário tem permissão para atualizar este perfil
            if user_id != get_jwt_identity():
                return {"message": "Acesso não autorizado"}, 403

            data = request.get_json()

            # Não permitir alteração de email ou senha por esta rota/
            if "email" in data or "password" in data:
                return {
                    "message": "Não é possível alterar email ou senha por esta rota"
                }, 400

            # Atualizar no MongoDB
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})

            # Retornar usuário atualizado
            updated_user = self.collection.find_one({"_id": ObjectId(user_id)})
            updated_user["_id"] = str(updated_user["_id"])
            del updated_user["password"]

            return updated_user, 200
        except Exception as e:
            return {"message": f"Erro ao atualizar usuário: {str(e)}"}, 500


def init_routes(api):
    api.add_resource(UserResource, "/api/users", "/api/users/<string:user_id>")
