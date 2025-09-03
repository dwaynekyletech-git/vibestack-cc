Execute a specific step from the implementation plan.

Usage: /execute-step [task-id] [step-n]
Example: /execute-step TASK-001 3

This command will:
- Load specific step from task implementation plan
- Execute only that step with full context
- Update plan document with step completion status
- Validate step completion before marking complete
- Provide granular control over implementation pace

Output: Single step completion with updated progress

Prerequisites: tasks/plan-{task-id}.md must exist

Arguments: $ARGUMENTS