# CLI API Contract

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31
**Status**: Final

This document defines the command-line interface specification for the CLI Todo Application.

## Entry Point

**Command**: `python src/main.py [command] [options]`

All operations are performed by invoking the main entry point with the appropriate subcommand.

---

## Commands Overview

| Command | Purpose | Required Args | Optional Args |
|---------|---------|---------------|---------------|
| `add` | Create a new task | `--title` | `--description` |
| `list` | Display all tasks | None | None |
| `update` | Update task title/description | `--id` | `--title`, `--description` |
| `delete` | Delete a task | `--id` | None |
| `complete` | Mark task as complete | `--id` | None |
| `incomplete` | Mark task as incomplete | `--id` | None |

**Note**: At least one of `--title` or `--description` must be provided for `update` command.

---

## Command Specifications

### Command: `add`

Creates a new task with a required title and optional description.

**Syntax**:
```bash
python src/main.py add --title "<title>" [--description "<description>"]
```

**Arguments**:
- `--title` (required): Task title
  - Type: string
  - Constraints: 1-200 characters, non-empty, non-whitespace
  - Example: `--title "Buy groceries"`

- `--description` (optional): Task description
  - Type: string
  - Constraints: 0-1000 characters
  - Default: Empty string
  - Example: `--description "Milk, eggs, bread"`

**Success Output**:
```
Task created successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: incomplete
```

**Error Cases**:
- Missing `--title` flag: `Error: --title is required for add command`
- Empty or whitespace-only title: `Error: Title cannot be empty or whitespace`
- Title exceeds 200 characters: `Error: Title must be 200 characters or less`
- Description exceeds 1000 characters: `Error: Description must be 1000 characters or less`
- File permission error: `Error: Cannot save task. Permission denied writing to ~/.todo_cli_tasks.json`
- Other file errors: `Error: Failed to save task: <specific error message>`

**Exit Codes**:
- Success: `0`
- Validation error: `1`
- File I/O error: `2`

---

### Command: `list`

Displays all tasks in a readable format, showing ID, title, description, and completion status.

**Syntax**:
```bash
python src/main.py list
```

**Arguments**: None

**Success Output** (with tasks):
```
Tasks (3 total):

ID: 1  [incomplete]  Buy groceries
    Description: Milk, eggs, bread

ID: 2  [complete]    Write report
    Description: Monthly performance review

ID: 3  [incomplete]  Call dentist
    Description: Schedule appointment
```

**Success Output** (empty list):
```
No tasks found. Use 'add' command to create a task.
```

**Error Cases**:
- File not found (auto-created): No error, empty list displayed
- Corrupted data file: `Warning: Data file corrupted. Starting with empty task list.`
- File permission error: `Error: Cannot read tasks. Permission denied accessing ~/.todo_cli_tasks.json`

**Exit Codes**:
- Success: `0`
- File I/O error: `2`

---

### Command: `update`

Updates an existing task's title and/or description by task ID.

**Syntax**:
```bash
python src/main.py update --id <id> [--title "<title>"] [--description "<description>"]
```

**Arguments**:
- `--id` (required): Task ID to update
  - Type: integer
  - Constraints: Must be a valid existing task ID
  - Example: `--id 1`

- `--title` (optional): New task title
  - Type: string
  - Constraints: 1-200 characters, non-empty, non-whitespace (if provided)
  - Example: `--title "Buy groceries (urgent)"`

- `--description` (optional): New task description
  - Type: string
  - Constraints: 0-1000 characters (if provided)
  - Example: `--description "Milk, eggs, bread - do today!"`

**Validation Rule**: At least one of `--title` or `--description` must be provided.

**Success Output**:
```
Task updated successfully!
ID: 1
Title: Buy groceries (urgent)
Description: Milk, eggs, bread - do today!
Status: incomplete
```

**Error Cases**:
- Missing `--id` flag: `Error: --id is required for update command`
- Missing `--title` and `--description`: `Error: At least one of --title or --description must be provided`
- Invalid or non-existent ID: `Error: Task with ID 999 not found. Valid IDs: 1, 2, 3`
- Empty or whitespace-only title: `Error: Title cannot be empty or whitespace`
- Title exceeds 200 characters: `Error: Title must be 200 characters or less`
- Description exceeds 1000 characters: `Error: Description must be 1000 characters or less`
- File permission error: `Error: Cannot update task. Permission denied writing to ~/.todo_cli_tasks.json`

**Exit Codes**:
- Success: `0`
- Validation error: `1`
- Task not found: `1`
- File I/O error: `2`

---

### Command: `delete`

Deletes a task by ID.

**Syntax**:
```bash
python src/main.py delete --id <id>
```

**Arguments**:
- `--id` (required): Task ID to delete
  - Type: integer
  - Constraints: Must be a valid existing task ID
  - Example: `--id 1`

**Success Output**:
```
Task deleted successfully!
ID: 1
Title: Buy groceries
```

**Error Cases**:
- Missing `--id` flag: `Error: --id is required for delete command`
- Invalid or non-existent ID: `Error: Task with ID 999 not found. Valid IDs: 1, 2, 3`
- File permission error: `Error: Cannot delete task. Permission denied writing to ~/.todo_cli_tasks.json`

**Exit Codes**:
- Success: `0`
- Task not found: `1`
- File I/O error: `2`

---

### Command: `complete`

Marks a task as complete.

**Syntax**:
```bash
python src/main.py complete --id <id>
```

**Arguments**:
- `--id` (required): Task ID to mark complete
  - Type: integer
  - Constraints: Must be a valid existing task ID
  - Example: `--id 1`

**Success Output**:
```
Task marked as complete!
ID: 1
Title: Buy groceries
```

**Error Cases**:
- Missing `--id` flag: `Error: --id is required for complete command`
- Invalid or non-existent ID: `Error: Task with ID 999 not found. Valid IDs: 1, 2, 3`
- File permission error: `Error: Cannot update task. Permission denied writing to ~/.todo_cli_tasks.json`

**Exit Codes**:
- Success: `0`
- Task not found: `1`
- File I/O error: `2`

---

### Command: `incomplete`

Marks a task as incomplete (undoes completion).

**Syntax**:
```bash
python src/main.py incomplete --id <id>
```

**Arguments**:
- `--id` (required): Task ID to mark incomplete
  - Type: integer
  - Constraints: Must be a valid existing task ID
  - Example: `--id 1`

**Success Output**:
```
Task marked as incomplete!
ID: 1
Title: Buy groceries
```

**Error Cases**:
- Missing `--id` flag: `Error: --id is required for incomplete command`
- Invalid or non-existent ID: `Error: Task with ID 999 not found. Valid IDs: 1, 2, 3`
- File permission error: `Error: Cannot update task. Permission denied writing to ~/.todo_cli_tasks.json`

**Exit Codes**:
- Success: `0`
- Task not found: `1`
- File I/O error: `2`

---

## Help Command

Display usage information.

**Syntax**:
```bash
python src/main.py --help
```

**Output**:
```
usage: main.py [-h] {add,list,update,delete,complete,incomplete} ...

CLI Todo Application - Manage your tasks from the command line.

positional arguments:
  {add,list,update,delete,complete,incomplete}
    add                 Add a new task
    list                List all tasks
    update              Update a task
    delete              Delete a task
    complete            Mark task as complete
    incomplete          Mark task as incomplete

options:
  -h, --help            show this help message and exit
```

**Command-Specific Help**:
```bash
python src/main.py add --help
```

---

## Global Behavior

### Error Message Format
All error messages follow this pattern:
```
Error: <clear, actionable message>
```

### Data Persistence
All write operations (add, update, delete, complete, incomplete) persist changes to `~/.todo_cli_tasks.json` immediately.

### File Auto-Creation
- If the data file does not exist on any operation, it is created automatically
- This is transparent to the user (no special setup required)

### Task ID Behavior
- Task IDs are auto-incrementing integers starting from 1
- Deleting a task does not reuse its ID
- IDs are unique and never change

### Unicode Support
- Task titles and descriptions support Unicode (emojis, special characters)
- JSON format natively handles Unicode
- No encoding issues on modern systems

---

## Exit Codes Summary

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success |
| `1` | Validation error, task not found, or invalid input |
| `2` | File I/O error (permission denied, disk full, etc.) |

---

## Interactive Mode

**Not Supported**: The application is non-interactive. All operations are single-command executions.

---

## Environment Variables

**Not Used**: The application does not use any environment variables. Configuration is implicit (data file location).

---

## Usage Examples

### Basic Workflow
```bash
# Add tasks
python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
python src/main.py add --title "Write report" --description "Monthly review"

# List tasks
python src/main.py list

# Update a task
python src/main.py update --id 1 --title "Buy groceries (urgent)"

# Mark a task complete
python src/main.py complete --id 1

# Delete a task
python src/main.py delete --id 2
```

### Edge Case Handling
```bash
# Try to update non-existent task
python src/main.py update --id 999 --title "New title"
# Error: Task with ID 999 not found. Valid IDs: 1, 2

# Try to add task without title
python src/main.py add --description "No title"
# Error: --title is required for add command

# Try to add empty title
python src/main.py add --title ""
# Error: Title cannot be empty or whitespace

# List when no tasks exist
python src/main.py list
# No tasks found. Use 'add' command to create a task.
```

