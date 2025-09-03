Handle scope changes and requirement updates.

Usage: /pivot [change]
Example: /pivot "Add user authentication to all endpoints"

This command will:
- Analyze impact of requested change on existing tasks and plans
- Update docs/prd.md with new requirements
- Modify affected tasks in tasks/tasks.json and create new ones as needed
- Update implementation plans to accommodate changes
- Identify cascade effects on completed work
- Create change log for project tracking

Updates:
- docs/prd.md - Updated requirements
- tasks/tasks.json - Modified and new tasks
- tasks/plan-*.md - Updated plans

Creates:
- docs/change-log.md - History of all pivots and their impacts

Arguments: $ARGUMENTS