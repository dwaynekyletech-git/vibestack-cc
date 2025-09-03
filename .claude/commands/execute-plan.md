Execute entire implementation plan step-by-step.

Usage: /execute-plan [task-id]
Example: /execute-plan TASK-001

This command will:
- Load task plan and execute each step sequentially
- Update plan document with progress as each step completes
- Run tests and validation after each major step
- Handle errors by invoking cascading-debugger if needed
- Maintain implementation history and progress tracking
- Continue until all plan steps are completed

Output: Completed implementation with updated plan progress

Can invoke agents: cascading-debugger, test-specialist

Prerequisites: tasks/plan-{task-id}.md must exist

Arguments: $ARGUMENTS