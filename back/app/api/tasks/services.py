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
            print(f"Cached: {cached_tasks}")

            return eval(
                str(cached_tasks),
                {"datetime": datetime, "TaskModel": TaskModel},
                dict(),
            )

        tasks = []
        for task in self.collection.find({"user_id": user_id}):
            task["_id"] = str(task["_id"])
            tasks.append(TaskModel(**task).model_dump())

        print(f"Tasks: {tasks}")
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
        user_id = get_jwt_identity()

        task_dict = task.dict(by_alias=True, exclude={"id"})
        task_dict["user_id"] = user_id
        result = self.collection.insert_one(task_dict)
        created_task = self.collection.find_one({"_id": result.inserted_id})

        # Invalidate cache for this user's tasks

        if user_id:
            cache_key = f"tasks:{user_id}"
            self.redis.delete(cache_key)

        return TaskModel(**created_task)

    def update_task(self, task_id, task_update: TaskUpdateModel):
        if not self.collection.find_one({"_id": ObjectId(task_id)}):
            return None

        user_id = get_jwt_identity()
        # Remove campos None
        update_data = {
            k: v
            for k, v in task_update.dict(exclude_unset=True).items()
            if v is not None
        }
        self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
        cache_key = f"tasks:{user_id}"
        self.redis.delete(cache_key)
        return self.get_task(task_id)

    def delete_task(self, task_id):
        # Get the task to find the user_id before deleting
        task = self.collection.find_one({"_id": ObjectId(task_id)})

        result = self.collection.delete_one({"_id": ObjectId(task_id)})

        if result.deleted_count > 0 and task:
            # Invalidate cache for this user's tasks
            user_id = task.get("user_id")
            if user_id:
                cache_key = f"tasks:{user_id}"
                self.redis.delete(cache_key)

        return result.deleted_count > 0
