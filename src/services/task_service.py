"""Task service for CLI Todo Application.

This module provides business logic for CRUD operations on tasks.
"""

from typing import List, Optional

from src.models.task import Task, TaskList
from src.services.storage import load_tasks, save_tasks, get_valid_task_ids


class TaskNotFoundError(Exception):
    """Raised when a task with given ID is not found."""
    pass


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class TaskService:
    """Service for managing task operations with persistence."""

    def __init__(self):
        """Initialize TaskService."""
        self._task_list = None
        self._load_data()

    def _load_data(self):
        """Load task data from storage."""
        try:
            self._task_list = load_tasks()
        except Exception as e:
            # If loading fails, start with empty task list
            self._task_list = TaskList()
            raise ValidationError(f"Failed to load tasks: {e}")

    def _save_data(self):
        """Save task data to storage."""
        try:
            save_tasks(self._task_list)
        except Exception as e:
            raise ValidationError(f"Failed to save tasks: {e}")

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: Task title (required, max 200 chars, non-empty).
            description: Task description (optional, max 1000 chars).

        Returns:
            Task: The created task.

        Raises:
            ValidationError: If validation fails.
        """
        # Validate title
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty or whitespace")
        if len(title) > 200:
            raise ValidationError("Title must be 200 characters or less")

        # Validate description
        if len(description) > 1000:
            raise ValidationError("Description must be 1000 characters or less")

        # Create task with next available ID
        task = Task(
            task_id=self._task_list.next_id,
            title=title.strip(),
            description=description,
            complete=False
        )

        # Add to task list
        self._task_list.tasks.append(task)
        self._task_list.next_id += 1

        # Persist
        self._save_data()

        return task

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.

        Args:
            task_id: Task ID to retrieve.

        Returns:
            Task: The task with the given ID.

        Raises:
            TaskNotFoundError: If task ID not found.
            ValidationError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValidationError(f"Invalid task ID: {task_id}")

        for task in self._task_list.tasks:
            if task.id == task_id:
                return task

        raise TaskNotFoundError(
            f"Task with ID {task_id} not found"
        )

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: Task ID to update.
            title: New title (optional).
            description: New description (optional).

        Returns:
            Task: The updated task.

        Raises:
            TaskNotFoundError: If task ID not found.
            ValidationError: If validation fails or neither title nor description provided.
        """
        if title is None and description is None:
            raise ValidationError(
                "At least one of title or description must be provided"
            )

        # Get the task
        task = self.get_task(task_id)

        # Update title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValidationError("Title cannot be empty or whitespace")
            if len(title) > 200:
                raise ValidationError("Title must be 200 characters or less")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            if len(description) > 1000:
                raise ValidationError("Description must be 1000 characters or less")
            task.description = description

        # Persist
        self._save_data()

        return task

    def delete_task(self, task_id: int) -> Task:
        """Delete a task by ID.

        Args:
            task_id: Task ID to delete.

        Returns:
            Task: The deleted task.

        Raises:
            TaskNotFoundError: If task ID not found.
            ValidationError: If task_id is invalid.
        """
        # Get the task first
        task = self.get_task(task_id)

        # Remove from list
        self._task_list.tasks = [
            t for t in self._task_list.tasks if t.id != task_id
        ]

        # Persist
        self._save_data()

        return task

    def toggle_complete(self, task_id: int, complete: bool) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Task ID to update.
            complete: Desired completion status (True/False).

        Returns:
            Task: The updated task.

        Raises:
            TaskNotFoundError: If task ID not found.
            ValidationError: If task_id is invalid.
        """
        task = self.get_task(task_id)
        task.complete = complete

        # Persist
        self._save_data()

        return task

    def list_all(self) -> List[Task]:
        """List all tasks.

        Returns:
            List[Task]: List of all tasks.
        """
        return self._task_list.tasks[:]

    def get_next_id(self) -> int:
        """Get the next available task ID.

        Returns:
            int: Next available ID.
        """
        return self._task_list.next_id

    def get_valid_ids(self) -> List[int]:
        """Get list of valid task IDs.

        Returns:
            List[int]: Sorted list of valid task IDs.
        """
        return get_valid_task_ids()
