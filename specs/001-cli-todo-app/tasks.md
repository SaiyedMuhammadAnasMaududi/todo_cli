# Implementation Tasks: CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31
**Status**: Ready for Implementation

This document provides a detailed, actionable task list for implementing the CLI Todo Application. Tasks are organized by user story to enable independent implementation and testing.

---

## Implementation Strategy

**MVP First**: Complete User Story 1 (Create and View Tasks) to deliver a functional MVP. Then incrementally add features.

**Incremental Delivery**: Each user story phase produces a complete, independently testable increment.

**Parallel Opportunities**: Tasks marked with `[P]` can be executed in parallel (different files, no blocking dependencies).

---

## Phase 1: Project Setup

**Goal**: Establish a clean and reproducible development environment with project structure.

- [X] T001 Initialize Python project with UV environment in project root
- [X] T002 [P] Create src/ directory structure with __init__.py files
- [X] T003 [P] Create placeholder main.py entry point in src/main.py
- [X] T004 [P] Create README.md with project description and quick start instructions
- [X] T005 Verify project structure matches implementation plan (cli/, models/, services/ directories)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Implement core data model and storage layer that all user stories depend on.

- [X] T006 [P] Implement Task model in src/models/task.py with attributes (id, title, description, complete), to_dict() and from_dict() methods, and validation logic (title required, max 200 chars; description max 1000 chars)
- [X] T007 [P] Implement JSON storage service in src/services/storage.py with STORAGE_PATH = ~/.todo_cli_tasks.json, load_tasks() method (handles FileNotFoundError, JSONDecodeError, returns empty TaskList on errors), and save_tasks() method using atomic write pattern (temp file + os.replace)
- [X] T008 [P] Implement TaskService in src/services/task_service.py with methods: add_task(title, description), get_task(task_id), update_task(task_id, title, description), delete_task(task_id), toggle_complete(task_id), list_all(), and get_next_id()
- [X] T009 Integrate TaskService with Storage: Update TaskService to use storage.load_tasks() and storage.save_tasks() for all persistence operations
- [X] T010 Add error handling in TaskService: Raise TaskNotFoundError for non-existent task IDs, raise ValidationError for invalid inputs, and catch/propagate storage layer errors with user-friendly messages

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1)

**Goal**: Enable users to add tasks with title/description and view all tasks with IDs and statuses.

**Independent Test**: Add multiple tasks with various titles and descriptions, then list all tasks to verify they appear correctly with IDs and statuses.

### Implementation Tasks

- [X] T011 [P] [US1] Implement add command handler in src/cli/commands.py: Parse --title (required) and --description (optional) arguments, validate title (non-empty, max 200 chars, no whitespace-only), validate description (max 1000 chars), call TaskService.add_task(), and output success message with task details
- [X] T012 [P] [US1] Implement list command handler in src/cli/commands.py: Call TaskService.list_all(), format output with ID, status [incomplete]/[complete], title, and indented description, display "No tasks found" message for empty list, and handle corrupted file warnings
- [X] T013 [US1] Wire up CLI entry point in src/main.py: Create argparse parser with subparser for add/list commands, add help text and command descriptions, route to appropriate command handlers in cli/commands.py, and implement main() function with if __name__ == "__main__"

---

## Phase 4: User Story 2 - Update Task Details (Priority: P2)

**Goal**: Enable users to modify task title and/or description by task ID.

**Independent Test**: Create a task, update its title and description using its ID, verify changes persist when listing tasks again.

### Implementation Tasks

- [X] T014 [P] [US2] Implement update command handler in src/cli/commands.py: Parse --id (required), --title (optional), and --description (optional) arguments, validate at least one of title/description provided, validate task ID exists (call TaskService.get_task()), validate title/description constraints, call TaskService.update_task(), and output success message with updated task details
- [X] T015 [US2] Add update subparser to main.py CLI: Add update command to argparse subparsers, define --id, --title, --description arguments with help text, set type=int for --id, and route to update command handler

---

## Phase 5: User Story 3 - Toggle Task Completion Status (Priority: P3)

**Goal**: Enable users to mark tasks as complete or incomplete to track progress.

**Independent Test**: Create tasks, toggle their status between complete and incomplete using task IDs, verify status updates correctly in task list.

### Implementation Tasks

- [X] T016 [P] [US3] Implement complete command handler in src/cli/commands.py: Parse --id (required) argument, validate task ID exists, call TaskService.toggle_complete() to set status to True, and output success message with task ID and title
- [X] T017 [P] [US3] Implement incomplete command handler in src/cli/commands.py: Parse --id (required) argument, validate task ID exists, call TaskService.toggle_complete() to set status to False, and output success message with task ID and title
- [X] T018 [US3] Add complete and incomplete subparsers to main.py CLI: Add complete and incomplete commands to argparse subparsers, define --id argument with help text for both commands, set type=int for --id, and route to respective command handlers

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove tasks from their todo list by task ID.

**Independent Test**: Create tasks, delete one or more by ID, verify they no longer appear in task list while other tasks remain.

### Implementation Tasks

- [X] T019 [P] [US4] Implement delete command handler in src/cli/commands.py: Parse --id (required) argument, validate task ID exists, call TaskService.delete_task(), and output success message with deleted task ID and title
- [X] T020 [US4] Add delete subparser to main.py CLI: Add delete command to argparse subparsers, define --id argument with help text, set type=int for --id, and route to delete command handler

---

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Improve CLI usability, error handling, and overall code quality.

- [X] T021 [P] Add global --help support: Ensure main parser provides full help message with all commands, add --help flag to all subcommands for command-specific help, and verify help text is clear and actionable
- [X] T022 [P] Standardize error messages across all command handlers: Ensure all errors follow format "Error: <clear, actionable message>", include specific guidance for common errors (invalid ID, missing fields, file permissions), and use consistent capitalization and punctuation
- [X] T023 [P] Implement graceful file error handling in storage.py: Catch PermissionError and display user-friendly message with path, catch OSError for disk full or other I/O issues, and ensure temp files are cleaned up on errors
- [X] T024 [P] Add exit codes to main.py: Return 0 for success, return 1 for validation errors and task not found errors, return 2 for file I/O errors, and document exit codes in help text
- [X] T025 [P] Validate all input constraints in command handlers: Check title non-empty and max 200 chars in add/update commands, check description max 1000 chars in add/update commands, and provide specific error messages for each validation failure
- [X] T026 [P] Add unicode support testing: Verify task titles and descriptions with emojis work correctly, test special characters (quotes, backslashes, non-ASCII), and ensure JSON serialization handles these cases
- [X] T027 Add docstrings to all public functions and classes: Document purpose in Task model methods, document CLI command handlers with usage examples, document service layer methods with parameters and return values, and follow Google docstring style
- [X] T028 Run PEP 8 compliance check: Check code formatting with pycodestyle or flake8, fix any indentation/line length issues, ensure imports are at top of files, and verify consistent naming conventions
- [X] T029 Create manual test documentation: Document test scenarios from quickstart.md, add edge case testing steps (corrupted file, long titles, special characters), and create tests/ directory with manual_test.txt
- [X] T030 Final integration testing: Test complete workflow (add → list → update → complete → list → delete → list), verify data persists across application restarts, test all error conditions with expected messages, and confirm application startup < 2 seconds and list operations < 1 second

---

## Dependencies Summary

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3+ (User Stories) → Final Phase (Polish)

User Stories can be implemented incrementally:
  Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (US4)

Within each user story phase, [P] tasks can run in parallel.
```

---

## Parallel Execution Examples

### Phase 3 - US1 (Create and View Tasks)
- **Parallel**: T011 (add command handler) and T012 (list command handler) can be done simultaneously (different command handlers)
- **Sequential**: T013 must wait for T011 and T012 to complete (requires both handlers to wire up CLI)

### Phase 2 - Foundational
- **Parallel**: T006 (Task model), T007 (storage service), and T008 (TaskService skeleton) can be done simultaneously (different files)
- **Sequential**: T009 and T010 must wait for T007 and T008 (integration and error handling require completed components)

### Final Phase - Polish
- **Parallel**: T021 (help), T022 (error messages), T023 (file errors), T024 (exit codes) can all be done simultaneously (cross-cutting improvements)
- **Sequential**: T030 (final testing) must wait for all polish tasks to complete

---

## Task Validation Checklist

- ✅ **Format Compliance**: All tasks follow checkbox format `- [ ] [TaskID] [P?] [Story?] Description with file path`
- ✅ **File Paths Included**: Every task specifies the exact file to create or modify
- ✅ **Story Labels Applied**: User story phase tasks have `[US1]`, `[US2]`, `[US3]`, or `[US4]` labels
- ✅ **Parallel Markers Accurate**: Tasks marked `[P]` have no dependencies on incomplete tasks
- ✅ **Specific Actions**: Each task describes a concrete, implementable action
- ✅ **Independent Test Criteria**: Each user story has clear test criteria from spec.md
- ✅ **All Contracts Covered**: All 6 CLI commands (add, list, update, delete, complete, incomplete) have implementation tasks
- ✅ **All Data Model Entities Covered**: Task and TaskList entities have corresponding implementation tasks
- ✅ **Error Handling Included**: Validation, file I/O, and user-not-found error handling tasks included
- ✅ **Polish Tasks Included**: CLI help, exit codes, PEP 8, and final testing tasks included

---

## MVP Scope Recommendation

**Minimum Viable Product**: Complete Phase 1, Phase 2, and Phase 3 (T001-T013)

This delivers:
- Task creation with title and description
- Task listing with ID, title, and status
- Data persistence between sessions
- Basic error handling

**Estimated Tasks**: 13 tasks total

**After MVP**: Implement Phases 4, 5, 6, and Final Phase sequentially to add update, toggle status, delete functionality, and polish.

---

## Total Task Count

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 5 tasks
- **Phase 3 (US1 - Create/View)**: 3 tasks
- **Phase 4 (US2 - Update)**: 2 tasks
- **Phase 5 (US3 - Toggle Status)**: 3 tasks
- **Phase 6 (US4 - Delete)**: 2 tasks
- **Final Phase (Polish)**: 10 tasks

**Grand Total**: 30 tasks

---

## Implementation Notes

1. **Atomic File Writes**: Storage layer must use temp file + os.replace() pattern (documented in research.md RQ-004)
2. **Error Message Format**: All errors must follow "Error: <clear, actionable message>" pattern (from cli-api.md)
3. **Validation Rules**: Title max 200 chars, description max 1000 chars, title required non-empty (from data-model.md)
4. **Exit Codes**: 0=success, 1=validation/not found, 2=I/O errors (from cli-api.md)
5. **PEP 8 Compliance**: Follow Python style guide per constitution NFR-003
6. **No External Dependencies**: Use only standard library (argparse, json, os, pathlib) per plan

---

**Ready for implementation**: Run `/sp.implement` to begin execution or implement tasks manually in order.
