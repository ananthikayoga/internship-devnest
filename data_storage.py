"""
Data storage manager using JSON
Handles saving and loading tasks from persistent storage
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from task import Task


class DataStorage:
    """Manages task data persistence using JSON"""

    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.storage_path = Path(storage_file)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage file if it doesn't exist"""
        if not self.storage_path.exists():
            self._save_to_file([])

    def _save_to_file(self, tasks_data: List[Dict[str, Any]]) -> None:
        """Save tasks to JSON file"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving tasks: {e}")
            raise

    def _load_from_file(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file"""
        try:
            if not self.storage_path.exists():
                return []
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if data else []
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save all tasks to storage"""
        tasks_data = [task.to_dict() for task in tasks]
        self._save_to_file(tasks_data)

    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage"""
        tasks_data = self._load_from_file()
        return [Task.from_dict(data) for data in tasks_data]

    def add_task(self, task: Task) -> None:
        """Add a single task"""
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        tasks = self.load_tasks()
        original_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        
        if len(tasks) < original_count:
            self.save_tasks(tasks)
            return True
        return False

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """Update an existing task"""
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return True
        return False

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a single task by ID"""
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def clear_all_tasks(self) -> None:
        """Clear all tasks from storage"""
        self._save_to_file([])

    def export_tasks(self, export_file: str) -> None:
        """Export tasks to another JSON file"""
        tasks = self.load_tasks()
        tasks_data = [task.to_dict() for task in tasks]
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            print(f"Tasks exported to {export_file}")
        except IOError as e:
            print(f"Error exporting tasks: {e}")

    def import_tasks(self, import_file: str) -> None:
        """Import tasks from another JSON file"""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            tasks = self.load_tasks()
            for data in tasks_data:
                task = Task.from_dict(data)
                if not any(t.id == task.id for t in tasks):
                    tasks.append(task)
            self.save_tasks(tasks)
            print(f"Tasks imported from {import_file}")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error importing tasks: {e}")
