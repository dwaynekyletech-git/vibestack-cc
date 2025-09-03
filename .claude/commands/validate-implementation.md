Comprehensive validation before task completion.

Usage: /validate-implementation [task-id]
Example: /validate-implementation TASK-001

This command will:
- Load task details and implementation plan
- Run complete test suite for the project
- Check TypeScript compilation and code quality (ESLint)
- Validate test coverage meets project standards (80%+)
- Run security vulnerability scans
- Verify implementation meets task acceptance criteria
- Invoke test-specialist agent if coverage gaps are found
- Generate comprehensive validation report

Creates:
- tasks/validation-report-{task-id}.md - Detailed validation results

Updates:
- tasks/tasks.json - Validation status

Quality checks:
- All tests pass
- TypeScript compilation successful
- Code quality standards met
- Test coverage above threshold (80%+)
- No security vulnerabilities
- Acceptance criteria satisfied

Can invoke agents: test-specialist

Arguments: $ARGUMENTS