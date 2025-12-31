"""Storage service for CLI Todo Application.

This module handles JSON file persistence with atomic write operations.
"""

import json
import os
from pathlib import Path
from typing import Optional

from src.models.task import TaskList


# Storage file location in user's home directory
STORAGE_PATH = Path.home() / ".todo_cli_tasks.json"


class StorageError(Exception):
    """Base exception for storage errors."""
    pass


class PermissionError(StorageError):
    """Raised when file permission errors occur."""
    pass


class CorruptedDataError(StorageError):
    """Raised when data file is corrupted."""
    pass


def load_tasks() -> TaskList:
    """Load tasks from JSON storage file.

    Returns:
        TaskList: Loaded task list, or empty TaskList if file doesn't exist
                  or is corrupted.

    Raises:
        PermissionError: If cannot read file due to permissions.
        StorageError: For other file I/O errors.
    """
    if not STORAGE_PATH.exists():
        # File doesn't exist, return empty task list
        return TaskList()

    try:
        with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return TaskList.from_dict(data)
    except PermissionError as e:
        raise PermissionError(
            f"Cannot read tasks. Permission denied accessing {STORAGE_PATH}"
        ) from e
    except json.JSONDecodeError as e:
        # File exists but is corrupted
        raise CorruptedDataError(
            f"Data file corrupted: {STORAGE_PATH}"
        ) from e
    except OSError as e:
        raise StorageError(
            f"Failed to load tasks from {STORAGE_PATH}: {e}"
        ) from e


def save_tasks(task_list: TaskList) -> None:
    """Save tasks to JSON storage file using atomic write.

    Args:
        task_list: TaskList to save.

    Raises:
        PermissionError: If cannot write file due to permissions.
        StorageError: For other file I/O errors.
    """
    # Ensure parent directory exists (should be home directory)
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create temporary file in same directory
    temp_path = STORAGE_PATH.with_suffix('.tmp')

    try:
        # Write to temporary file
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(task_list.to_dict(), f, indent=2, ensure_ascii=False)

        # Atomic rename: only succeeds if write was complete
        os.replace(temp_path, STORAGE_PATH)

    except PermissionError as e:
        # Clean up temp file if exists
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        raise PermissionError(
            f"Cannot save task. Permission denied writing to {STORAGE_PATH}"
        ) from e
    except OSError as e:
        # Clean up temp file if exists
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        raise StorageError(
            f"Failed to save task to {STORAGE_PATH}: {e}"
        ) from e


def get_valid_task_ids() -> list[int]:
    """Get list of valid task IDs from storage.

    Returns:
        list[int]: List of valid task IDs, sorted.
    """
    try:
        task_list = load_tasks()
        return sorted(task.id for task in task_list.tasks)
    except (StorageError, CorruptedDataError):
        # If we can't load, return empty list
        return []
