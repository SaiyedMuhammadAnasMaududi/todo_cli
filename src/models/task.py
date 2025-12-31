"""Task model for CLI Todo Application.

This module defines the Task entity representing a single todo item.
"""


class Task:
    """Represents a single todo item.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task (required, max 200 chars).
        description (str): Optional detailed description (max 1000 chars).
        complete (bool): Completion status, defaults to False.
    """

    def __init__(self, task_id: int, title: str, description: str = "",
                 complete: bool = False):
        """Initialize a new Task instance.

        Args:
            task_id: Unique identifier for the task.
            title: Title of the task (required).
            description: Optional description (default: "").
            complete: Completion status (default: False).

        Raises:
            ValueError: If title is invalid (empty, whitespace-only, or too long).
        """
        self.id = task_id
        self._title = None
        self.title = title  # This will call the setter with validation
        self._description = None
        self.description = description  # This will call the setter with validation
        self.complete = complete

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set the task title with validation.

        Args:
            value: The title to set.

        Raises:
            ValueError: If title is empty, whitespace-only, or exceeds 200 chars.
        """
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace")
        if len(value) > 200:
            raise ValueError("Title must be 200 characters or less")
        self._title = value.strip()

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the task description with validation.

        Args:
            value: The description to set.

        Raises:
            ValueError: If description exceeds 1000 characters.
        """
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        if len(value) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        self._description = value

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "complete": self.complete
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from dictionary.

        Args:
            data: Dictionary containing task data.

        Returns:
            Task: New Task instance created from the dictionary.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if "id" not in data or "title" not in data:
            raise ValueError("Task data must contain 'id' and 'title' fields")

        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            complete=data.get("complete", False)
        )

    def __repr__(self) -> str:
        """Return string representation of the task."""
        status = "complete" if self.complete else "incomplete"
        return f"Task(id={self.id}, title='{self.title}', status={status})"


class TaskList:
    """Represents a collection of tasks with auto-incrementing IDs."""

    def __init__(self, tasks: list = None, next_id: int = 1):
        """Initialize a TaskList.

        Args:
            tasks: List of Task objects (default: []).
            next_id: Next available ID for new tasks (default: 1).
        """
        self.tasks = tasks[:] if tasks else []
        self.next_id = next_id

    def to_dict(self) -> dict:
        """Convert task list to dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the task list.
        """
        return {
            "tasks": [task.to_dict() for task in self.tasks],
            "next_id": self.next_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskList":
        """Create a TaskList instance from dictionary.

        Args:
            data: Dictionary containing task list data.

        Returns:
            TaskList: New TaskList instance created from the dictionary.
        """
        tasks = []
        for task_data in data.get("tasks", []):
            try:
                tasks.append(Task.from_dict(task_data))
            except ValueError:
                # Skip invalid tasks but continue loading
                pass

        next_id = data.get("next_id", 1)

        # Recalculate next_id if needed
        if tasks:
            max_id = max(task.id for task in tasks if task.id is not None)
            next_id = max(next_id, max_id + 1)

        return cls(tasks=tasks, next_id=next_id)

    def __repr__(self) -> str:
        """Return string representation of the task list."""
        return f"TaskList(count={len(self.tasks)}, next_id={self.next_id})"
