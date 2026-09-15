"""Dialog for adding and editing tasks."""

from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from ...app.controllers.task_controller import TaskController
from ...app.models.task import Task


class TaskDialog(QDialog):
    """
    Dialog for creating or editing tasks.

    Features:
    - Form for all task fields
    - Validation
    - Confirmation handling
    """

    def __init__(
        self,
        parent=None,
        controller: TaskController | None = None,
        task: Task | None = None
    ):
        """
        Initialize the task dialog.

        Args:
            parent: Parent widget.
            controller: TaskController instance.
            task: Optional Task to edit. If None, creates a new task.
        """
        super().__init__(parent)
        self.controller = controller
        self.task = task
        self.is_edit_mode = task is not None

        title = self.task.title if self.task else "Nouvelle tâche"
        self.setWindowTitle("Nouvelle tâche" if not self.is_edit_mode else f"Modifier : {title}")
        self.setMinimumWidth(400)

        self._setup_ui()

        if self.task:
            self._populate_form()

    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Form
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Entrez un titre...")
        form_layout.addRow("Titre *:", self.title_input)

        # Description
        self.description_input = QPlainTextEdit()
        self.description_input.setPlaceholderText("Entrez une description (optionnel)...")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description :", self.description_input)

        # Priority
        self.priority_input = QSpinBox()
        self.priority_input.setRange(1, 5)
        self.priority_input.setValue(3)
        self.priority_input.setToolTip("1 = Très faible, 5 = Critique")
        form_layout.addRow("Priorité (1-5) :", self.priority_input)

        # Due date
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(datetime.now().date())
        self.due_date_input.setDisplayFormat("dd/MM/yyyy")
        self.due_date_input.setSpecialValueText("Aucune date")
        self.due_date_checkbox = QPushButton("✓ Utiliser une date")
        self.due_date_checkbox.setCheckable(True)
        self.due_date_checkbox.setChecked(True)
        self.due_date_checkbox.clicked.connect(self._toggle_due_date)

        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(self.due_date_input)
        due_date_layout.addWidget(self.due_date_checkbox)
        form_layout.addRow("Date limite :", due_date_layout)

        # Tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tag1, Tag2, Tag3 (séparés par des virgules)")
        form_layout.addRow("Tags :", self.tags_input)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self._accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply styles
        self._apply_styles()

    def _apply_styles(self):
        """Apply custom styles to the dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }

            QLabel {
                color: #ffffff;
            }

            QLineEdit, QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3f41;
                border-radius: 3px;
                padding: 5px;
            }

            QLineEdit:focus, QPlainTextEdit:focus {
                border: 1px solid #0078d7;
            }

            QSpinBox, QDateEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3f41;
                border-radius: 3px;
                padding: 5px;
            }

            QSpinBox:focus, QDateEdit:focus {
                border: 1px solid #0078d7;
            }

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

            QDialogButtonBox QPushButton {
                min-width: 80px;
            }

            QDialogButtonBox QPushButton:first {
                background-color: #0078d7;
            }

            QDialogButtonBox QPushButton:last {
                background-color: #4a4d4f;
            }
        """)

    def _toggle_due_date(self, checked: bool):
        """Toggle due date field enabled state."""
        self.due_date_input.setEnabled(checked)
        if checked:
            self.due_date_checkbox.setText("✓ Utiliser une date")
        else:
            self.due_date_checkbox.setText("✗ Pas de date")

    def _populate_form(self):
        """Populate the form with task data."""
        if not self.task:
            return

        self.title_input.setText(self.task.title)
        self.description_input.setPlainText(self.task.description)
        self.priority_input.setValue(self.task.priority)

        if self.task.due_date:
            self.due_date_input.setDate(self.task.due_date.date())
            self.due_date_checkbox.setChecked(True)
        else:
            self.due_date_checkbox.setChecked(False)
            self.due_date_input.setEnabled(False)

        if self.task.tags:
            self.tags_input.setText(", ".join(self.task.tags))

    def _accept(self):
        """Handle dialog acceptance (OK button)."""
        # Validate inputs
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation", "Le titre est obligatoire.")
            return

        description = self.description_input.toPlainText().strip()
        priority = self.priority_input.value()

        # Handle due date
        due_date = None
        if self.due_date_checkbox.isChecked():
            due_date = self.due_date_input.date().toPython()
            due_datetime = datetime.combine(due_date, datetime.min.time())
            # Add 23:59:59 to include the entire day
            due_date = due_datetime + timedelta(days=1, seconds=-1)

        tags_str = self.tags_input.text().strip()
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        try:
            if self.is_edit_mode and self.task:
                # Update existing task
                Task(
                    id=self.task.id,
                    title=title,
                    description=description,
                    created_at=self.task.created_at,
                    due_date=due_date,
                    completed=self.task.completed,
                    priority=priority,
                    tags=tags
                )
                self.controller.update_task(
                    self.task.id,
                    title,
                    description,
                    priority,
                    tags_str,
                    self.task.completed
                )
            else:
                # Add new task
                self.controller.add_task(
                    title=title,
                    description=description,
                    priority=priority,
                    tags_str=tags_str
                )

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")

    def _get_task_data(self) -> dict:
        """Get the current form data as a dictionary."""
        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "priority": self.priority_input.value(),
            "due_date": self.due_date_input.date().toPython() if self.due_date_checkbox.isChecked() else None,
            "tags": [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        }
