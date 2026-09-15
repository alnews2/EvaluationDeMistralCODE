"""Task model representing a single task in the application."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Task:
    """
    Represents a task with all necessary attributes.

    Attributes:
        id: Unique identifier for the task (auto-generated if not provided).
        title: Title of the task (required).
        description: Optional description of the task.
        created_at: Timestamp when the task was created.
        due_date: Optional deadline for the task.
        completed: Whether the task is completed.
        priority: Priority level (1-5, where 5 is highest).
        tags: List of tags/categories for the task.
    """

    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    due_date: datetime | None = None
    completed: bool = False
    priority: int = 3
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title:
            raise ValueError("Task title cannot be empty")
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 and 5")

    @property
    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self.due_date is None or self.completed:
            return False
        return self.due_date < datetime.now()

    @property
    def priority_label(self) -> str:
        """Get human-readable priority label."""
        priorities = {
            1: "Très faible",
            2: "Faible",
            3: "Moyenne",
            4: "Élevée",
            5: "Critique"
        }
        return priorities.get(self.priority, "Inconnue")

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "priority": self.priority,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            id=UUID(data["id"]) if data.get("id") else uuid4(),
            title=data.get("title", ""),
            description=data.get("description", ""),
            created_at=datetime.fromisoformat(data["created_at"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            completed=data.get("completed", False),
            priority=data.get("priority", 3),
            tags=data.get("tags", [])
        )
