"""Service for managing tasks."""

import json
from pathlib import Path
from uuid import UUID

from ..models.task import Task


class TaskService:
    """
    Service class for managing tasks.

    Handles CRUD operations, persistence, and business logic for tasks.
    Uses JSON file storage by default, but can be extended to use a database.
    """

    DEFAULT_STORAGE_PATH = "tasks.json"

    def __init__(self, storage_path: str | None = None):
        """
        Initialize the task service.

        Args:
            storage_path: Path to the JSON file for storing tasks.
                         If None, uses DEFAULT_STORAGE_PATH.
        """
        self.storage_path = storage_path or self.DEFAULT_STORAGE_PATH
        self._tasks: dict[UUID, Task] = {}
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from the storage file."""
        try:
            if not Path(self.storage_path).exists():
                self._tasks = {}
                return

            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
                self._tasks = {
                    task.id: task for task in
                    (Task.from_dict(item) for item in data.get("tasks", []))
                }
        except (json.JSONDecodeError, FileNotFoundError, ValueError):
            # If loading fails, start with empty tasks
            self._tasks = {}

    def _save_tasks(self) -> None:
        """Save tasks to the storage file."""
        data = {
            "tasks": [task.to_dict() for task in self._tasks.values()],
            "metadata": {
                "count": len(self._tasks),
                "last_updated": Task.created_at.isoformat() if self._tasks else None
            }
        }

        # Ensure directory exists
        Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        return list(self._tasks.values())

    def get_by_id(self, task_id: UUID) -> Task | None:
        """Get a task by its ID."""
        return self._tasks.get(task_id)

    def add(self, task: Task) -> Task:
        """
        Add a new task.

        Args:
            task: The task to add.

        Returns:
            The added task (with generated ID if not provided).
        """
        self._tasks[task.id] = task
        self._save_tasks()
        return task

    def update(self, task: Task) -> Task | None:
        """
        Update an existing task.

        Args:
            task: The task to update (must have a valid ID).

        Returns:
            The updated task, or None if the task was not found.
        """
        if task.id not in self._tasks:
            return None

        self._tasks[task.id] = task
        self._save_tasks()
        return task

    def delete(self, task_id: UUID) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if it was not found.
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        self._save_tasks()
        return True

    def get_completed(self) -> list[Task]:
        """Get all completed tasks."""
        return [task for task in self._tasks.values() if task.completed]

    def get_pending(self) -> list[Task]:
        """Get all pending (incomplete) tasks."""
        return [task for task in self._tasks.values() if not task.completed]

    def get_overdue(self) -> list[Task]:
        """Get all overdue tasks."""
        return [task for task in self._tasks.values() if task.is_overdue]

    def get_by_priority(self, priority: int) -> list[Task]:
        """Get tasks by priority level."""
        return [task for task in self._tasks.values() if task.priority == priority]

    def get_by_tag(self, tag: str) -> list[Task]:
        """Get tasks by tag."""
        return [task for task in self._tasks.values() if tag in task.tags]

    def toggle_complete(self, task_id: UUID) -> Task | None:
        """
        Toggle the completed status of a task.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task, or None if not found.
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        self._save_tasks()
        return task

    def search(self, query: str) -> list[Task]:
        """
        Search tasks by title or description.

        Args:
            query: The search term (case-insensitive).

        Returns:
            List of tasks matching the query.
        """
        query = query.lower()
        return [
            task for task in self._tasks.values()
            if query in task.title.lower() or query in task.description.lower()
        ]

    def clear_all(self) -> None:
        """Delete all tasks."""
        self._tasks = {}
        self._save_tasks()

    def count(self) -> int:
        """Get the total number of tasks."""
        return len(self._tasks)
