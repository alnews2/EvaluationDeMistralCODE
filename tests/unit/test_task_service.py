"""Unit tests for the TaskService class."""

import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from src.app.models.task import Task
from src.app.services.task_service import TaskService


class TestTaskService:
    """Test suite for the TaskService class."""

    @pytest.fixture
    def temp_storage_path(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture
    def task_service(self, temp_storage_path):
        """Create a TaskService instance with temporary storage."""
        return TaskService(storage_path=temp_storage_path)

    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        return [
            Task(title="Task 1", priority=1, tags=["low"]),
            Task(title="Task 2", priority=3, completed=True),
            Task(title="Task 3", priority=5, due_date=datetime.now() - timedelta(days=1)),
            Task(title="Task 4", description="Important task", priority=4)
        ]

    def test_initialization_creates_empty_service(self, task_service):
        """Test that a new TaskService starts with no tasks."""
        assert task_service.count() == 0
        assert task_service.get_all() == []

    def test_add_task(self, task_service):
        """Test adding a task."""
        task = Task(title="Test Task", description="Test Description")
        
        added_task = task_service.add(task)
        
        assert added_task.id is not None
        assert task_service.count() == 1
        assert task_service.get_by_id(added_task.id) is not None

    def test_add_multiple_tasks(self, task_service, sample_tasks):
        """Test adding multiple tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        assert task_service.count() == len(sample_tasks)
        assert len(task_service.get_all()) == len(sample_tasks)

    def test_get_by_id(self, task_service, sample_tasks):
        """Test getting a task by ID."""
        for task in sample_tasks:
            task_service.add(task)
        
        # Get the first task
        first_task = sample_tasks[0]
        retrieved_task = task_service.get_by_id(first_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == first_task.id
        assert retrieved_task.title == first_task.title

    def test_get_by_id_nonexistent(self, task_service):
        """Test getting a task with a non-existent ID."""
        result = task_service.get_by_id(uuid4())
        assert result is None

    def test_update_task(self, task_service):
        """Test updating a task."""
        original_task = Task(title="Original Title")
        task_service.add(original_task)
        
        updated_task = Task(
            id=original_task.id,
            title="Updated Title",
            description="Updated Description",
            priority=5
        )
        
        result = task_service.update(updated_task)
        
        assert result is not None
        assert result.title == "Updated Title"
        assert result.description == "Updated Description"
        assert result.priority == 5
        
        # Verify the update is persisted
        retrieved = task_service.get_by_id(original_task.id)
        assert retrieved.title == "Updated Title"

    def test_update_nonexistent_task(self, task_service):
        """Test updating a non-existent task."""
        task = Task(id=uuid4(), title="Non-existent")
        result = task_service.update(task)
        assert result is None

    def test_delete_task(self, task_service, sample_tasks):
        """Test deleting a task."""
        for task in sample_tasks:
            task_service.add(task)
        
        task_to_delete = sample_tasks[0]
        result = task_service.delete(task_to_delete.id)
        
        assert result is True
        assert task_service.count() == len(sample_tasks) - 1
        assert task_service.get_by_id(task_to_delete.id) is None

    def test_delete_nonexistent_task(self, task_service):
        """Test deleting a non-existent task."""
        result = task_service.delete(uuid4())
        assert result is False

    def test_get_completed_tasks(self, task_service, sample_tasks):
        """Test getting completed tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        completed_tasks = task_service.get_completed()
        
        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == "Task 2"

    def test_get_pending_tasks(self, task_service, sample_tasks):
        """Test getting pending tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        pending_tasks = task_service.get_pending()
        
        assert len(pending_tasks) == 3  # All except Task 2

    def test_get_overdue_tasks(self, task_service, sample_tasks):
        """Test getting overdue tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        overdue_tasks = task_service.get_overdue()
        
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].title == "Task 3"

    def test_get_by_priority(self, task_service, sample_tasks):
        """Test getting tasks by priority."""
        for task in sample_tasks:
            task_service.add(task)
        
        high_priority_tasks = task_service.get_by_priority(5)
        
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].title == "Task 3"

    def test_get_by_tag(self, task_service, sample_tasks):
        """Test getting tasks by tag."""
        for task in sample_tasks:
            task_service.add(task)
        
        low_priority_tasks = task_service.get_by_tag("low")
        
        assert len(low_priority_tasks) == 1
        assert low_priority_tasks[0].title == "Task 1"

    def test_search_tasks(self, task_service, sample_tasks):
        """Test searching tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        # Search by title
        results = task_service.search("Task 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"
        
        # Search by description
        results = task_service.search("Important")
        assert len(results) == 1
        assert results[0].title == "Task 4"
        
        # Search with no results
        results = task_service.search("Non-existent")
        assert len(results) == 0

    def test_toggle_complete(self, task_service):
        """Test toggling task completion status."""
        task = Task(title="Toggle Test", completed=False)
        task_service.add(task)
        
        # First toggle: False -> True
        result = task_service.toggle_complete(task.id)
        assert result is not None
        assert result.completed is True
        
        # Second toggle: True -> False
        result = task_service.toggle_complete(task.id)
        assert result is not None
        assert result.completed is False

    def test_toggle_complete_nonexistent(self, task_service):
        """Test toggling completion for a non-existent task."""
        result = task_service.toggle_complete(uuid4())
        assert result is None

    def test_clear_all(self, task_service, sample_tasks):
        """Test clearing all tasks."""
        for task in sample_tasks:
            task_service.add(task)
        
        assert task_service.count() == len(sample_tasks)
        
        task_service.clear_all()
        
        assert task_service.count() == 0
        assert task_service.get_all() == []

    def test_persistence(self, temp_storage_path):
        """Test that tasks are persisted to file."""
        service1 = TaskService(storage_path=temp_storage_path)
        
        # Add tasks
        task1 = Task(title="Persistent Task 1")
        task2 = Task(title="Persistent Task 2")
        service1.add(task1)
        service1.add(task2)
        
        # Create a new service instance with the same storage path
        service2 = TaskService(storage_path=temp_storage_path)
        
        # Verify tasks are loaded
        assert service2.count() == 2
        all_tasks = service2.get_all()
        assert len(all_tasks) == 2
        
        # Verify task data
        titles = [t.title for t in all_tasks]
        assert "Persistent Task 1" in titles
        assert "Persistent Task 2" in titles

    def test_persistence_file_format(self, task_service, temp_storage_path):
        """Test the format of the persistence file."""
        task = Task(title="Format Test", description="Test description")
        task_service.add(task)
        
        # Read the file directly
        with open(temp_storage_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "tasks" in data
        assert "metadata" in data
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Format Test"
        assert data["tasks"][0]["description"] == "Test description"

    def test_empty_storage_file(self, temp_storage_path):
        """Test loading from an empty or non-existent storage file."""
        # Create a new service with a non-existent file
        service = TaskService(storage_path=temp_storage_path)
        assert service.count() == 0
        
        # Create an empty file
        with open(temp_storage_path, 'w', encoding='utf-8') as f:
            f.write('')
        
        # Create a new service with the empty file
        service = TaskService(storage_path=temp_storage_path)
        assert service.count() == 0

    def test_corrupted_storage_file(self, temp_storage_path):
        """Test loading from a corrupted storage file."""
        # Write corrupted JSON
        with open(temp_storage_path, 'w', encoding='utf-8') as f:
            f.write('{ invalid json }')
        
        # Service should handle this gracefully
        service = TaskService(storage_path=temp_storage_path)
        assert service.count() == 0

    def test_storage_directory_creation(self, temp_storage_path):
        """Test that the storage directory is created if it doesn't exist."""
        # Use a path in a non-existent directory
        nested_path = os.path.join(tempfile.gettempdir(), "nested", "dir", "tasks.json")
        
        service = TaskService(storage_path=nested_path)
        task = Task(title="Test")
        service.add(task)
        
        # Verify the directory was created
        assert os.path.exists(os.path.dirname(nested_path))
        assert os.path.exists(nested_path)
        
        # Clean up
        os.unlink(nested_path)
        os.rmdir(os.path.dirname(nested_path))
        os.rmdir(os.path.dirname(os.path.dirname(nested_path)))
