from datetime import datetime
from enum import Enum, auto


class TaskStatus(str, Enum):
    """Enum representing the possible status of a task"""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    
    @classmethod
    def list(cls):
        """Returns a list of all status values"""
        return [status.value for status in cls]


class Task:
    """Task domain model"""
    
    def __init__(
        self,
        title,
        description,
        user_id,
        status=None,
        due_date=None,
        created_at=None,
        updated_at=None,
        _id=None
    ):
        self._id = _id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status = status or TaskStatus.TODO
        self.due_date = due_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self):
        """Get the ID of the task"""
        return str(self._id) if self._id else None
    
    def update_status(self, new_status):
        """Update the status of the task"""
        if new_status not in TaskStatus.list():
            raise ValueError(f"Invalid status: {new_status}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert task model to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary"""
        return cls(
            _id=data.get("_id"),
            title=data.get("title"),
            description=data.get("description"),
            user_id=data.get("user_id"),
            status=data.get("status"),
            due_date=data.get("due_date"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )