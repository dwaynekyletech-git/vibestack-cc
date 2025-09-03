Generate detailed implementation plan using planning-specialist agent.

Usage: /plan-task [task-id]
Example: /plan-task TASK-001

This command will:
- Load task details from tasks/tasks.json
- Invoke planning-specialist agent with task context
- Agent conducts codebase exploration and requirements analysis
- Create detailed step-by-step implementation plan
- Identify files to modify, patterns to follow, and potential blockers
- Estimate complexity and time requirements
- Generate comprehensive plan document in tasks folder

Creates:
- tasks/plan-{task-id}.md - Detailed implementation plan

Updates:
- tasks/tasks.json - Plan reference and status

Invokes: planning-specialist agent

Arguments: $ARGUMENTS