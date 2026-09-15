"""Main application window for TaskMaster."""

from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ...app.controllers.task_controller import TaskController


class MainWindow(QMainWindow):
    """
    Main application window with task management interface.

    Features:
    - Task list display
    - Task creation/edition
    - Filtering and search
    - Modern UI with dark theme support
    """

    def __init__(self, controller: TaskController):
        """
        Initialize the main window.

        Args:
            controller: TaskController instance for business logic.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle("TaskMaster")
        self.setMinimumSize(800, 600)

        # Configure the controller's signals
        self._setup_controller_signals()

        # Set up the UI
        self._setup_menubar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()

        # Apply styles
        self._apply_styles()

        # Load initial data
        self.controller.load_tasks()

    def _setup_controller_signals(self):
        """Connect controller signals to UI slots."""
        self.controller.tasks_updated.connect(self._on_tasks_updated)
        self.controller.task_added.connect(self._on_task_added)
        self.controller.task_updated.connect(self._on_task_updated)
        self.controller.task_deleted.connect(self._on_task_deleted)
        self.controller.error_occurred.connect(self._on_error)

    def _setup_menubar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("Fichier")

        new_action = QAction("Nouvelle tâche", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._show_add_task_dialog)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        exit_action = QAction("Quitter", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        menubar.addMenu("Édition")

        # View menu
        menubar.addMenu("Affichage")

        # Help menu
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

    def _setup_toolbar(self):
        """Set up the tool bar."""
        toolbar = QToolBar("Barre d'outils")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add task button
        add_task_action = toolbar.addAction("Ajouter une tâche")
        add_task_action.setIcon(self._create_icon("+"))
        add_task_action.triggered.connect(self._show_add_task_dialog)

        # Search field
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)

        search_label = QLabel("Rechercher :")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Entrez un terme de recherche...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._on_search_changed)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        toolbar.addWidget(search_widget)

        # Spacer
        toolbar.addSeparator()

        # Filter buttons
        filter_all = QPushButton("Toutes")
        filter_all.setCheckable(True)
        filter_all.setChecked(True)
        filter_all.clicked.connect(lambda: self._set_filter("all"))
        toolbar.addWidget(filter_all)

        filter_pending = QPushButton("En cours")
        filter_pending.setCheckable(True)
        filter_pending.clicked.connect(lambda: self._set_filter("pending"))
        toolbar.addWidget(filter_pending)

        filter_completed = QPushButton("Terminées")
        filter_completed.setCheckable(True)
        filter_completed.clicked.connect(lambda: self._set_filter("completed"))
        toolbar.addWidget(filter_completed)

        filter_overdue = QPushButton("En retard")
        filter_overdue.setCheckable(True)
        filter_overdue.clicked.connect(lambda: self._set_filter("overdue"))
        toolbar.addWidget(filter_overdue)

        # Store filter buttons for exclusive selection
        self.filter_buttons = {
            "all": filter_all,
            "pending": filter_pending,
            "completed": filter_completed,
            "overdue": filter_overdue
        }
        self.current_filter = "all"

    def _setup_central_widget(self):
        """Set up the central widget with main content."""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create the main content area
        self.stacked_widget = QStackedWidget()

        # Main tasks view
        self.tasks_tab = self._create_tasks_tab()
        self.stacked_widget.addWidget(self.tasks_tab)

        # Stats view
        self.stats_tab = self._create_stats_tab()
        self.stacked_widget.addWidget(self.stats_tab)

        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(self.stacked_widget, "Tâches")
        tab_widget.addTab(self.stats_tab, "Statistiques")

        main_layout.addWidget(tab_widget)
        self.setCentralWidget(central_widget)

    def _create_tasks_tab(self) -> QWidget:
        """Create the main tasks tab."""
        tasks_widget = QWidget()
        layout = QVBoxLayout(tasks_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        header.addWidget(QLabel("Mes tâches"))
        header.addStretch()

        self.task_count_label = QLabel("0 tâche(s)")
        header.addWidget(self.task_count_label)
        layout.addLayout(header)

        # Tasks list area (will be populated dynamically)
        self.tasks_container = QVBoxLayout()
        self.tasks_container.setSpacing(10)

        # Scrollable area for tasks
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.addLayout(self.tasks_container)
        scroll_layout.addStretch()

        # Add to main layout
        layout.addWidget(scroll_widget)
        layout.addStretch()

        return tasks_widget

    def _create_stats_tab(self) -> QWidget:
        """Create the statistics tab."""
        stats_widget = QWidget()
        layout = QVBoxLayout(stats_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        layout.addWidget(QLabel("Statistiques"))
        layout.addStretch()

        return stats_widget

    def _setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt", 3000)

    def _apply_styles(self):
        """Apply custom styles to the window."""
        self.setStyleSheet("""
            /* Main window */
            QMainWindow {
                background-color: #2b2b2b;
            }

            /* Toolbar */
            QToolBar {
                background-color: #3c3f41;
                border-bottom: 1px solid #1e1e1e;
                padding: 5px;
            }

            QToolBar QPushButton {
                background-color: #4a4d4f;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }

            QToolBar QPushButton:hover {
                background-color: #5a5d5f;
            }

            QToolBar QPushButton:checked {
                background-color: #0078d7;
            }

            /* Menu bar */
            QMenuBar {
                background-color: #3c3f41;
                color: #ffffff;
                border-bottom: 1px solid #1e1e1e;
            }

            QMenuBar::item {
                background-color: transparent;
                color: #ffffff;
            }

            QMenuBar::item:selected {
                background-color: #0078d7;
            }

            QMenu {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #1e1e1e;
            }

            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                padding: 5px 20px;
            }

            QMenu::item:selected {
                background-color: #0078d7;
            }

            /* Status bar */
            QStatusBar {
                background-color: #3c3f41;
                color: #ffffff;
                border-top: 1px solid #1e1e1e;
            }

            /* Labels */
            QLabel {
                color: #ffffff;
            }

            /* Line edits */
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3f41;
                border-radius: 3px;
                padding: 5px;
            }

            QLineEdit:focus {
                border: 1px solid #0078d7;
            }

            /* Buttons */
            QPushButton {
                background-color: #0078d7;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                min-height: 25px;
            }

            QPushButton:hover {
                background-color: #005fa3;
            }

            QPushButton:pressed {
                background-color: #004578;
            }

            QPushButton:disabled {
                background-color: #4a4d4f;
            }

            /* Tab widget */
            QTabWidget::pane {
                background-color: #2b2b2b;
                border: 1px solid #3c3f41;
            }

            QTabBar::tab {
                background-color: #3c3f41;
                color: #ffffff;
                padding: 8px 15px;
                border: none;
            }

            QTabBar::tab:selected {
                background-color: #0078d7;
            }

            /* Scrollbar */
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 10px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background-color: #4a4d4f;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #5a5d5f;
            }

            /* Task item */
            QFrame#TaskItem {
                background-color: #3c3f41;
                border: 1px solid #4a4d4f;
                border-radius: 5px;
                padding: 10px;
            }

            QFrame#TaskItem:hover {
                border: 1px solid #0078d7;
            }

            QFrame#TaskItem.completed {
                background-color: #2d5a2d;
                border: 1px solid #3d7a3d;
            }

            QFrame#TaskItem.overdue {
                background-color: #5a2d2d;
                border: 1px solid #7a3d3d;
            }
        """)

    def _create_icon(self, text: str) -> QIcon:
        """Create a simple icon from text."""
        # This is a placeholder - in a real app, you'd use actual icons
        icon = QIcon()
        return icon

    def _on_tasks_updated(self, tasks: list):
        """Handle tasks updated signal."""
        self._refresh_tasks_list()
        self.task_count_label.setText(f"{len(tasks)} tâche(s)")
        self.status_bar.showMessage(f"{len(tasks)} tâche(s) chargées", 2000)

    def _on_task_added(self, task):
        """Handle task added signal."""
        self.status_bar.showMessage(f"Tâche '{task.title}' ajoutée", 2000)

    def _on_task_updated(self, task):
        """Handle task updated signal."""
        self.status_bar.showMessage(f"Tâche '{task.title}' mise à jour", 2000)

    def _on_task_deleted(self, task_id):
        """Handle task deleted signal."""
        self.status_bar.showMessage("Tâche supprimée", 2000)

    def _on_error(self, error_message: str):
        """Handle error signal."""
        QMessageBox.critical(self, "Erreur", error_message)

    def _on_search_changed(self, text: str):
        """Handle search text changed."""
        if text:
            results = self.controller.search_tasks(text)
            self._display_tasks(results)
        else:
            self._apply_filter()

    def _set_filter(self, filter_type: str):
        """Set the current filter type."""
        # Uncheck all buttons
        for btn in self.filter_buttons.values():
            btn.setChecked(False)

        # Check the selected button
        self.filter_buttons[filter_type].setChecked(True)
        self.current_filter = filter_type
        self._apply_filter()

    def _apply_filter(self):
        """Apply the current filter to the tasks list."""
        if self.current_filter == "all":
            tasks = self.controller.get_all()
        elif self.current_filter == "pending":
            tasks = self.controller.get_pending_tasks()
        elif self.current_filter == "completed":
            tasks = self.controller.get_completed_tasks()
        elif self.current_filter == "overdue":
            tasks = self.controller.get_overdue_tasks()
        else:
            tasks = self.controller.get_all()

        # Apply search filter if there's text
        search_text = self.search_input.text()
        if search_text:
            tasks = self.controller.search_tasks(search_text)

        self._display_tasks(tasks)

    def _refresh_tasks_list(self):
        """Refresh the tasks list based on current filter."""
        self._apply_filter()

    def _display_tasks(self, tasks: list):
        """Display the given list of tasks."""
        # Clear existing tasks
        for i in reversed(range(self.tasks_container.count())):
            item = self.tasks_container.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                widget.setParent(None)

        # Add each task
        for task in tasks:
            task_item = self._create_task_item(task)
            self.tasks_container.addWidget(task_item)

        # Add stretch to push tasks to the top
        self.tasks_container.addStretch()

    def _create_task_item(self, task) -> QFrame:
        """Create a widget for displaying a single task."""
        frame = QFrame()
        frame.setObjectName("TaskItem")
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setFrameShadow(QFrame.Shadow.Raised)

        # Add completed or overdue classes
        if task.completed:
            frame.setProperty("class", "completed")
        elif task.is_overdue:
            frame.setProperty("class", "overdue")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Checkbox for completion status
        complete_button = QPushButton()
        complete_button.setCheckable(True)
        complete_button.setChecked(task.completed)
        complete_button.setFixedSize(20, 20)
        complete_button.setStyleSheet("""
            QPushButton {
                background-color: #4a4d4f;
                border: 1px solid #6a6d6f;
                border-radius: 3px;
            }
            QPushButton:checked {
                background-color: #0078d7;
                border: 1px solid #005fa3;
            }
        """)
        complete_button.clicked.connect(
            lambda checked, tid=task.id: self.controller.toggle_task_complete(tid)
        )
        layout.addWidget(complete_button)

        # Task info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        title_label = QLabel(task.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(title_label)

        if task.description:
            desc_label = QLabel(task.description)
            desc_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)

        # Tags and priority
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(10)

        priority_label = QLabel(f"Priorité: {task.priority_label}")
        priority_label.setStyleSheet("color: #888888; font-size: 11px;")
        meta_layout.addWidget(priority_label)

        if task.tags:
            tags_label = QLabel(f"Tags: {', '.join(task.tags)}")
            tags_label.setStyleSheet("color: #888888; font-size: 11px;")
            meta_layout.addWidget(tags_label)

        if task.due_date:
            due_label = QLabel(f"Échéance: {task.due_date.strftime('%d/%m/%Y')}")
            due_label.setStyleSheet("color: #888888; font-size: 11px;")
            meta_layout.addWidget(due_label)

        info_layout.addLayout(meta_layout)
        layout.addLayout(info_layout)
        layout.addStretch()

        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(5)

        edit_button = QPushButton("Modifier")
        edit_button.setFixedSize(80, 25)
        edit_button.clicked.connect(
            lambda _, tid=task.id: self._show_edit_task_dialog(tid)
        )
        actions_layout.addWidget(edit_button)

        delete_button = QPushButton("Supprimer")
        delete_button.setFixedSize(80, 25)
        delete_button.setStyleSheet("background-color: #d32f2f;")
        delete_button.clicked.connect(
            lambda _, tid=task.id: self._confirm_delete_task(tid)
        )
        actions_layout.addWidget(delete_button)

        layout.addLayout(actions_layout)

        return frame

    def _show_add_task_dialog(self):
        """Show dialog for adding a new task."""
        from ..dialogs.task_dialog import TaskDialog

        dialog = TaskDialog(self, self.controller)
        dialog.setWindowTitle("Nouvelle tâche")
        if dialog.exec() == QMessageBox.Accepted:
            pass  # Task is added via the dialog

    def _show_edit_task_dialog(self, task_id):
        """Show dialog for editing an existing task."""
        from ..dialogs.task_dialog import TaskDialog

        task = self.controller.task_service.get_by_id(task_id)
        if task:
            dialog = TaskDialog(self, self.controller, task)
            dialog.setWindowTitle(f"Modifier : {task.title}")
            if dialog.exec() == QMessageBox.Accepted:
                pass  # Task is updated via the dialog

    def _confirm_delete_task(self, task_id):
        """Confirm and delete a task."""
        task = self.controller.task_service.get_by_id(task_id)
        if task:
            reply = QMessageBox.question(
                self,
                "Supprimer la tâche",
                f"Voulez-vous vraiment supprimer la tâche '{task.title}' ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.controller.delete_task(task_id)

    def _show_about_dialog(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "À propos de TaskMaster",
            "<h2>TaskMaster</h2>"
            "<p>Application de gestion de tâches développée avec PySide6.</p>"
            "<p>Version : 0.1.0</p>"
            "<p>Auteur : VibeCode (Mistral AI)</p>"
        )

    def closeEvent(self, event):
        """Handle window close event."""
        # Save any unsaved changes if needed
        event.accept()
