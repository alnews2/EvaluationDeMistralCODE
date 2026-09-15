"""Unit tests for the Task model."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.app.models.task import Task


class TestTaskModel:
    """Test suite for the Task model."""

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(title="Test Task")
        
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == 3
        assert task.tags == []
        assert task.created_at is not None
        assert isinstance(task.id, uuid4().__class__)

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task_id = uuid4()
        due_date = datetime.now() + timedelta(days=7)
        
        task = Task(
            id=task_id,
            title="Full Task",
            description="Task description",
            created_at=datetime.now(),
            due_date=due_date,
            completed=True,
            priority=5,
            tags=["urgent", "work"]
        )
        
        assert task.id == task_id
        assert task.title == "Full Task"
        assert task.description == "Task description"
        assert task.due_date == due_date
        assert task.completed is True
        assert task.priority == 5
        assert task.tags == ["urgent", "work"]

    def test_task_creation_without_title_raises_error(self):
        """Test that creating a task without a title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_task_creation_with_invalid_priority_raises_error(self):
        """Test that creating a task with invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
            Task(title="Test", priority=0)
        
        with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
            Task(title="Test", priority=6)

    def test_is_overdue_property(self):
        """Test the is_overdue property."""
        # Task with no due date is not overdue
        task1 = Task(title="No due date")
        assert task1.is_overdue is False
        
        # Completed task with past due date is not overdue
        past_date = datetime.now() - timedelta(days=1)
        task2 = Task(
            title="Completed with past due",
            due_date=past_date,
            completed=True
        )
        assert task2.is_overdue is False
        
        # Incomplete task with past due date is overdue
        task3 = Task(
            title="Incomplete with past due",
            due_date=past_date,
            completed=False
        )
        assert task3.is_overdue is True
        
        # Incomplete task with future due date is not overdue
        future_date = datetime.now() + timedelta(days=1)
        task4 = Task(
            title="Incomplete with future due",
            due_date=future_date,
            completed=False
        )
        assert task4.is_overdue is False

    def test_priority_label_property(self):
        """Test the priority_label property."""
        priorities = {
            1: "Très faible",
            2: "Faible",
            3: "Moyenne",
            4: "Élevée",
            5: "Critique"
        }
        
        for priority, label in priorities.items():
            task = Task(title="Test", priority=priority)
            assert task.priority_label == label

    def test_to_dict_method(self):
        """Test the to_dict method."""
        task_id = uuid4()
        due_date = datetime.now() + timedelta(days=1)
        
        task = Task(
            id=task_id,
            title="Test Task",
            description="Test Description",
            created_at=datetime.now(),
            due_date=due_date,
            completed=True,
            priority=4,
            tags=["test", "example"]
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["id"] == str(task_id)
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is True
        assert task_dict["priority"] == 4
        assert task_dict["tags"] == ["test", "example"]
        assert "created_at" in task_dict
        assert "due_date" in task_dict

    def test_from_dict_method(self):
        """Test the from_dict method."""
        task_id = uuid4()
        created_at = datetime.now()
        due_date = created_at + timedelta(days=1)
        
        data = {
            "id": str(task_id),
            "title": "From Dict Task",
            "description": "From Dict Description",
            "created_at": created_at.isoformat(),
            "due_date": due_date.isoformat(),
            "completed": False,
            "priority": 2,
            "tags": ["from", "dict"]
        }
        
        task = Task.from_dict(data)
        
        assert task.id == task_id
        assert task.title == "From Dict Task"
        assert task.description == "From Dict Description"
        assert task.created_at == created_at
        assert task.due_date == due_date
        assert task.completed is False
        assert task.priority == 2
        assert task.tags == ["from", "dict"]

    def test_from_dict_with_missing_fields(self):
        """Test from_dict with missing optional fields."""
        data = {
            "title": "Minimal Task",
            "created_at": datetime.now().isoformat()
        }
        
        task = Task.from_dict(data)
        
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == 3
        assert task.tags == []
        assert task.due_date is None
