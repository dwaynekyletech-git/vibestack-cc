Split complex tasks into smaller, manageable subtasks.

Usage: /break-down [task-id]
Example: /break-down TASK-001

This command will:
- Load task from tasks/tasks.json and analyze complexity and scope
- Identify natural breakpoints and dependencies
- Create subtasks with clear boundaries (TASK-001a, TASK-001b, etc.)
- Update task hierarchy in tasks/tasks.json
- Maintain parent-child relationships
- Preserve original acceptance criteria across subtasks

Updates:
- tasks/tasks.json - New subtask structure

Arguments: $ARGUMENTS