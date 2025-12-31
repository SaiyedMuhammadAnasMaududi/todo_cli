# Data Model: CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31
**Status**: Complete

This document defines the data entities, their attributes, relationships, and validation rules for the CLI Todo Application.

## Entity: Task

### Purpose
Represents a single todo item in the user's task list.

### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id` | integer | Yes | Auto-generated | Unique identifier for the task (auto-incrementing starting from 1) |
| `title` | string | Yes | N/A | Title/description of the task. Max 200 characters. |
| `description` | string | No | Empty string (`""`) | Optional detailed description of the task. Max 1000 characters. |
| `complete` | boolean | No | `False` | Completion status: `True` if task is complete, `False` if incomplete |

### Validation Rules

1. **ID Validation**
   - Must be a positive integer (> 0)
   - Must be unique within the task list
   - Auto-assigned by the system; not user-provided

2. **Title Validation**
   - Required field (cannot be None or empty string)
   - Must be a string
   - Maximum length: 200 characters
   - Cannot contain only whitespace

3. **Description Validation**
   - Optional field (can be None or empty string)
   - Must be a string if provided
   - Maximum length: 1000 characters
   - Can be empty string or whitespace-only

4. **Status Validation**
   - Must be a boolean value (`True` or `False`)
   - Default to `False` (incomplete) on creation
   - Can be toggled between values

### State Transitions

```
[Task Created] → complete = False (incomplete)
       ↓
[User marks complete] → complete = True
       ↓
[User marks incomplete] → complete = False
       ↓
... (can toggle indefinitely)
```

**Transition Rules**:
- Initial state is always `incomplete`
- Status can be toggled from either state to the other
- No other states are possible (e.g., no "in progress", "blocked", etc.)

### Invariants

1. **ID Immutability**: Once assigned, a task's ID never changes.
2. **Persistence**: All task modifications are immediately persisted to storage.
3. **Uniqueness**: No two tasks in the list share the same ID.

---

## Entity: TaskList

### Purpose
Represents the collection of all tasks managed by the application.

### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tasks` | list[Task] | No | Empty list (`[]`) | Collection of Task objects in the system |
| `next_id` | integer | No | `1` | Next available ID for new tasks (auto-increment) |

### Operations

| Operation | Description | Side Effects |
|-----------|-------------|--------------|
| `add_task(title, description)` | Creates a new task with next_id, increments next_id | Persists new task |
| `get_task(task_id)` | Retrieves a task by ID | None |
| `update_task(task_id, title, description)` | Updates task fields | Persists updated task |
| `delete_task(task_id)` | Removes task from list | Persists deletion |
| `toggle_complete(task_id)` | Flips task's complete status | Persists new status |
| `list_all()` | Returns all tasks | None |
| `get_next_id()` | Returns next available ID | Increments next_id |

### Validation Rules

1. **Task Uniqueness**: No duplicate task IDs allowed.
2. **Sequential IDs**: IDs are assigned sequentially (1, 2, 3, ...).
3. **ID Gaps**: Deleting a task creates an ID gap (IDs are not reused).
4. **Empty List Validity**: An empty task list is a valid state.

---

## Data Model in JSON (Persistence Format)

### File Structure
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "complete": false
    },
    {
      "id": 2,
      "title": "Write report",
      "description": "Monthly performance review",
      "complete": true
    }
  ],
  "next_id": 3
}
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["tasks", "next_id"],
  "properties": {
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "complete"],
        "properties": {
          "id": {
            "type": "integer",
            "minimum": 1
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "maxLength": 1000
          },
          "complete": {
            "type": "boolean"
          }
        }
      }
    },
    "next_id": {
      "type": "integer",
      "minimum": 1
    }
  }
}
```

---

## Relationships

### Task ↔ TaskList
- **Relationship**: Composition (TaskList owns Task objects)
- **Cardinality**: One TaskList contains zero or more Tasks
- **Lifetime**: Tasks exist only within a TaskList; they have no independent persistence

### No Other Relationships
- Tasks do not reference each other (no dependencies)
- No task categories, tags, or metadata
- No user entities (single-user application)

---

## Data Lifecycle

### Creation Flow
```
User provides title/description
       ↓
CLI validates input (title required, non-empty, length check)
       ↓
TaskService creates Task object with auto-generated ID
       ↓
TaskService adds Task to TaskList
       ↓
Storage saves TaskList to JSON file atomically
       ↓
User receives confirmation with task ID
```

### Update Flow
```
User provides task ID and new title/description
       ↓
CLI validates task ID (must exist) and input fields
       ↓
TaskService retrieves Task from TaskList
       ↓
TaskService updates Task fields
       ↓
Storage saves TaskList to JSON file atomically
       ↓
User receives confirmation
```

### Deletion Flow
```
User provides task ID
       ↓
CLI validates task ID (must exist)
       ↓
TaskService retrieves Task from TaskList
       ↓
TaskService removes Task from TaskList
       ↓
Storage saves TaskList to JSON file atomically
       ↓
User receives confirmation
       ↓
ID is not reused (permanently removed)
```

---

## Edge Case Handling

### Scenario 1: Corrupted Data File
- **Detection**: JSONDecodeError on file read
- **Resolution**: Initialize empty TaskList (no tasks, next_id = 1)
- **User Action**: Inform user of corruption and that all tasks were lost
- **Persistence**: Overwrite corrupted file with new empty state

### Scenario 2: Empty Data File
- **Detection**: File exists but is empty or contains only whitespace
- **Resolution**: Initialize empty TaskList
- **User Action**: No user notification (normal first-run state)

### Scenario 3: Task with Missing Fields
- **Detection**: JSON parse succeeds but fields are missing
- **Resolution**: Use default values for optional fields, reject if required fields missing
- **User Action**: Inform user of data inconsistency

### Scenario 4: Non-Sequential or Duplicate IDs
- **Detection**: IDs not sequential or duplicates found
- **Resolution**: Recalculate next_id = max(existing_ids) + 1 (or 1 if no tasks)
- **User Action**: No user action needed (transparent recovery)

### Scenario 5: Very Long Task Title/Description
- **Detection**: Input exceeds character limits
- **Resolution**: Reject input with clear error message indicating max length
- **User Action**: User must provide shorter input

---

## Performance Considerations

### Current Scale (10s to low 100s of tasks)
- All operations in-memory after initial file read
- Single file read/write per operation
- Expected latency: < 100ms for typical operations

### Scaling Beyond Design
- **1000+ tasks**: File I/O becomes bottleneck; consider SQLite
- **Concurrent access**: Current design not thread-safe; would need file locking
- **Search/Filter**: Linear scan through tasks; would need indexes for large sets

These are out-of-scope optimizations per the feature specification.

