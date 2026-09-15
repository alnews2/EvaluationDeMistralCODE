#!/usr/bin/env python3
"""
TaskMaster - Main application entry point.

This is the main entry point for the TaskMaster Qt application.
It initializes the QApplication, sets up the dependency injection,
and starts the main window.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.controllers.task_controller import TaskController
from app.services.task_service import TaskService
from ui.windows.main_window import MainWindow


def main():
    """
    Main application entry point.
    
    Initializes the Qt application, sets up the service layer,
    and displays the main window.
    """
    # Create QApplication instance
    app = QApplication(sys.argv)
    app.setApplicationName("TaskMaster")
    app.setOrganizationName("MistralAI")
    app.setOrganizationDomain("mistral.ai")
    
    # Set up data directory
    data_dir = Path.home() / ".taskmaster"
    data_dir.mkdir(exist_ok=True)
    
    # Initialize service layer
    storage_path = str(data_dir / "tasks.json")
    task_service = TaskService(storage_path=storage_path)
    
    # Initialize controller layer
    task_controller = TaskController(task_service)
    
    # Create and show main window
    window = MainWindow(task_controller)
    window.show()
    
    # Execute application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
