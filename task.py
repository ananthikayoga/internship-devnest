"""
Task model for TaskFlow Pro
Handles individual task data and operations
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, Optional


class Priority(Enum):
    """Priority levels for tasks"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self):
        return self.name


class TaskStatus(Enum):
    """Status of tasks"""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class Task:
    """Represents a single task"""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[str] = None,
        category: str = "General",
        task_id: Optional[str] = None,
        completed: bool = False,
        created_date: Optional[str] = None,
        completed_date: Optional[str] = None
    ):
        self.title = title
        self.description = description
        self.priority = priority if isinstance(priority, Priority) else Priority[priority.upper()]
        self.due_date = due_date
        self.category = category
        self.completed = completed
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_date = completed_date
        self.reminders_set = False
        self.id = task_id or self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique task ID"""
        import hashlib
        import uuid
        data = f"{self.title}{datetime.now().timestamp()}".encode()
        return hashlib.md5(data).hexdigest()[:8]

    def get_status(self) -> TaskStatus:
        """Determine current task status"""
        if self.completed:
            return TaskStatus.COMPLETED
        
        if self.due_date:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            if datetime.now() > due and not self.completed:
                return TaskStatus.OVERDUE
        
        return TaskStatus.PENDING

    def mark_completed(self) -> None:
        """Mark task as completed"""
        self.completed = True
        self.completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_incomplete(self) -> None:
        """Mark task as incomplete"""
        self.completed = False
        self.completed_date = None

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> None:
        """Update task attributes"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = Priority[priority.upper()]
        if due_date is not None:
            self.due_date = due_date
        if category is not None:
            self.category = category

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON storage"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "due_date": self.due_date,
            "category": self.category,
            "completed": self.completed,
            "created_date": self.created_date,
            "completed_date": self.completed_date,
            "reminders_set": self.reminders_set
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary"""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "MEDIUM"),
            due_date=data.get("due_date"),
            category=data.get("category", "General"),
            task_id=data.get("id"),
            completed=data.get("completed", False),
            created_date=data.get("created_date"),
            completed_date=data.get("completed_date")
        )

    def __str__(self) -> str:
        """String representation of task"""
        status = self.get_status()
        due_display = f" | Due: {self.due_date}" if self.due_date else ""
        completed_mark = "✓" if self.completed else "○"
        return (f"{completed_mark} [{self.id}] {self.title} | {self.priority.name} "
                f"| {self.category}{due_display}")

    def __repr__(self) -> str:
        return f"Task({self.title}, {self.priority.name}, {self.due_date})"
