import json
import pytest
from bson import ObjectId
from datetime import datetime, timedelta, UTC
from app.api.tasks.models import TaskModel
from app.infrastructure.redis.rediscache import RedisCache


class TestTaskEndpoints:
    """Test class for task endpoints."""

    def test_create_task(self, client, auth_headers, mongodb):
        """Test creating a new task."""
        # Prepare task data
        task_data = {
            "titulo": "New Test Task",
            "descricao": "This is a new test task",
            "status": "pending",
            "data_vencimento": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        }

        # Send request to create task
        response = client.post(
            "/api/tasks",
            headers=auth_headers,
            data=json.dumps(task_data),
            content_type="application/json",
        )

        # Assert response
        assert response.status_code == 201
        response_data = json.loads(response.data)

        # Verify task was created in database
        created_task = mongodb.get_collection("tasks").find_one(
            {"titulo": "New Test Task"}
        )
        assert created_task is not None
        assert created_task["titulo"] == task_data["titulo"]
        assert created_task["descricao"] == task_data["descricao"]
        assert created_task["status"] == task_data["status"]

    def test_get_specific_task(self, client, auth_headers, test_task):
        """Test retrieving a specific task."""
        # Send request to get the task
        response = client.get(f"/api/tasks/{test_task.id}", headers=auth_headers)

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify task data
        assert response_data["titulo"] == test_task.titulo
        assert response_data["descricao"] == test_task.descricao
        assert response_data["status"] == test_task.status

    def test_get_all_tasks(self, client, auth_headers, mongodb, test_user):
        """Test retrieving all tasks for a user."""
        # Create multiple tasks for the user
        tasks_data = [
            {
                "titulo": f"Task {i}",
                "descricao": f"Description for task {i}",
                "status": "pending",
                "data_vencimento": datetime.now(UTC) + timedelta(days=i),
                "user_id": str(test_user.id),
            }
            for i in range(1, 4)
        ]

        for task_data in tasks_data:
            mongodb.get_collection("tasks").insert_one(task_data)

        # Send request to get all tasks
        response = client.get("/api/tasks", headers=auth_headers)

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify all tasks are returned (3 new tasks + 1 from test_task fixture)
        assert len(response_data) == 4

        # Verify task data
        task_titles = [task["titulo"] for task in response_data]
        for i in range(1, 4):
            assert f"Task {i}" in task_titles

    def test_redis_caching_get_all_tasks(
        self, client, auth_headers, mongodb, test_user, redis_cache
    ):
        """Test that tasks are cached in Redis when retrieving all tasks."""
        # Create tasks for the user
        tasks_data = [
            {
                "titulo": f"Cache Test Task {i}",
                "descricao": f"Description for cache test task {i}",
                "status": "pending",
                "data_vencimento": datetime.now(UTC) + timedelta(days=i),
                "user_id": str(test_user.id),
            }
            for i in range(1, 3)
        ]

        for task_data in tasks_data:
            mongodb.get_collection("tasks").insert_one(task_data)

        # First request to get all tasks (should cache the results)
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify response
        assert response.status_code == 200

        # Check if tasks are cached in Redis
        cache_key = f"tasks:{str(test_user.id)}"
        cached_tasks = redis_cache.get(cache_key)

        # Verify cache exists
        assert cached_tasks is not None

        # Verify cached data
        task_titles = [task.get("titulo", None) for task in cached_tasks]
        for i in range(1, 3):
            assert f"Cache Test Task {i}" in task_titles

    def test_redis_caching_get_specific_task(
        self, client, auth_headers, test_task, test_user, redis_cache
    ):
        """Test that tasks are cached in Redis when retrieving a specific task."""
        # First request to get all tasks (should cache the results)
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify response
        assert response.status_code == 200

        # Now get a specific task (should use the cache)
        response = client.get(f"/api/tasks/{test_task.id}", headers=auth_headers)

        # Verify response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify task data
        assert response_data["titulo"] == test_task.titulo

        # Check if tasks are cached in Redis
        cache_key = f"tasks:{str(test_user.id)}"
        cached_tasks = redis_cache.get(cache_key)

        # Verify cache exists
        assert cached_tasks is not None

        # Verify the specific task is in the cache
        task_ids = [task.get("id", None) for task in cached_tasks]
        assert str(test_task.id) in task_ids

    def test_cache_invalidation_on_task_creation(
        self, client, auth_headers, test_user, redis_cache
    ):
        """Test that cache is invalidated when a new task is created."""
        # First, get all tasks to populate the cache
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify cache exists
        cache_key = f"tasks:{str(test_user.id)}"
        initial_cached_tasks = redis_cache.get(cache_key)
        assert initial_cached_tasks is not None

        # Count initial tasks
        initial_task_count = len(initial_cached_tasks)

        # Create a new task
        task_data = {
            "titulo": "Cache Invalidation Test Task",
            "descricao": "This task should invalidate the cache",
            "status": "pending",
            "data_vencimento": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        }

        response = client.post(
            "/api/tasks",
            headers=auth_headers,
            data=json.dumps(task_data),
            content_type="application/json",
        )

        # Verify task was created
        assert response.status_code == 201

        # Get all tasks again
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify new task count
        assert len(response_data) == initial_task_count + 1

        # Check updated cache
        updated_cached_tasks = redis_cache.get(cache_key)
        assert updated_cached_tasks is not None
        assert len(updated_cached_tasks) == initial_task_count + 1

        # Verify the new task is in the updated cache
        task_titles = [task.get("titulo", None) for task in updated_cached_tasks]
        assert "Cache Invalidation Test Task" in task_titles

    def test_cache_invalidation_on_task_update(
        self, client, auth_headers, test_task, test_user, redis_cache
    ):
        """Test that cache is invalidated when a task is updated."""
        # First, get all tasks to populate the cache
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify cache exists
        cache_key = f"tasks:{str(test_user.id)}"
        initial_cached_tasks = redis_cache.get(cache_key)
        assert initial_cached_tasks is not None

        # Update a task
        update_data = {"titulo": "Updated Task Title", "status": "completed"}
        response = client.put(
            f"/api/tasks/{test_task.id}",
            headers=auth_headers,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Verify task was updated
        assert response.status_code == 200

        # Get all tasks again
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Find the updated task in the response
        updated_task = None
        for task in response_data:
            if task.get("id") == str(test_task.id):
                updated_task = task
                break

        assert updated_task is not None
        assert updated_task["titulo"] == "Updated Task Title"
        assert updated_task["status"] == "completed"

        # Check updated cache
        updated_cached_tasks = redis_cache.get(cache_key)
        assert updated_cached_tasks is not None

        # Verify the updated task is in the cache with new values
        updated_task_in_cache = None
        for task in updated_cached_tasks:
            if task.get("id") == str(test_task.id):
                updated_task_in_cache = task
                break

        assert updated_task_in_cache is not None
        assert updated_task_in_cache["titulo"] == "Updated Task Title"
        assert updated_task_in_cache["status"] == "completed"

    def test_cache_invalidation_on_task_deletion(
        self, client, auth_headers, test_task, test_user, redis_cache
    ):
        """Test that cache is invalidated when a task is deleted."""
        # First, get all tasks to populate the cache
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify cache exists
        cache_key = f"tasks:{str(test_user.id)}"
        initial_cached_tasks = redis_cache.get(cache_key)
        assert initial_cached_tasks is not None

        # Count initial tasks
        initial_task_count = len(initial_cached_tasks)

        # Delete a task
        response = client.delete(f"/api/tasks/{test_task.id}", headers=auth_headers)

        # Verify task was deleted
        assert response.status_code == 200

        # Get all tasks again
        response = client.get("/api/tasks", headers=auth_headers)

        # Verify response
        assert response.status_code == 200
        response_data = json.loads(response.data)

        # Verify task count decreased
        assert len(response_data) == initial_task_count - 1

        # Check updated cache
        updated_cached_tasks = redis_cache.get(cache_key)
        assert updated_cached_tasks is not None
        assert len(updated_cached_tasks) == initial_task_count - 1

        # Verify the deleted task is not in the cache
        task_ids = [task.get("id", None) for task in updated_cached_tasks]
        assert str(test_task.id) not in task_ids
