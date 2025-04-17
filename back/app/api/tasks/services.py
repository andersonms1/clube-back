from bson import ObjectId
from app.api.tasks.models import TaskModel, TaskUpdateModel
from app.infrastructure.database.mongodb import MongoDB

class TaskService:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.get_collection('tasks')

    def get_all_tasks(self):
        tasks = []
        for task in self.collection.find():
            tasks.append(TaskModel(**task))
        return tasks

    def get_task(self, task_id):
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            return TaskModel(**task)
        return None

    def create_task(self, task: TaskModel):
        task_dict = task.dict(by_alias=True, exclude={"id"})
        result = self.collection.insert_one(task_dict)
        created_task = self.collection.find_one({"_id": result.inserted_id})
        return TaskModel(**created_task)

    def update_task(self, task_id, task_update: TaskUpdateModel):
        # Remove campos None
        update_data = {k: v for k, v in task_update.dict(exclude_unset=True).items() if v is not None}
        
        if update_data:
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return self.get_task(task_id)
        
        return None

    def delete_task(self, task_id):
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0