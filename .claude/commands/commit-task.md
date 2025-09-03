Commit completed task with comprehensive commit message.

Usage: /commit-task [task-id]
Example: /commit-task TASK-001

This command will:
- Require successful /validate-implementation before proceeding
- Validate all plan steps are completed
- Run final tests and quality checks
- Generate commit message referencing task ID and plan
- Create git commit with all changes
- Update tasks.json to mark task as completed
- Prepare for next task in sequence

Output: Git commit with task completion and status updates

Prerequisites: Successful /validate-implementation required

Arguments: $ARGUMENTS