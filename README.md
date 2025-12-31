# CLI Todo Application

A clean, reliable command-line todo application demonstrating all basic CRUD operations with file-based JSON persistence.

## Features

- Add tasks with title and optional description
- List all tasks with ID, title, description, and completion status
- Update task title and/or description
- Mark tasks as complete or incomplete
- Delete tasks
- Automatic data persistence between sessions

## Quick Start

### Prerequisites

- Python 3.13 or newer
- UV for environment management (recommended)

### Installation

1. Clone or download the repository
2. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   # Or with pip: pip install uv
   ```

3. UV will automatically manage the virtual environment - no manual setup needed!

### Usage

**Interactive Mode (Recommended for beginners):**
```bash
uv run todo-cli
```

**Command-line Mode:**
```bash
# Add a task
uv run todo-cli add --title "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
uv run todo-cli list

# Update a task
uv run todo-cli update --id 1 --title "Buy groceries (urgent)"

# Mark task as complete
uv run todo-cli complete --id 1

# Mark task as incomplete
uv run todo-cli incomplete --id 1

# Delete a task
uv run todo-cli delete --id 1

# Get help
uv run todo-cli --help
uv run todo-cli add --help
```

**Alternative (without UV):**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run directly
python3 -m src.main list
python3 -m src.main add --title "Task"
```

## Data Storage

Tasks are stored in `~/.todo_cli_tasks.json` in your home directory.

## Project Structure

```
src/
├── __init__.py
├── main.py              # Entry point
├── cli/                 # CLI interface
│   └── commands.py      # Command handlers
├── models/              # Data models
│   └── task.py          # Task entity
└── services/            # Business logic
    ├── task_service.py  # Task CRUD operations
    └── storage.py       # JSON file persistence
```

## Architecture

- **CLI Layer**: Command parsing and user interaction using argparse
- **Service Layer**: Business logic for task management
- **Storage Layer**: Atomic JSON file persistence
- **Model Layer**: Task entity with validation

## Code Standards

- PEP 8 compliant
- Clear separation of concerns
- No external dependencies (standard library only)
- Comprehensive error handling

## License

MIT License
