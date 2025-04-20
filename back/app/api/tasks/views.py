import logging

logger = logging.getLogger(__name__)
from datetime import datetime

from flask import request
from flask_restful import Resource
from bson.errors import InvalidId

from app.api.tasks.models import TaskModel, TaskUpdateModel
from app.api.tasks.services import TaskService
from flask_jwt_extended import jwt_required, get_jwt_identity

task_service = TaskService()


class TaskView(Resource):

    @jwt_required()
    def get(self, task_id=None):
        if task_id:
            try:
                task = task_service.get_task(task_id)
                if task:
                    return task.dict(by_alias=True), 200
                    return task.dict(by_alias=True), 200
                return {"message": "Tarefa não encontrada"}, 404
            except InvalidId:
                return {"message": "ID de tarefa inválido"}, 400
        else:
            tasks = task_service.get_all_tasks()
            return tasks, 200

    @jwt_required()
    def post(self):
        try:
            task_data = request.get_json()
            task = TaskModel(**task_data)
            created_task = task_service.create_task(task)
            return created_task.model_dump(), 201
        except Exception as e:
            return {"message": f"Erro ao criar tarefa: {str(e)}"}, 400

    @jwt_required()
    def put(self, task_id):
        try:
            task_data = request.get_json()
            task_update = TaskUpdateModel(**task_data)
            updated_task = task_service.update_task(task_id, task_update)

            if updated_task:
                return updated_task.dict(by_alias=True), 200
            return {"message": "Tarefa não encontrada"}, 404
        except InvalidId:
            return {"message": "ID de tarefa inválido"}, 400
        except Exception as e:
            return {"message": f"Erro ao atualizar tarefa: {str(e)}"}, 400

    @jwt_required()
    def delete(self, task_id):
        try:
            if task_service.delete_task(task_id):
                return {"message": "Tarefa excluída com sucesso"}, 200
            return {"message": "Tarefa não encontrada"}, 404
        except InvalidId:
            return {"message": "ID de tarefa inválido"}, 400
        except Exception as e:
            return {"message": f"Erro ao excluir tarefa: {str(e)}"}, 400


def init_routes(api):
    api.add_resource(
        TaskView,
        "/api/tasks",
        "/api/tasks/<task_id>",
    )
