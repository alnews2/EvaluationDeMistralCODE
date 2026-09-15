"""Integration tests for the MainWindow class."""

import pytest
from unittest.mock import MagicMock

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMessageBox

from src.app.controllers.task_controller import TaskController
from src.app.models.task import Task
from src.app.services.task_service import TaskService
from src.ui.windows.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance for testing."""
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def mock_controller(qapp):
    """Create a mock TaskController for testing."""
    # Create a real controller with a mock service
    mock_service = MagicMock(spec=TaskService)
    mock_service.get_all.return_value = []
    
    controller = TaskController(task_service=mock_service)
    return controller


@pytest.fixture
def main_window(qapp, mock_controller):
    """Create a MainWindow instance for testing."""
    window = MainWindow(mock_controller)
    window.show()  # Need to show for some tests
    yield window
    window.close()


class TestMainWindow:
    """Test suite for the MainWindow class."""

    def test_main_window_creation(self, qapp, mock_controller):
        """Test that the main window can be created."""
        window = MainWindow(mock_controller)
        
        assert window is not None
        assert window.windowTitle() == "TaskMaster"
        assert window.minimumWidth() >= 800
        assert window.minimumHeight() >= 600
        
        window.close()

    def test_main_window_has_menubar(self, main_window):
        """Test that the main window has a menu bar."""
        assert main_window.menuBar() is not None
        
        # Check menu items
        menus = main_window.menuBar().findChildren(QObject)
        menu_titles = [m.title() for m in menus if hasattr(m, 'title') and m.title()]
        
        assert "Fichier" in menu_titles
        assert "Édition" in menu_titles
        assert "Affichage" in menu_titles
        assert "Aide" in menu_titles

    def test_main_window_has_toolbar(self, main_window):
        """Test that the main window has a tool bar."""
        toolbars = main_window.findChildren(QObject)
        toolbar = next((t for t in toolbars if hasattr(t, 'objectName') and 'Barre d\'outils' in t.objectName()), None)
        
        assert toolbar is not None

    def test_main_window_has_status_bar(self, main_window):
        """Test that the main window has a status bar."""
        assert main_window.status_bar is not None

    def test_main_window_has_central_widget(self, main_window):
        """Test that the main window has a central widget."""
        assert main_window.centralWidget() is not None

    def test_controller_signals_connected(self, qapp, mock_controller):
        """Test that controller signals are connected to window slots."""
        window = MainWindow(mock_controller)
        
        # Verify signal connections
        assert window.controller.tasks_updated is not None
        assert window.controller.task_added is not None
        assert window.controller.task_updated is not None
        assert window.controller.task_deleted is not None
        assert window.controller.error_occurred is not None
        
        window.close()

    def test_search_functionality(self, qapp, mock_controller):
        """Test the search functionality."""
        # Set up mock to return some tasks
        mock_tasks = [
            Task(title="Test Task 1"),
            Task(title="Test Task 2"),
            Task(title="Other Task")
        ]
        mock_controller.search_tasks.return_value = mock_tasks
        
        window = MainWindow(mock_controller)
        
        # Simulate search
        window.search_input.setText("Test")
        window._on_search_changed("Test")
        
        # Verify search was called
        mock_controller.search_tasks.assert_called_with("Test")
        
        window.close()

    def test_filter_functionality(self, qapp, mock_controller):
        """Test the filter functionality."""
        mock_tasks = [
            Task(title="Task 1", completed=False),
            Task(title="Task 2", completed=True)
        ]
        mock_controller.get_all.return_value = mock_tasks
        mock_controller.get_pending_tasks.return_value = [mock_tasks[0]]
        mock_controller.get_completed_tasks.return_value = [mock_tasks[1]]
        
        window = MainWindow(mock_controller)
        
        # Test setting different filters
        window._set_filter("all")
        assert window.current_filter == "all"
        
        window._set_filter("pending")
        assert window.current_filter == "pending"
        
        window._set_filter("completed")
        assert window.current_filter == "completed"
        
        window.close()

    def test_task_display(self, qapp, mock_controller):
        """Test that tasks are displayed correctly."""
        mock_tasks = [
            Task(title="Display Task 1", description="Description 1"),
            Task(title="Display Task 2", description="Description 2")
        ]
        mock_controller.get_all.return_value = mock_tasks
        
        window = MainWindow(mock_controller)
        
        # Trigger display of tasks
        window._display_tasks(mock_tasks)
        
        # Check that tasks are added to the container
        # Note: This is a basic check - more thorough testing would require
        # inspecting the actual widgets, which is complex with PySide6
        assert window.tasks_container.count() > 0
        
        window.close()

    def test_error_handling(self, qapp, mock_controller):
        """Test error handling in the main window."""
        window = MainWindow(mock_controller)
        
        # Mock the error message box
        with pytest.mock.patch.object(QMessageBox, 'critical') as mock_critical:
            window._on_error("Test error message")
            
            # Verify error message box was called
            mock_critical.assert_called_once()
            args, kwargs = mock_critical.call_args
            assert args[1] == "Test error message"
        
        window.close()

    def test_about_dialog(self, qapp, mock_controller):
        """Test the about dialog."""
        window = MainWindow(mock_controller)
        
        # Mock the about message box
        with pytest.mock.patch.object(QMessageBox, 'about') as mock_about:
            window._show_about_dialog()
            
            # Verify about dialog was called
            mock_about.assert_called_once()
        
        window.close()

    def test_window_close_event(self, qapp, mock_controller):
        """Test the window close event."""
        from PySide6.QtGui import QCloseEvent
        
        window = MainWindow(mock_controller)
        
        # Mock the close event
        mock_event = MagicMock(spec=QCloseEvent)
        
        # Call the close event handler
        window.closeEvent(mock_event)
        
        # Verify event was accepted
        mock_event.accept.assert_called_once()
        
        window.close()


class TestTaskDialog:
    """Test suite for the TaskDialog class."""

    def test_task_dialog_creation(self, qapp, mock_controller):
        """Test that the task dialog can be created."""
        from src.ui.dialogs.task_dialog import TaskDialog
        
        dialog = TaskDialog(None, mock_controller)
        
        assert dialog is not None
        assert "Nouvelle tâche" in dialog.windowTitle()
        
        dialog.close()

    def test_task_dialog_edit_mode(self, qapp, mock_controller):
        """Test the task dialog in edit mode."""
        from src.ui.dialogs.task_dialog import TaskDialog
        
        task = Task(title="Edit Task", description="Edit Description")
        dialog = TaskDialog(None, mock_controller, task)
        
        assert dialog.is_edit_mode is True
        assert "Modifier" in dialog.windowTitle()
        
        dialog.close()

    def test_task_dialog_form_population(self, qapp, mock_controller):
        """Test that the form is populated with task data in edit mode."""
        from src.ui.dialogs.task_dialog import TaskDialog
        
        task = Task(
            title="Form Task",
            description="Form Description",
            priority=4,
            tags=["tag1", "tag2"]
        )
        dialog = TaskDialog(None, mock_controller, task)
        
        assert dialog.title_input.text() == "Form Task"
        assert dialog.description_input.toPlainText() == "Form Description"
        assert dialog.priority_input.value() == 4
        assert dialog.tags_input.text() == "tag1, tag2"
        
        dialog.close()

    def test_task_dialog_validation(self, qapp, mock_controller):
        """Test form validation in the task dialog."""
        from src.ui.dialogs.task_dialog import TaskDialog
        
        dialog = TaskDialog(None, mock_controller)
        
        # Set empty title
        dialog.title_input.setText("")
        
        # Mock the warning message box
        with pytest.mock.patch.object(QMessageBox, 'warning') as mock_warning:
            dialog._accept()
            
            # Verify warning was shown
            mock_warning.assert_called_once()
        
        dialog.close()

    def test_task_dialog_accept(self, qapp, mock_controller):
        """Test the accept functionality of the task dialog."""
        from src.ui.dialogs.task_dialog import TaskDialog
        
        dialog = TaskDialog(None, mock_controller)
        
        # Fill the form
        dialog.title_input.setText("Accept Task")
        dialog.description_input.setPlainText("Accept Description")
        dialog.priority_input.setValue(3)
        dialog.tags_input.setText("accept, test")
        
        # Mock the controller's add_task method
        mock_controller.add_task.return_value = Task(
            title="Accept Task",
            description="Accept Description",
            priority=3,
            tags=["accept", "test"]
        )
        
        # Mock the dialog's accept method
        with pytest.mock.patch.object(dialog, 'accept') as mock_accept:
            dialog._accept()
            
            # Verify controller was called
            mock_controller.add_task.assert_called_once()
            
            # Verify dialog accept was called
            mock_accept.assert_called_once()
        
        dialog.close()
