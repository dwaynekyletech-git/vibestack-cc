Load the next highest-priority task for planning.

Usage: /next-task

This command will:
- Scan tasks/tasks.json for next available task based on priority and dependencies
- Load task context and requirements from the task database
- Validate all dependencies are completed
- Set task status to 'planning'
- Prepare task for planning-specialist agent handoff
- Update tasks.json with status change

Output: Task details and readiness confirmation for planning phase

Prerequisites: tasks/tasks.json must exist with pending tasks

Arguments: $ARGUMENTS