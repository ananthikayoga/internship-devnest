"""
Task Manager for TaskFlow Pro
Core business logic for managing tasks
"""

from typing import List, Optional
from datetime import datetime, timedelta
from task import Task, Priority
from data_storage import DataStorage
from analytics import ProductivityAnalytics


class TaskManager:
    """Main task management engine"""

    def __init__(self, storage_file: str = "tasks.json"):
        self.storage = DataStorage(storage_file)
        self.tasks = self.storage.load_tasks()

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        due_date: Optional[str] = None,
        category: str = "General"
    ) -> Task:
        """Add new task"""
        task = Task(
            title=title,
            description=description,
            priority=Priority[priority.upper()],
            due_date=due_date,
            category=category
        )
        self.tasks.append(task)
        self.storage.add_task(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete task by ID"""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return self.storage.delete_task(task_id)

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> bool:
        """Update task attributes"""
        for task in self.tasks:
            if task.id == task_id:
                task.update(title, description, priority, due_date, category)
                self.storage.update_task(task_id, task)
                return True
        return False

    def mark_completed(self, task_id: str) -> bool:
        """Mark task as completed"""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_completed()
                self.storage.update_task(task_id, task)
                return True
        return False

    def mark_incomplete(self, task_id: str) -> bool:
        """Mark task as incomplete"""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_incomplete()
                self.storage.update_task(task_id, task)
                return True
        return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks.copy()

    def get_active_tasks(self) -> List[Task]:
        """Get all incomplete tasks"""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [t for t in self.tasks if t.completed]

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks by category"""
        return [t for t in self.tasks if t.category.lower() == category.lower()]

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority"""
        try:
            priority_level = Priority[priority.upper()]
            return [t for t in self.tasks if t.priority == priority_level]
        except KeyError:
            return []

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query = query.lower()
        return [
            t for t in self.tasks
            if query in t.title.lower() or query in t.description.lower()
        ]

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by multiple criteria"""
        result = self.tasks.copy()

        if completed is not None:
            result = [t for t in result if t.completed == completed]

        if priority:
            try:
                priority_level = Priority[priority.upper()]
                result = [t for t in result if t.priority == priority_level]
            except KeyError:
                pass

        if category:
            result = [t for t in result if t.category.lower() == category.lower()]

        if due_date:
            result = [t for t in result if t.due_date == due_date]

        return result

    def set_task_reminder(self, task_id: str, reminder_minutes: int = 24 * 60) -> bool:
        """Set reminder for task (placeholder for future implementation)"""
        task = self.get_task(task_id)
        if task:
            task.reminders_set = True
            self.storage.update_task(task_id, task)
            return True
        return False

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks"""
        today = datetime.now()
        overdue = []
        for task in self.tasks:
            if task.due_date and not task.completed:
                due = datetime.strptime(task.due_date, "%Y-%m-%d")
                if due < today:
                    overdue.append(task)
        return overdue

    def get_due_today_tasks(self) -> List[Task]:
        """Get tasks due today"""
        today = datetime.now().strftime("%Y-%m-%d")
        return [t for t in self.tasks if t.due_date == today and not t.completed]

    def get_due_soon_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within specified days"""
        today = datetime.now()
        end_date = today + timedelta(days=days)

        return [
            t for t in self.tasks
            if t.due_date and not t.completed and
            today <= datetime.strptime(t.due_date, "%Y-%m-%d") <= end_date
        ]

    def get_analytics(self) -> ProductivityAnalytics:
        """Get analytics object for current tasks"""
        return ProductivityAnalytics(self.tasks)

    def reload_tasks(self) -> None:
        """Reload tasks from storage"""
        self.tasks = self.storage.load_tasks()

    def get_statistics_summary(self) -> dict:
        """Get quick statistics"""
        analytics = self.get_analytics()
        return {
            "total": analytics.get_total_tasks(),
            "completed": analytics.get_completed_count(),
            "pending": analytics.get_pending_count(),
            "overdue": analytics.get_overdue_count(),
            "productivity": analytics.get_productivity_percentage()
        }
