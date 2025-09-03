Manually update task status for tracking and workflow management.

Usage: /task-status [id] [status]
Example: /task-status TASK-001 completed

Valid statuses: pending, planning, in-progress, blocked, completed, cancelled

This command will:
- Update specified task status in tasks/tasks.json
- Validate status transition is valid
- Update dependent tasks if needed
- Maintain task history and audit trail
- Trigger any status-dependent actions

Arguments: $ARGUMENTS