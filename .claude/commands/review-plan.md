Review and validate implementation plan before execution.

Usage: /review-plan [task-id]
Example: /review-plan TASK-001

This command will:
- Load and analyze the task's implementation plan
- Validate plan completeness and feasibility
- Check for missing dependencies or edge cases
- Suggest improvements or identify risks
- Confirm plan is ready for execution
- Allow plan refinement before implementation
- Update tasks/tasks.json with review status

Output: Plan validation report and approval status

Prerequisites: tasks/plan-{task-id}.md must exist

Arguments: $ARGUMENTS