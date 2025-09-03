# Claude Code Configuration for vibestack-cc

This directory contains the complete Claude Code configuration implementing the comprehensive workflow system described in `claude-code-plan.md`.

## Directory Structure

```
.claude/
├── claude-code.json         # Main configuration file
├── README.md               # This file
├── agents/
│   └── agents.json         # AI agent definitions and configurations
├── commands/
│   └── commands.json       # Slash command definitions and workflows
└── hooks/
    ├── hooks.json          # Hook configuration and settings
    ├── task-quality-gate.py                # Quality enforcement hook
    ├── error-cascade-monitor.py            # Error cascade prevention
    ├── context-drift-detection.py          # Task alignment monitoring
    ├── change-impact-tracker.py            # Scope change tracking
    ├── plan-quality-validator.py           # Plan validation hook
    ├── implementation-progress-tracker.py   # Progress monitoring
    └── plan-drift-monitor.py               # Implementation drift detection
```

## Quick Start

### 1. Initialize a New Project
```bash
/genesis "Your project idea description"
```

### 2. Create Task Breakdown
```bash
/parse-prd
```

### 3. Execute Development Cycle
```bash
/next-task                    # Load next task
/plan-task TASK-001          # Create implementation plan
/execute-plan TASK-001       # Execute the plan
/validate-implementation TASK-001  # Validate quality
/commit-task TASK-001        # Commit changes
```

## AI Agents

### planning-specialist (Opus)
- **Purpose**: Strategic planning and architectural design
- **When**: Before implementing features or significant changes
- **Output**: Detailed implementation plans with step-by-step guidance

### test-specialist (Sonnet)
- **Purpose**: Comprehensive testing strategy and implementation
- **When**: During implementation when test coverage is needed
- **Output**: Test suites with high coverage and edge case handling

### cascading-debugger (Sonnet)
- **Purpose**: Intelligent error resolution with cascade prevention
- **When**: Compilation errors, test failures, or error cascades detected
- **Output**: Working code with comprehensive error resolution

## Quality Hooks

### High Priority (Blocking)
- **task-quality-gate**: Enforces TypeScript/ESLint standards
- **plan-quality-validator**: Validates plan completeness and quality

### Medium Priority (Alerting)
- **context-drift-detection**: Monitors task alignment
- **change-impact-tracker**: Tracks scope change effects
- **plan-drift-monitor**: Detects implementation drift

### Low Priority (Monitoring)
- **implementation-progress-tracker**: Updates progress in plans
- **error-cascade-monitor**: Prevents debugging cascades

## Slash Commands

### Project Flow
- `/genesis [idea]` - Transform idea into structured PRD
- `/parse-prd` - Convert PRD into actionable tasks
- `/next-task` - Load next highest-priority task

### Task Execution
- `/plan-task [id]` - Create detailed implementation plan
- `/review-plan [id]` - Validate plan before execution
- `/execute-plan [id]` - Execute entire plan
- `/execute-step [id] [n]` - Execute specific plan step
- `/validate-implementation [id]` - Comprehensive quality validation
- `/commit-task [id]` - Commit completed task

### Management
- `/break-down [id]` - Split complex tasks into subtasks
- `/task-status [id] [status]` - Update task status
- `/pivot [change]` - Handle scope changes
- `/sync-context` - Reconcile documentation with reality

## Hook Configuration

Hooks are automatically triggered based on:
- **Tool Usage**: Edit, Write, Bash operations
- **Commands**: Specific slash commands
- **File Changes**: Modifications to key project files
- **Agent Invocation**: When specific agents are called
- **Context**: Task status and project state

## Quality Standards

### TypeScript
- Strict mode enabled
- No compilation errors allowed
- Type safety enforced

### ESLint
- Zero errors policy
- Maximum 10 warnings
- Consistent code patterns

### Testing
- 80% minimum coverage threshold
- Unit, integration, and E2E tests
- Automatic test generation when needed

## Workflow Phases

1. **Ideation**: Transform ideas into requirements (`/genesis`)
2. **Task Decomposition**: Break down into actionable tasks (`/parse-prd`)
3. **Task Selection**: Choose next task to work on (`/next-task`)
4. **Planning**: Create detailed implementation plan (`/plan-task`)
5. **Plan Validation**: Review and approve plan (`/review-plan`)
6. **Implementation**: Execute the planned work (`/execute-plan`)
7. **Validation**: Validate implementation quality (`/validate-implementation`)
8. **Completion**: Finalize and commit work (`/commit-task`)

## Error Handling

The system includes comprehensive error handling:
- **Cascade Detection**: Prevents one fix from creating multiple new errors
- **Quality Gates**: Blocks progression when quality standards aren't met
- **Context Monitoring**: Alerts when implementation drifts from plans
- **Impact Tracking**: Analyzes ripple effects of scope changes

## Project Integration

The configuration integrates with:
- **Git**: Automated commit message generation and branch management
- **GitHub**: PR template generation and issue linking
- **NPM/Package Managers**: Automatic dependency and script detection
- **Testing Frameworks**: Jest, Cypress, and other testing tools

## Troubleshooting

### Hook Execution Issues
```bash
# Check hook permissions
chmod +x .claude/hooks/*.py

# Test individual hook
python3 .claude/hooks/task-quality-gate.py

# View hook logs
tail -f .claude/logs/claude-code.log
```

### Agent Issues
- Ensure OpenAI API key is configured
- Check agent model availability (Opus for planning-specialist)
- Verify tool permissions in agent configuration

### Command Issues
- Verify project structure (docs/, tasks/ directories)
- Check required files exist (package.json, tsconfig.json)
- Ensure git repository is initialized

## Customization

### Adding Custom Commands
Edit `.claude/commands/commands.json` to add new slash commands with:
- Command definition and usage
- Behavior specification
- Tool requirements
- Prerequisites and outputs

### Adding Custom Hooks
1. Create Python script in `.claude/hooks/`
2. Add configuration to `.claude/hooks/hooks.json`
3. Set appropriate trigger conditions and priority
4. Make script executable: `chmod +x script.py`

### Modifying Quality Standards
Update `.claude/claude-code.json` quality_standards section:
- TypeScript configuration
- ESLint rules and thresholds
- Testing requirements and coverage

## Best Practices

1. **Always start with `/genesis`** for new projects
2. **Use `/plan-task` before implementation** for complex features
3. **Let hooks guide quality** - don't override quality gates
4. **Monitor drift alerts** and update plans when needed
5. **Use `/sync-context`** regularly in team environments
6. **Document scope changes** with `/pivot` command

## Support

For issues or questions:
1. Check the hook logs in `.claude/logs/`
2. Verify configuration files are valid JSON
3. Ensure all required dependencies are installed
4. Test individual components in isolation

This configuration transforms Claude Code into a comprehensive development workflow system with enterprise-grade quality controls and intelligent AI assistance.