# Quick Start Guide

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31
**Status**: Final

This guide will help you get the CLI Todo Application up and running in minutes.

---

## Prerequisites

- Python 3.13 or newer installed
- Basic familiarity with command-line interface
-  UV for environment management (recommended)

---

## Installation

### Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd todo_cli
```

Or download the source code and navigate to the project directory.

### Step 2: Set Up the Environment

**Option A: Using UV (Recommended)**

```bash
# Install UV if not already installed
pip install uv

# Create virtual environment
uv venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies (none needed for this project)
uv pip install -e .
```

**Option B: Using Standard Python venv**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Verify Installation

```bash
python src/main.py --help
```

You should see the help message with all available commands.

---

## Your First Task

### Add a Task

```bash
python src/main.py add --title "My first task" --description "Learning the CLI todo app"
```

**Output**:
```
Task created successfully!
ID: 1
Title: My first task
Description: Learning the CLI todo app
Status: incomplete
```

### List All Tasks

```bash
python src/main.py list
```

**Output**:
```
Tasks (1 total):

ID: 1  [incomplete]  My first task
    Description: Learning the CLI todo app
```

---

## Common Operations

### Create Multiple Tasks

```bash
python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
python src/main.py add --title "Write report"
python src/main.py add --title "Call dentist" --description "Schedule checkup"
```

### Mark Tasks Complete

```bash
python src/main.py complete --id 1
python src/main.py complete --id 3
```

### View Updated Task List

```bash
python src/main.py list
```

**Output**:
```
Tasks (3 total):

ID: 1  [complete]    Buy groceries
    Description: Milk, eggs, bread

ID: 2  [incomplete]  Write report
    Description:

ID: 3  [complete]    Call dentist
    Description: Schedule checkup
```

### Update a Task

```bash
python src/main.py update --id 2 --title "Write quarterly report" --description "Due next Friday"
```

### Mark Task Incomplete

```bash
python src/main.py incomplete --id 1
```

### Delete a Task

```bash
python src/main.py delete --id 3
```

---

## Tips

### Task IDs are Auto-Assigned
When you add a task, the system automatically assigns it an ID. This ID never changes, even if you delete other tasks.

### Task IDs Are Not Reused
If you delete task #2, the next task you add will be #3, not #2. Deleted IDs are permanently removed.

### Get Help for Any Command
```bash
python src/main.py add --help
python src/main.py update --help
```

### View Available Commands
```bash
python src/main.py --help
```

### Data Persistence
All tasks are saved automatically to `~/.todo_cli_tasks.json` (in your home directory). Tasks persist between application restarts and system reboots.

---

## Troubleshooting

### "Command not found: python"
Make sure Python is installed and in your PATH. Try `python3` instead of `python`:
```bash
python3 src/main.py --help
```

### "Permission denied"
If you see file permission errors, ensure you have write access to your home directory where the data file is stored.

### "Task with ID X not found"
Use the `list` command to see all valid task IDs:
```bash
python src/main.py list
```

### Corrupted Data File
If the data file becomes corrupted, the application will automatically start with an empty task list and warn you.

---

## Example Session

```bash
# Start fresh
$ python src/main.py list
No tasks found. Use 'add' command to create a task.

# Add tasks
$ python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
Task created successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: incomplete

$ python src/main.py add --title "Write report"
Task created successfully!
ID: 2
Title: Write report
Description:
Status: incomplete

# View tasks
$ python src/main.py list
Tasks (2 total):

ID: 1  [incomplete]  Buy groceries
    Description: Milk, eggs, bread

ID: 2  [incomplete]  Write report
    Description:

# Complete first task
$ python src/main.py complete --id 1
Task marked as complete!
ID: 1
Title: Buy groceries

# Update second task
$ python src/main.py update --id 2 --title "Write quarterly report" --description "Due Friday"
Task updated successfully!
ID: 2
Title: Write quarterly report
Description: Due Friday
Status: incomplete

# Final list
$ python src/main.py list
Tasks (2 total):

ID: 1  [complete]    Buy groceries
    Description: Milk, eggs, bread

ID: 2  [incomplete]  Write quarterly report
    Description: Due Friday

# Delete completed task
$ python src/main.py delete --id 1
Task deleted successfully!
ID: 1
Title: Buy groceries
```

---

## Next Steps

- Read the [CLI API Contract](contracts/cli-api.md) for detailed command specifications
- Review the [Data Model](data-model.md) to understand how tasks are structured
- Check the [Feature Specification](spec.md) for complete requirements

---

## Data File Location

Your tasks are stored in:
- **Linux/macOS**: `~/.todo_cli_tasks.json`
- **Windows**: `C:\Users\<username>\.todo_cli_tasks.json`

You can back up this file to save your tasks or copy it to another machine.

---

## Uninstallation

To remove the application:
```bash
# Delete the virtual environment
rm -rf venv  # or rmdir /s venv on Windows

# Delete the data file (optional)
rm ~/.todo_cli_tasks.json  # or delete manually on Windows

# Remove the source code directory
```

---

## Getting Help

- Use `--help` flag for command assistance
- Check error messages for specific guidance
- Review this guide and other documentation in the `specs/` directory

---

**Happy task managing!**
