# Research: CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31
**Status**: Complete

This document captures research findings and technology decisions for the CLI Todo Application implementation.

## Research Questions Resolved

### RQ-001: CLI Argument Parsing Library

**Question**: Which library should be used for CLI argument parsing?

**Decision**: Use `argparse` from Python standard library

**Rationale**:
- Part of Python standard library (no external dependencies)
- Well-documented and battle-tested
- Provides all needed functionality: subcommands, arguments, help text
- Aligns with constitution principle of simplicity
- Sufficient for CLI complexity defined in spec (5 basic commands)

**Alternatives Considered**:
- `click`: More feature-rich, but external dependency adds complexity
- `typer`: Modern and type-safe, but external dependency and learning curve
- Custom parsing: Too complex, reinventing the wheel

---

### RQ-002: JSON File Storage Location

**Question**: Where should the JSON data file be stored?

**Decision**: Store in user's home directory as `.todo_cli_tasks.json`

**Rationale**:
- Cross-platform compatible (works on Linux, macOS, Windows)
- Follows convention for application config/data files
- Persistent across application restarts
- Easy for users to locate and backup
- No permission issues (users have write access to home directory)

**Alternatives Considered**:
- Current working directory: Not persistent if user changes directories
- `/tmp`: Not persistent across reboots
- Application-specific config directory (`~/.config/todo/`): More complex path handling
- Environment variable: Adds setup complexity for users

---

### RQ-003: Task ID Generation Strategy

**Question**: How should unique task IDs be generated?

**Decision**: Use auto-incrementing integer IDs starting from 1

**Rationale**:
- Simple and human-readable
- Easy to reference in CLI commands
- Minimal collision risk for single-user scenario
- Deterministic and predictable
- Easy to implement without external libraries

**Alternatives Considered**:
- UUIDs: More unique but harder to reference in CLI (long strings)
- Timestamp-based: Predictable but can have collision issues
- Hash of title content: Not deterministic after title updates

---

### RQ-004: Atomic File Write Pattern

**Question**: How to ensure atomic writes to prevent data corruption?

**Decision**: Write to temporary file, then use atomic rename operation

**Rationale**:
- Standard pattern for safe file writes
- Prevents data corruption if write fails mid-operation
- Works across platforms (os.replace() is atomic on POSIX, Windows)
- Simple implementation using only standard library

**Implementation Pattern**:
1. Read existing data from storage file
2. Write new data to temporary file in same directory
3. Use `os.replace()` to atomically rename temp file to target file

**Alternatives Considered**:
- Direct write: Risk of corruption if interrupted
- Backup file approach: Adds complexity, cleanup needed
- Database transactions: Overkill for JSON file storage

---

### RQ-005: Error Handling Strategy

**Question**: What error handling patterns should be used?

**Decision**: Try-except blocks with user-friendly messages for all I/O operations

**Rationale**:
- Clear separation between technical errors and user messages
- Specific error types caught (FileNotFoundError, PermissionError, JSONDecodeError)
- Provides actionable feedback to users
- Prevents application crashes

**Error Categories**:
- File not found: Create new file automatically
- Permission denied: Clear message with suggestions
- Corrupted JSON: Warn user and initialize empty task list
- Invalid task ID: Specific message with valid ID ranges
- Missing required fields: Clear indication of what's needed

**Alternatives Considered**:
- Silent failure: Violates correctness principle
- Crash on error: Poor user experience
- Logging only: Not useful for CLI users

---

### RQ-006: Data Validation Approach

**Question**: How to validate task data before storage?

**Decision**: Input validation at CLI layer + in-memory validation before persistence

**Rationale**:
- Catch errors early (CLI layer) for better user experience
- Double-check before persistence to ensure data integrity
- Simple validation rules: title required and non-empty
- Use Python's truthiness and type checking

**Validation Rules**:
- Title: Required, non-empty string, max 200 characters (prevent abuse)
- Description: Optional, string, max 1000 characters (reasonable limit)
- Status: Boolean or enum (complete/incomplete), default to incomplete
- Task ID: Must exist in task list for update/delete/complete operations

**Alternatives Considered**:
- Only validate at persistence layer: Poor UX (errors discovered late)
- Schema validation library (pydantic): External dependency, overkill
- No validation: Violates correctness principle

---

### RQ-007: Python 3.13+ Specific Features

**Question**: Are there Python 3.13+ features that should be leveraged?

**Decision**: Use standard Python patterns; no 3.13-specific features required

**Rationale**:
- Maintains compatibility with earlier 3.x versions if needed
- Spec requires 3.13+ but doesn't mandate using new features
- Focus on simplicity and clarity over bleeding-edge features
- Standard patterns are well-understood by Python developers

**Features Considered**:
- Type hints: Use for clarity but not mandatory
- f-strings: Use for string formatting (available since 3.6)
- match/case: Not needed for this complexity level
- Error unions: Not needed for this use case

**Alternatives Considered**:
- Latest features only: Reduces clarity for developers on older Python versions
- Type checking with mypy: Out of scope per spec
- Dataclasses: Could be used but plain classes are simpler

---

### RQ-008: Data Model Design

**Question**: What data structure should represent a task?

**Decision**: Plain Python class with dictionary serialization

**Rationale**:
- Simple and readable
- Easy to serialize to/from JSON
- No external dependencies
- Clear separation between domain model and persistence

**Task Structure**:
```python
class Task:
    def __init__(self, task_id: int, title: str, description: str = "", complete: bool = False):
        self.id = task_id
        self.title = title
        self.description = description
        self.complete = complete

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "complete": self.complete
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            complete=data.get("complete", False)
        )
```

**Alternatives Considered**:
- NamedTuple: Immutable, tasks need to be updated
- Dataclass: More boilerplate than needed
- Dictionary only: No type safety, harder to maintain

---

## Summary of Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI Parsing | `argparse` (stdlib) | No dependencies, sufficient features |
| Storage Location | `~/.todo_cli_tasks.json` | Cross-platform, persistent, user-accessible |
| Task IDs | Auto-increment integers | Simple, readable, deterministic |
| File Writes | Temp file + atomic rename | Safe, standard pattern |
| Error Handling | Try-except with user messages | Clear UX, prevents crashes |
| Validation | CLI + in-memory checks | Early feedback, data integrity |
| Python Features | Standard patterns | Clarity, compatibility |
| Data Model | Plain class with dict serialization | Simple, testable, no deps |

## Open Questions

None - all research questions resolved.

## Follow-up Considerations

1. **Performance**: Current design will handle 10s to low 100s of tasks efficiently. No optimization needed.
2. **Scalability**: If task count grows beyond 1000, consider switching to SQLite (out of scope for now).
3. **Unicode**: JSON natively handles Unicode, so task titles/descriptions with emojis or special characters will work correctly.
4. **Concurrent Access**: Single-user scenario per spec. If multi-user needed, would require file locking or database (out of scope).

