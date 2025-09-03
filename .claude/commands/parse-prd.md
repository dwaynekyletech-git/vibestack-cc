Convert PRD into structured, actionable development tasks.

Usage: /parse-prd

This command will:
- Analyze existing docs/prd.md for all features and requirements
- Break down features into granular development tasks
- Create task dependency mapping
- Assign priority levels and effort estimates
- Generate task IDs for tracking (TASK-001, TASK-002, etc.)
- Create initial task backlog with clear acceptance criteria
- Populate the empty tasks.json structure created by /genesis

Updates:
- tasks/tasks.json - Structured task database with IDs, dependencies, status

Prerequisites: docs/prd.md must exist

Arguments: $ARGUMENTS