"""Controller for managing task-related operations."""

from uuid import UUID

from PySide6.QtCore import QObject, Signal, Slot

from ..models.task import Task
from ..services.task_service import TaskService


class TaskController(QObject):
    """
    Controller class that mediates between the UI and the TaskService.

    Uses Qt's Signal/Slot mechanism to enable loose coupling between
    the UI and business logic layers.
    """

    # Signals for UI updates
    tasks_updated = Signal(list)  # Emitted when tasks list changes
    task_added = Signal(Task)      # Emitted when a task is added
    task_updated = Signal(Task)   # Emitted when a task is updated
    task_deleted = Signal(UUID)    # Emitted when a task is deleted
    error_occurred = Signal(str)   # Emitted when an error occurs

    def __init__(self, task_service: TaskService | None = None):
        """
        Initialize the task controller.

        Args:
            task_service: Optional TaskService instance. If None, creates a new one.
        """
        super().__init__()
        self._task_service = task_service or TaskService()

    @property
    def task_service(self) -> TaskService:
        """Get the task service instance."""
        return self._task_service

    def load_tasks(self) -> list[Task]:
        """
        Load all tasks from the service.

        Returns:
            List of all tasks.
        """
        try:
            tasks = self._task_service.get_all()
            self.tasks_updated.emit(tasks)
            return tasks
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    @Slot(str, str, int, str)
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: int = 3,
        tags_str: str = ""
    ) -> Task | None:
        """
        Add a new task.

        Args:
            title: Task title.
            description: Task description.
            priority: Task priority (1-5).
            tags_str: Comma-separated tags.

        Returns:
            The created task, or None if creation failed.
        """
        try:
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            task = Task(
                title=title,
                description=description,
                priority=priority,
                tags=tags
            )
            created_task = self._task_service.add(task)
            self.task_added.emit(created_task)
            self.tasks_updated.emit(self._task_service.get_all())
            return created_task
        except Exception as e:
            self.error_occurred.emit(str(e))
            return None

    @Slot(UUID)
    def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete.

        Returns:
            True if deletion succeeded, False otherwise.
        """
        try:
            success = self._task_service.delete(task_id)
            if success:
                self.task_deleted.emit(task_id)
                self.tasks_updated.emit(self._task_service.get_all())
            return success
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    @Slot(UUID, str, str, int, str, bool)
    def update_task(
        self,
        task_id: UUID,
        title: str,
        description: str,
        priority: int,
        tags_str: str,
        completed: bool
    ) -> Task | None:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update.
            title: New title.
            description: New description.
            priority: New priority.
            tags_str: Comma-separated tags.
            completed: New completion status.

        Returns:
            The updated task, or None if update failed.
        """
        try:
            existing_task = self._task_service.get_by_id(task_id)
            if existing_task is None:
                self.error_occurred.emit(f"Task with ID {task_id} not found")
                return None

            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            updated_task = Task(
                id=task_id,
                title=title,
                description=description,
                created_at=existing_task.created_at,
                due_date=existing_task.due_date,
                completed=completed,
                priority=priority,
                tags=tags
            )

            result = self._task_service.update(updated_task)
            if result:
                self.task_updated.emit(result)
                self.tasks_updated.emit(self._task_service.get_all())
            return result
        except Exception as e:
            self.error_occurred.emit(str(e))
            return None

    @Slot(UUID)
    def toggle_task_complete(self, task_id: UUID) -> Task | None:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle.

        Returns:
            The updated task, or None if not found.
        """
        try:
            result = self._task_service.toggle_complete(task_id)
            if result:
                self.task_updated.emit(result)
                self.tasks_updated.emit(self._task_service.get_all())
            return result
        except Exception as e:
            self.error_occurred.emit(str(e))
            return None

    @Slot(str)
    def search_tasks(self, query: str) -> list[Task]:
        """
        Search tasks by query.

        Args:
            query: Search term.

        Returns:
            List of matching tasks.
        """
        try:
            return self._task_service.search(query)
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    @Slot(int)
    def filter_by_priority(self, priority: int) -> list[Task]:
        """
        Filter tasks by priority.

        Args:
            priority: Priority level (1-5).

        Returns:
            List of tasks with the specified priority.
        """
        try:
            return self._task_service.get_by_priority(priority)
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    @Slot()
    def get_completed_tasks(self) -> list[Task]:
        """Get all completed tasks."""
        try:
            return self._task_service.get_completed()
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    @Slot()
    def get_pending_tasks(self) -> list[Task]:
        """Get all pending tasks."""
        try:
            return self._task_service.get_pending()
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    @Slot()
    def get_overdue_tasks(self) -> list[Task]:
        """Get all overdue tasks."""
        try:
            return self._task_service.get_overdue()
        except Exception as e:
            self.error_occurred.emit(str(e))
            return []

    def get_task_count(self) -> int:
        """Get the total number of tasks."""
        return self._task_service.count()
