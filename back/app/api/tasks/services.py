from bson import ObjectId
from app.api.tasks.models import TaskModel, TaskUpdateModel
from app.infrastructure.database.mongodb import MongoDB
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.infrastructure.redis.rediscache import RedisCache
import json
import datetime
import logging

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.get_collection("tasks")
        self.redis = RedisCache()

    def get_all_tasks(self):

        user_id = get_jwt_identity()

        cache_key = f"tasks:{user_id}"
        # self.redis.delete(cache_key)
        cached_tasks = self.redis.get(cache_key)

        if cached_tasks:
            return eval(
                str(cached_tasks),
                {"datetime": datetime, "TaskModel": TaskModel},
                dict(),
            )

        tasks = []
        for task in self.collection.find({"user_id": user_id}):
            task["_id"] = str(task["_id"])
            tasks.append(TaskModel(**task).model_dump())

        self.redis.set(cache_key, tasks)
        return tasks

    def get_task(self, task_id):
        user_id = get_jwt_identity()

        cache_key = f"tasks:{user_id}"
        cached_tasks = self.redis.get(cache_key)

        if cached_tasks:
            tasks = eval(
                str(cached_tasks),
                {"datetime": datetime, "TaskModel": TaskModel},
                dict(),
            )
            # Buscar a tarefa pelo task_id na lista de tarefas
            print(f"tasks: {tasks}")
            for task in tasks:
                if str(task.get("id", None)) == str(task_id):
                    return task

        tasks = []
        found_task = None
        for task in self.collection.find({"user_id": user_id}):
            task["_id"] = str(task["_id"])
            tasks.append(TaskModel(**task).model_dump())
            if str(task_id) == task["_id"]:
                found_task = task

        self.redis.set(cache_key, tasks)

        return found_task

    def create_task(self, task: TaskModel):
        task_dict = task.dict(by_alias=True, exclude={"id"})
        print(f"task_dict: {task_dict}")
        result = self.collection.insert_one(task_dict)
        print(f"result: {result}")
        created_task = self.collection.find_one({"_id": result.inserted_id})
        print(f"created_task: {created_task}")
        return TaskModel(**created_task)

    def update_task(self, task_id, task_update: TaskUpdateModel):
        # Remove campos None
        update_data = {
            k: v
            for k, v in task_update.dict(exclude_unset=True).items()
            if v is not None
        }

        if update_data:
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": update_data}
            )

            if result.modified_count:
                return self.get_task(task_id)

        return None

    def delete_task(self, task_id):
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0
