AGENTS

## planning-specialist
**Purpose:** Strategic planning and architectural design for development tasks
**Model:** Opus (for superior reasoning and planning capabilities)

**When to Use:**
- Before implementing any feature or significant code change
- When breaking down complex requirements into actionable steps
- When you need to understand codebase architecture and dependencies
- For creating detailed implementation roadmaps
- When evaluating multiple implementation approaches
- Before refactoring or architectural changes

**What This Agent Does:**
- Conducts thorough codebase exploration to understand existing patterns
- Gathers context through targeted questions about requirements and constraints
- Analyzes dependencies and potential integration points
- Creates detailed, step-by-step implementation plans
- Identifies edge cases and potential blockers before implementation
- Designs architecture that follows project conventions
- Evaluates performance, security, and maintainability implications
- Creates structured plan documents for execution tracking

**Tools Access:** Read, Grep, Glob, Bash (for analysis), TodoWrite (for plan tracking)
**Output:** Structured implementation plan document with clear steps and rationale

---

## test-specialist
**Purpose:** Comprehensive testing strategy and test implementation
**Model:** Sonnet (optimized for test generation and coverage analysis)

**When to Use:**
- During task implementation when test coverage is needed
- After implementing new features that require validation
- When existing tests are insufficient or outdated
- For complex business logic that needs edge case testing
- Before task completion to ensure adequate test coverage
- When refactoring code that lacks proper test coverage

**What This Agent Does:**
- Analyzes code to identify testable units and edge cases
- Generates unit tests for functions, classes, and components
- Creates integration tests for API endpoints and workflows
- Writes end-to-end tests for critical user journeys
- Evaluates existing test coverage and identifies gaps
- Suggests testing strategies and framework improvements
- Ensures tests follow project conventions and best practices
- Validates that tests properly cover acceptance criteria

**Tools Access:** Read, Write, Edit, Bash (test runners), mcp__ide__executeCode, Grep, Glob
**Output:** Comprehensive test suites with high coverage and edge case handling

---

## cascading-debugger
**Purpose:** Intelligent error resolution with cascade detection and prevention
**Model:** Sonnet (optimized for debugging workflows)

**When to Use:**
- When encountering compilation errors, runtime errors, or test failures
- After implementing changes that break existing functionality
- When fixes create new errors or reveal hidden issues
- For systematic debugging of complex, interconnected systems
- When error messages are unclear or misleading
- For preventing error cascades during large refactoring efforts

**What This Agent Does:**
- Analyzes error messages and stack traces systematically
- Maps error relationships and identifies root causes
- Detects when fixing one error reveals or creates others
- Implements fixes while monitoring for cascade effects
- Validates fixes don't introduce regressions
- Documents error patterns for future prevention
- Suggests architectural improvements to prevent similar issues
- Maintains system stability during debugging sessions

**Tools Access:** Read, Edit, MultiEdit, Bash, Grep, Glob, mcp__ide__getDiagnostics
**Output:** Working code with comprehensive error resolution and cascade prevention

SLASH COMMANDS

## Project Flow Commands

### /genesis [idea]
**Purpose:** Transform a raw idea into a structured PRD and initialize project setup
**Usage:** `/genesis "Build a task management app with AI recommendations"`

**Command Behavior:**
- Conducts thorough requirements gathering through targeted questions
- Analyzes similar products and best practices
- Creates comprehensive PRD with features, user stories, and technical requirements
- Sets up initial project structure and documentation
- Identifies key technical decisions and constraints
- Creates project roadmap with major milestones
- Initializes task management folder structure

**Folder Structure Created:**
```
project-root/
├── docs/
│   └── prd.md                       # Product Requirements Document
└── tasks/
    └── tasks.json                   # Task database (initially empty, populated by /parse-prd)
```

**Output Files:**
- `docs/prd.md` - Complete product requirements document with features, user stories, technical requirements
- `tasks/tasks.json` - Empty task database structure ready for /parse-prd population

---

### /parse-prd
**Purpose:** Convert PRD into structured, actionable development tasks
**Usage:** `/parse-prd`

**Command Behavior:**
- Analyzes existing `docs/prd.md` for all features and requirements
- Breaks down features into granular development tasks
- Creates task dependency mapping
- Assigns priority levels and effort estimates
- Generates task IDs for tracking (TASK-001, TASK-002, etc.)
- Creates initial task backlog with clear acceptance criteria
- Populates the empty tasks.json structure created by /genesis

**Output Files:**
- `tasks/tasks.json` - Structured task database with IDs, dependencies, status, and individual task details

---

### /next-task
**Purpose:** Load the next highest-priority task for planning
**Usage:** `/next-task`

**Command Behavior:**
- Scans `tasks/tasks.json` for next available task based on priority and dependencies
- Loads task context and requirements from the task database
- Validates all dependencies are completed
- Sets task status to "planning" 
- Prepares task for planning-specialist agent handoff
- Updates tasks.json with status change

**Output:** Task details and readiness confirmation for planning phase

---

## Task Execution Flow Commands

### /plan-task [task-id]
**Purpose:** Generate detailed implementation plan using planning-specialist agent
**Usage:** `/plan-task TASK-001`

**Command Behavior:**
- Loads task details from `tasks/tasks.json`
- Invokes planning-specialist agent with task context
- Agent conducts codebase exploration and requirements analysis
- Creates detailed step-by-step implementation plan
- Identifies files to modify, patterns to follow, and potential blockers
- Estimates complexity and time requirements
- Generates comprehensive plan document in tasks folder

**Output Files:**
- `tasks/plan-task-001.md` - Detailed implementation plan (follows naming: plan-{task-id}.md)
- Updates `tasks/tasks.json` with plan reference and status

---

### /review-plan [task-id]
**Purpose:** Review and validate implementation plan before execution
**Usage:** `/review-plan TASK-001`

**Command Behavior:**
- Loads and analyzes the task's implementation plan from `tasks/plan-task-001.md`
- Validates plan completeness and feasibility
- Checks for missing dependencies or edge cases
- Suggests improvements or identifies risks
- Confirms plan is ready for execution
- Allows plan refinement before implementation
- Updates `tasks/tasks.json` with review status

**Output:** Plan validation report and approval status

---

### /execute-plan [task-id]
**Purpose:** Execute entire implementation plan step-by-step
**Usage:** `/execute-plan TASK-001`

**Command Behavior:**
- Loads task plan and executes each step sequentially
- Updates plan document with progress as each step completes
- Runs tests and validation after each major step
- Handles errors by invoking cascading-debugger if needed
- Maintains implementation history and progress tracking
- Continues until all plan steps are completed

**Output:** Completed implementation with updated plan progress

---

### /execute-step [task-id] [step-n]
**Purpose:** Execute a specific step from the implementation plan
**Usage:** `/execute-step TASK-001 3`

**Command Behavior:**
- Loads specific step from task implementation plan
- Executes only that step with full context
- Updates plan document with step completion status
- Validates step completion before marking complete
- Provides granular control over implementation pace

**Output:** Single step completion with updated progress

---

### /validate-implementation [task-id]
**Purpose:** Comprehensive validation before task completion
**Usage:** `/validate-implementation TASK-001`

**Command Behavior:**
- Loads task details and implementation plan from `tasks/tasks.json` and `tasks/plan-task-001.md`
- Runs complete test suite for the project
- Checks TypeScript compilation and code quality (ESLint)
- Validates test coverage meets project standards
- Runs security vulnerability scans
- Verifies implementation meets task acceptance criteria
- Invokes test-specialist agent if coverage gaps are found
- Generates comprehensive validation report

**Output Files:**
- `tasks/validation-report-task-001.md` - Detailed validation results
- Updates `tasks/tasks.json` with validation status

**Validation Checks:**
- ✅ All tests pass
- ✅ TypeScript compilation successful
- ✅ Code quality standards met
- ✅ Test coverage above threshold (80%+)
- ✅ No security vulnerabilities
- ✅ Acceptance criteria satisfied

---

### /commit-task [task-id]
**Purpose:** Commit completed task with comprehensive commit message
**Usage:** `/commit-task TASK-001`

**Command Behavior:**
- Requires successful /validate-implementation before proceeding
- Validates all plan steps are completed
- Runs final tests and quality checks
- Generates commit message referencing task ID and plan
- Creates git commit with all changes
- Updates TASKS.json to mark task as completed
- Prepares for next task in sequence

**Output:** Git commit with task completion and status updates

---

## Management Commands

### /break-down [task-id]
**Purpose:** Split complex tasks into smaller, manageable subtasks
**Usage:** `/break-down TASK-001`

**Command Behavior:**
- Loads task from `tasks/tasks.json` and analyzes complexity and scope
- Identifies natural breakpoints and dependencies
- Creates subtasks with clear boundaries (TASK-001a, TASK-001b, etc.)
- Updates task hierarchy in `tasks/tasks.json`
- Maintains parent-child relationships
- Preserves original acceptance criteria across subtasks

**Output:** Updated `tasks/tasks.json` with new subtask structure

---

### /task-status [id] [status]
**Purpose:** Manually update task status for tracking and workflow management
**Usage:** `/task-status TASK-001 completed`

**Command Behavior:**
- Updates specified task status in `tasks/tasks.json`
- Validates status transition is valid
- Updates dependent tasks if needed
- Maintains task history and audit trail
- Triggers any status-dependent actions

**Valid Statuses:** pending, planning, in-progress, blocked, completed, cancelled

---

### /pivot [change]
**Purpose:** Handle scope changes and requirement updates
**Usage:** `/pivot "Add user authentication to all endpoints"`

**Command Behavior:**
- Analyzes impact of requested change on existing tasks and plans
- Updates `docs/prd.md` with new requirements
- Modifies affected tasks in `tasks/tasks.json` and creates new ones as needed
- Updates implementation plans in `tasks/plan-*.md` files to accommodate changes
- Identifies cascade effects on completed work
- Creates change log for project tracking

**Output Files:**
- Updated `docs/prd.md` and `tasks/tasks.json`
- Updated relevant `tasks/plan-*.md` files
- `docs/change-log.md` - History of all pivots and their impacts

---

### /sync-context
**Purpose:** Reconcile project context when implementation drifts from plans
**Usage:** `/sync-context`

**Command Behavior:**
- Compares current codebase state with project documentation
- Identifies discrepancies between plans and implementation
- Updates `docs/prd.md` and `tasks/tasks.json` with current reality
- Reconciles task status with actual completion state
- Updates relevant `tasks/plan-*.md` files to reflect implementation changes
- Maintains project coherence and accuracy

**Output:** Updated project documentation and alignment recommendations

HOOKS

## 1. task-quality-gate.py
**Purpose:** Enforce code quality standards before task progression
**Trigger:** PostToolUse (after any code modification during task execution)
**Priority:** HIGH - Blocks execution on failure

**Hook Logic:**
```python
import subprocess
import json
import os
from pathlib import Path

def main():
    # Check if we're in a task execution context
    if not os.path.exists("tasks/tasks.json"):
        return {"action": "continue"}
    
    quality_checks = []
    
    # TypeScript compilation check
    try:
        result = subprocess.run(["npx", "tsc", "--noEmit"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            quality_checks.append(f"TypeScript errors: {result.stderr}")
    except Exception as e:
        quality_checks.append(f"TypeScript check failed: {str(e)}")
    
    # ESLint code quality validation
    try:
        result = subprocess.run(["npx", "eslint", ".", "--format", "json"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            errors = json.loads(result.stdout)
            error_count = sum(len(file["messages"]) for file in errors)
            if error_count > 0:
                quality_checks.append(f"ESLint violations: {error_count} issues found")
    except Exception as e:
        quality_checks.append(f"ESLint check failed: {str(e)}")
    
    # Pattern consistency verification
    # Check for common anti-patterns, inconsistent naming, etc.
    
    if quality_checks:
        return {
            "action": "block",
            "message": f"Quality gate failed:\n" + "\n".join(quality_checks) + 
                      "\n\nPlease fix these issues before proceeding."
        }
    
    return {"action": "continue"}
```

---

## 2. error-cascade-monitor.py
**Purpose:** Detect and prevent error cascades during debugging
**Trigger:** PostToolUse (after cascading-debugger agent execution)
**Priority:** HIGH - Critical for system stability

**Hook Logic:**
```python
import subprocess
import json
import time
from pathlib import Path

def main():
    # Only run after cascading-debugger actions
    if not is_debugger_context():
        return {"action": "continue"}
    
    # Wait briefly for compilation
    time.sleep(2)
    
    # Scan for new errors
    new_errors = scan_for_errors()
    
    if new_errors:
        error_analysis = analyze_error_cascade(new_errors)
        
        if error_analysis["is_cascade"]:
            return {
                "action": "alert",
                "message": f"Error cascade detected!\n"
                          f"New errors: {len(new_errors)}\n"
                          f"Cascade risk: {error_analysis['risk_level']}\n"
                          f"Recommendation: {error_analysis['recommendation']}"
            }
    
    return {"action": "continue"}

def scan_for_errors():
    errors = []
    
    # TypeScript errors
    try:
        result = subprocess.run(["npx", "tsc", "--noEmit"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            errors.extend(parse_typescript_errors(result.stderr))
    except Exception:
        pass
    
    # Runtime errors from test runs
    try:
        result = subprocess.run(["npm", "test", "--silent"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            errors.extend(parse_test_errors(result.stderr))
    except Exception:
        pass
    
    return errors

def analyze_error_cascade(errors):
    # Analyze if errors are related/cascading
    cascade_indicators = [
        "Cannot find module",
        "Property does not exist",
        "Type error",
        "Import error"
    ]
    
    cascade_count = sum(1 for error in errors 
                       if any(indicator in error for indicator in cascade_indicators))
    
    risk_level = "HIGH" if cascade_count > 3 else "MEDIUM" if cascade_count > 1 else "LOW"
    
    return {
        "is_cascade": cascade_count > 1,
        "risk_level": risk_level,
        "recommendation": "Run cascading-debugger again" if risk_level == "HIGH" 
                        else "Monitor next changes carefully"
    }
```

---

## 3. context-drift-detection.py
**Purpose:** Monitor alignment between implementation and original task intent
**Trigger:** PostToolUse (after significant code changes - Edit, MultiEdit, Write)
**Priority:** MEDIUM - Preventive monitoring

**Hook Logic:**
```python
import json
import os
from pathlib import Path
import subprocess

def main():
    # Check if we have task context
    if not os.path.exists("tasks/tasks.json"):
        return {"action": "continue"}
    
    # Load current task context
    current_task = get_current_task()
    if not current_task:
        return {"action": "continue"}
    
    # Analyze recent changes vs task intent
    drift_analysis = analyze_context_drift(current_task)
    
    if drift_analysis["drift_detected"]:
        return {
            "action": "alert",
            "message": f"Context drift detected!\n"
                      f"Task: {current_task['id']} - {current_task['title']}\n"
                      f"Drift severity: {drift_analysis['severity']}\n"
                      f"Issues found: {drift_analysis['issues']}\n"
                      f"Recommendation: {drift_analysis['recommendation']}"
        }
    
    return {"action": "continue"}

def get_current_task():
    try:
        with open("tasks/tasks.json", "r") as f:
            tasks_data = json.load(f)
            
        # Find task with status "in-progress"
        for task in tasks_data.get("tasks", []):
            if task.get("status") == "in-progress":
                return task
                
        return None
    except Exception:
        return None

def analyze_context_drift(task):
    # Get recent git changes
    try:
        result = subprocess.run(["git", "diff", "--name-only", "HEAD~1"], 
                              capture_output=True, text=True)
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        changed_files = []
    
    # Load task plan if exists
    plan_file = f"tasks/plan-{task['id'].lower()}.md"
    planned_files = []
    
    if os.path.exists(plan_file):
        with open(plan_file, "r") as f:
            plan_content = f.read()
            # Extract file mentions from plan (simple pattern matching)
            import re
            planned_files = re.findall(r'`([^`]*\.[a-zA-Z]{2,4})`', plan_content)
    
    # Detect drift
    issues = []
    
    # Files changed that weren't in plan
    unexpected_changes = [f for f in changed_files if f not in planned_files and f]
    if unexpected_changes:
        issues.append(f"Unexpected file changes: {', '.join(unexpected_changes)}")
    
    # Task acceptance criteria check (simplified)
    if len(changed_files) > 10:
        issues.append("Large number of files changed - may indicate scope creep")
    
    severity = "HIGH" if len(issues) > 2 else "MEDIUM" if issues else "LOW"
    
    return {
        "drift_detected": len(issues) > 0,
        "severity": severity,
        "issues": ", ".join(issues),
        "recommendation": "Review task scope and update plan" if severity == "HIGH" 
                         else "Monitor next changes"
    }
```

---

## 4. change-impact-tracker.py
**Purpose:** Track ripple effects of scope changes and pivots
**Trigger:** PostToolUse (after /pivot command execution)
**Priority:** MEDIUM - Impact analysis

**Hook Logic:**
```python
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def main():
    # Only run after pivot commands
    if not is_pivot_context():
        return {"action": "continue"}
    
    # Analyze change impact
    impact_analysis = analyze_change_impact()
    
    # Log impact for tracking
    log_change_impact(impact_analysis)
    
    if impact_analysis["high_impact"]:
        return {
            "action": "alert",
            "message": f"High impact change detected!\n"
                      f"Affected systems: {', '.join(impact_analysis['affected_systems'])}\n"
                      f"Tasks requiring updates: {len(impact_analysis['affected_tasks'])}\n"
                      f"Recommendation: {impact_analysis['recommendation']}"
        }
    
    return {"action": "continue"}

def analyze_change_impact():
    # Get recent changes
    try:
        result = subprocess.run(["git", "diff", "--name-only", "HEAD~1"], 
                              capture_output=True, text=True)
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        changed_files = []
    
    # Analyze affected systems
    affected_systems = []
    
    # Check for core system changes
    if any("auth" in f.lower() for f in changed_files):
        affected_systems.append("Authentication")
    if any("api" in f.lower() for f in changed_files):
        affected_systems.append("API Layer")
    if any("database" in f.lower() or "db" in f.lower() for f in changed_files):
        affected_systems.append("Database")
    if any("component" in f.lower() for f in changed_files):
        affected_systems.append("UI Components")
    
    # Check task impacts
    affected_tasks = check_task_impacts(changed_files)
    
    high_impact = len(affected_systems) > 2 or len(affected_tasks) > 5
    
    return {
        "high_impact": high_impact,
        "affected_systems": affected_systems,
        "affected_tasks": affected_tasks,
        "changed_files": changed_files,
        "recommendation": "Update all affected task plans" if high_impact 
                         else "Monitor affected tasks"
    }

def check_task_impacts(changed_files):
    # Load tasks and check which ones might be affected
    try:
        with open("tasks/tasks.json", "r") as f:
            tasks_data = json.load(f)
        
        affected_tasks = []
        
        for task in tasks_data.get("tasks", []):
            # Simple check - if task mentions any changed files
            task_str = str(task).lower()
            if any(os.path.basename(f).lower() in task_str for f in changed_files):
                affected_tasks.append(task["id"])
        
        return affected_tasks
    except Exception:
        return []

def log_change_impact(impact_analysis):
    # Log to change log file
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "impact_analysis": impact_analysis
    }
    
    try:
        log_file = "docs/change-impact-log.json"
        
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_data = json.load(f)
        else:
            log_data = {"impacts": []}
        
        log_data["impacts"].append(log_entry)
        
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)
    except Exception:
        pass  # Fail silently if logging fails
```

---

## 5. plan-quality-validator.py
**Purpose:** Validate implementation plans before execution begins
**Trigger:** PostToolUse (after /plan-task command completion)
**Priority:** HIGH - Quality assurance

**Hook Logic:**
```python
import os
import json
import re
from pathlib import Path

def main():
    # Only run after plan-task completion
    if not is_plan_task_context():
        return {"action": "continue"}
    
    # Find the most recently created plan
    latest_plan = find_latest_plan()
    if not latest_plan:
        return {"action": "continue"}
    
    # Validate plan quality
    validation_result = validate_plan_quality(latest_plan)
    
    if validation_result["has_issues"]:
        return {
            "action": "alert",
            "message": f"Plan quality issues detected!\n"
                      f"Plan: {latest_plan}\n"
                      f"Issues found: {len(validation_result['issues'])}\n"
                      f"Critical issues: {validation_result['critical_count']}\n"
                      f"Recommendations:\n" + "\n".join(validation_result['recommendations'])
        }
    
    return {"action": "continue"}

def find_latest_plan():
    tasks_dir = Path("tasks")
    if not tasks_dir.exists():
        return None
    
    plan_files = list(tasks_dir.glob("plan-*.md"))
    if not plan_files:
        return None
    
    # Return most recently modified
    return max(plan_files, key=lambda f: f.stat().st_mtime)

def validate_plan_quality(plan_file):
    try:
        with open(plan_file, "r") as f:
            plan_content = f.read()
    except Exception:
        return {"has_issues": False, "issues": [], "critical_count": 0, "recommendations": []}
    
    issues = []
    recommendations = []
    
    # Check for required sections
    required_sections = ["## Context", "## Steps", "## Acceptance Criteria"]
    missing_sections = [section for section in required_sections 
                       if section not in plan_content]
    
    if missing_sections:
        issues.append(f"Missing required sections: {', '.join(missing_sections)}")
        recommendations.append("Add missing sections to provide complete plan structure")
    
    # Check for step numbering/structure
    steps = re.findall(r'^\d+\.\s', plan_content, re.MULTILINE)
    if len(steps) < 3:
        issues.append("Plan has too few implementation steps (minimum 3 recommended)")
        recommendations.append("Break down implementation into more detailed steps")
    
    # Check for file mentions (should specify what files to modify)
    file_mentions = re.findall(r'`([^`]*\.[a-zA-Z]{2,4})`', plan_content)
    if len(file_mentions) < 1:
        issues.append("Plan doesn't specify which files to modify")
        recommendations.append("Add specific file paths that will be modified")
    
    # Check for edge case considerations
    edge_case_keywords = ["edge case", "error handling", "validation", "fallback"]
    if not any(keyword in plan_content.lower() for keyword in edge_case_keywords):
        issues.append("Plan may not consider edge cases or error handling")
        recommendations.append("Add consideration for edge cases and error scenarios")
    
    # Check for testing mentions
    test_keywords = ["test", "spec", "jest", "cypress", "validate"]
    if not any(keyword in plan_content.lower() for keyword in test_keywords):
        issues.append("Plan doesn't mention testing strategy")
        recommendations.append("Add testing approach to validate implementation")
    
    critical_count = len([issue for issue in issues 
                         if any(critical in issue.lower() 
                               for critical in ["missing", "doesn't specify", "too few"])])
    
    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "critical_count": critical_count,
        "recommendations": recommendations
    }
```

---

## 6. implementation-progress-tracker.py
**Purpose:** Track implementation progress and update plan documents
**Trigger:** PostToolUse (after /execute-step command execution)
**Priority:** LOW - Progress monitoring

**Hook Logic:**
```python
import json
import os
import re
from datetime import datetime
from pathlib import Path

def main():
    # Only run after execute-step commands
    if not is_execute_step_context():
        return {"action": "continue"}
    
    # Find current task and update progress
    progress_update = track_implementation_progress()
    
    if progress_update["should_alert"]:
        return {
            "action": "alert",
            "message": f"Progress Update:\n"
                      f"Task: {progress_update['task_id']}\n"
                      f"Step completed: {progress_update['completed_step']}\n"
                      f"Overall progress: {progress_update['progress_percentage']}%\n"
                      f"Time taken: {progress_update['time_estimate']}\n"
                      f"Status: {progress_update['status']}"
        }
    
    return {"action": "continue"}

def track_implementation_progress():
    # Get current task
    current_task = get_current_task()
    if not current_task:
        return {"should_alert": False}
    
    task_id = current_task["id"]
    plan_file = f"tasks/plan-{task_id.lower()}.md"
    
    if not os.path.exists(plan_file):
        return {"should_alert": False}
    
    # Update plan with progress
    progress_info = update_plan_progress(plan_file, task_id)
    
    # Log progress
    log_progress(task_id, progress_info)
    
    return {
        "should_alert": progress_info["progress_percentage"] % 25 == 0,  # Alert every 25%
        "task_id": task_id,
        "completed_step": progress_info["last_completed_step"],
        "progress_percentage": progress_info["progress_percentage"],
        "time_estimate": progress_info["time_estimate"],
        "status": progress_info["status"]
    }

def update_plan_progress(plan_file, task_id):
    try:
        with open(plan_file, "r") as f:
            content = f.read()
        
        # Count total steps and completed steps
        total_steps = len(re.findall(r'^\d+\.\s', content, re.MULTILINE))
        completed_steps = len(re.findall(r'^\d+\.\s.*✓', content, re.MULTILINE))
        
        progress_percentage = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0
        
        # Add progress section if not exists
        progress_section = f"\n## Progress Tracking\n- Steps completed: {completed_steps}/{total_steps}\n- Progress: {progress_percentage}%\n- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        
        if "## Progress Tracking" not in content:
            content += progress_section
        else:
            # Update existing progress section
            content = re.sub(r'## Progress Tracking.*?(?=\n##|\Z)', 
                           progress_section, content, flags=re.DOTALL)
        
        with open(plan_file, "w") as f:
            f.write(content)
        
        return {
            "progress_percentage": progress_percentage,
            "last_completed_step": completed_steps,
            "total_steps": total_steps,
            "time_estimate": "On track",
            "status": "In Progress" if progress_percentage < 100 else "Completed"
        }
        
    except Exception:
        return {
            "progress_percentage": 0,
            "last_completed_step": 0,
            "total_steps": 0,
            "time_estimate": "Unknown",
            "status": "Unknown"
        }

def log_progress(task_id, progress_info):
    try:
        log_file = "tasks/progress-log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "progress": progress_info
        }
        
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_data = json.load(f)
        else:
            log_data = {"progress_entries": []}
        
        log_data["progress_entries"].append(log_entry)
        
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)
    except Exception:
        pass  # Fail silently
```

---

## 7. plan-drift-monitor.py
**Purpose:** Monitor deviation between implementation and plan during execution
**Trigger:** PostToolUse (during plan execution when code changes don't match plan)
**Priority:** MEDIUM - Alignment monitoring

**Hook Logic:**
```python
import json
import os
import subprocess
import re
from pathlib import Path

def main():
    # Only run during active plan execution
    if not is_plan_execution_context():
        return {"action": "continue"}
    
    # Analyze plan vs implementation drift
    drift_analysis = analyze_plan_drift()
    
    if drift_analysis["drift_detected"]:
        return {
            "action": "alert",
            "message": f"Plan drift detected!\n"
                      f"Task: {drift_analysis['task_id']}\n"
                      f"Drift type: {drift_analysis['drift_type']}\n"
                      f"Severity: {drift_analysis['severity']}\n"
                      f"Details: {drift_analysis['details']}\n"
                      f"Recommendation: {drift_analysis['recommendation']}"
        }
    
    return {"action": "continue"}

def analyze_plan_drift():
    # Get current task
    current_task = get_current_task()
    if not current_task:
        return {"drift_detected": False}
    
    task_id = current_task["id"]
    plan_file = f"tasks/plan-{task_id.lower()}.md"
    
    if not os.path.exists(plan_file):
        return {"drift_detected": False}
    
    # Load plan content
    try:
        with open(plan_file, "r") as f:
            plan_content = f.read()
    except Exception:
        return {"drift_detected": False}
    
    # Get recent changes
    try:
        result = subprocess.run(["git", "diff", "--name-only", "HEAD~1"], 
                              capture_output=True, text=True)
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        changed_files = []
    
    # Analyze drift
    drift_issues = []
    
    # Check if changed files are mentioned in plan
    plan_files = re.findall(r'`([^`]*\.[a-zA-Z]{2,4})`', plan_content)
    unexpected_files = [f for f in changed_files if f not in plan_files and f]
    
    if unexpected_files:
        drift_issues.append(f"Modified files not in plan: {', '.join(unexpected_files)}")
    
    # Check for scope expansion (simple heuristic)
    if len(changed_files) > len(plan_files) * 1.5:
        drift_issues.append("Implementation scope appears larger than planned")
    
    # Check git commit messages for drift indicators
    try:
        result = subprocess.run(["git", "log", "--oneline", "-5"], 
                              capture_output=True, text=True)
        recent_commits = result.stdout.lower()
        
        drift_keywords = ["refactor", "fix", "debug", "change approach", "different"]
        if any(keyword in recent_commits for keyword in drift_keywords):
            drift_issues.append("Recent commits suggest approach changes")
    except Exception:
        pass
    
    if not drift_issues:
        return {"drift_detected": False}
    
    severity = "HIGH" if len(drift_issues) > 2 else "MEDIUM"
    drift_type = "Scope Expansion" if "scope" in str(drift_issues) else "Approach Change"
    
    return {
        "drift_detected": True,
        "task_id": task_id,
        "drift_type": drift_type,
        "severity": severity,
        "details": "; ".join(drift_issues),
        "recommendation": "Update plan to reflect actual implementation" if severity == "HIGH"
                         else "Monitor next changes closely"
    }
```

**Hook Installation Instructions:**
1. Save each hook as a `.py` file in `.claude/hooks/`
2. Ensure hooks have executable permissions: `chmod +x .claude/hooks/*.py`
3. Install required dependencies: `pip install subprocess pathlib`
4. Test hooks individually before enabling in Claude Code

---

# COMPLETE USER WORKFLOW

## Overview: Idea to Implementation Pipeline

This system transforms raw ideas into production-ready code through a structured, AI-assisted workflow that mirrors enterprise development practices. Here's when, why, and how to use each component:

---

## PHASE 1: IDEATION & SETUP

### **When:** You have a new project idea or major feature concept
### **Goal:** Transform idea into structured requirements and project foundation

**🚀 START HERE:**
```bash
/genesis "Build a task management app with AI recommendations"
```

**What Happens:**
- Claude conducts requirements gathering through targeted questions
- Creates comprehensive PRD in `docs/prd.md`
- Sets up project folder structure (`docs/`, `tasks/`)
- Initializes empty task database

**Why This Matters:** Prevents scope creep and ensures clear requirements before any coding begins.

**⏱️ Time:** 10-20 minutes of interactive Q&A
**📁 Creates:** `docs/prd.md`, `tasks/tasks.json`

---

## PHASE 2: TASK DECOMPOSITION

### **When:** You have a completed PRD and need actionable development tasks
### **Goal:** Break down PRD into trackable, implementable tasks

**📋 DECOMPOSE:**
```bash
/parse-prd
```

**What Happens:**
- Analyzes your PRD for all features and requirements
- Creates granular development tasks with IDs (TASK-001, TASK-002, etc.)
- Establishes task dependencies and priorities
- Populates `tasks/tasks.json` with structured task database

**Why This Matters:** Large projects become manageable when broken into specific, trackable tasks.

**⏱️ Time:** 5-10 minutes
**📁 Updates:** `tasks/tasks.json` with complete task breakdown

---

## PHASE 3: TASK PLANNING & EXECUTION CYCLE

*This is your core development loop - repeat for each task:*

### Step 3A: Load Next Task
```bash
/next-task
```
- **When:** Ready to start working on the next highest-priority task
- **What:** Loads task context, validates dependencies, sets status to "planning"
- **Why:** Ensures you're always working on the right thing at the right time

### Step 3B: Create Implementation Plan
```bash
/plan-task TASK-001
```
- **When:** You have a loaded task but need detailed implementation approach
- **What:** Invokes **planning-specialist agent** (Opus-powered) to create comprehensive plan
- **Agent Does:**
  - Explores codebase to understand existing patterns
  - Asks targeted questions about implementation preferences
  - Creates detailed step-by-step plan in `tasks/plan-task-001.md`
  - Identifies files to modify, edge cases, and potential blockers

**🧠 Why Use planning-specialist:** Complex implementations benefit from strategic thinking before tactical execution.

### Step 3C: Review & Validate Plan (Optional)
```bash
/review-plan TASK-001
```
- **When:** Want to validate plan quality before implementation
- **What:** Reviews plan completeness, identifies risks, suggests improvements
- **Hook Trigger:** `plan-quality-validator.py` runs automatically after planning

### Step 3D: Execute Implementation

**Option 1 - Full Execution:**
```bash
/execute-plan TASK-001
```
- **When:** Ready to implement entire plan at once
- **What:** Executes all plan steps sequentially with progress tracking

**Option 2 - Step-by-Step Control:**
```bash
/execute-step TASK-001 1
/execute-step TASK-001 2
# ... continue as needed
```
- **When:** Want granular control or debugging complex implementations
- **What:** Executes individual plan steps with validation between each

**🤖 During Execution:** 
- **test-specialist agent** may be invoked automatically when test coverage is needed
- Multiple hooks monitor progress and quality continuously

### Step 3E: Validate Implementation
```bash
/validate-implementation TASK-001
```
- **When:** Implementation appears complete
- **What:** Comprehensive pre-commit validation:
  - Runs all tests (unit, integration, e2e)
  - Checks TypeScript compilation and ESLint
  - Validates test coverage (80%+ threshold)
  - Runs security vulnerability scans
  - Verifies acceptance criteria are met
  - Creates validation report in `tasks/validation-report-task-001.md`

**🔒 Quality Gate:** If validation fails, fix issues before proceeding.

### Step 3F: Commit Completed Task
```bash
/commit-task TASK-001
```
- **When:** Validation passes and implementation is complete
- **What:** Creates git commit with comprehensive message, updates task status
- **Requires:** Successful `/validate-implementation` first

---

## PHASE 4: CONTINUOUS MANAGEMENT

### **Handling Complex Tasks**
```bash
/break-down TASK-003
```
- **When:** A task proves too complex during planning or implementation
- **What:** Splits into subtasks (TASK-003a, TASK-003b, etc.)
- **Why:** Maintains manageable scope and clear progress tracking

### **Managing Scope Changes**
```bash
/pivot "Add user authentication to all endpoints"
```
- **When:** Requirements change or new needs emerge
- **What:** Analyzes impact on existing tasks/plans, updates PRD, creates new tasks
- **Hook Trigger:** `change-impact-tracker.py` monitors ripple effects

### **Manual Status Management**
```bash
/task-status TASK-002 blocked
/task-status TASK-002 in-progress
```
- **When:** Need to manually update task status (blocked, cancelled, etc.)
- **What:** Updates task database with status changes and audit trail

### **Context Alignment**
```bash
/sync-context
```
- **When:** Implementation has drifted from documentation or plans seem outdated
- **What:** Reconciles current code state with project documentation

---

## PHASE 5: ERROR HANDLING & DEBUGGING

### **When Errors Occur**
**🔧 cascading-debugger Agent Triggers Automatically When:**
- Compilation errors occur
- Tests fail after changes
- Runtime errors are detected
- Previous fixes create new issues

**Agent Actions:**
- Maps error relationships systematically
- Implements fixes while monitoring for cascades
- Prevents error chains from destabilizing the system

**Manual Invocation:** Use when facing complex, interconnected errors that need systematic resolution.

---

## BACKGROUND MONITORING (Hooks)

**These run automatically - no user action required:**

### **Quality Gates**
- `task-quality-gate.py`: Blocks progression on TypeScript/ESLint failures
- `plan-quality-validator.py`: Validates plans after creation
- `test-coverage-monitor.py`: Ensures adequate test coverage

### **Alignment Monitoring**
- `context-drift-detection.py`: Alerts when implementation diverges from task intent
- `plan-drift-monitor.py`: Detects deviation from execution plans
- `change-impact-tracker.py`: Tracks ripple effects from scope changes

### **Progress Tracking**
- `implementation-progress-tracker.py`: Updates plan documents with progress
- `error-cascade-monitor.py`: Prevents debugging from creating new issues

---

## DECISION FLOWCHART

### **Choose Your Execution Strategy:**

**Simple, Well-Defined Tasks:**
`/next-task` → `/plan-task` → `/execute-plan` → `/validate-implementation` → `/commit-task`

**Complex or Uncertain Tasks:**
`/next-task` → `/plan-task` → `/review-plan` → `/execute-step` (multiple) → test-specialist → `/validate-implementation` → `/commit-task`

**Changing Requirements:**
Any point → `/pivot` → Update affected plans → Continue execution

**Quality Issues:**
Hooks alert → Fix issues → cascading-debugger (if needed) → Continue

---

## COMMON SCENARIOS

### **Scenario 1: New Feature Development**
```bash
# 1. Start new project
/genesis "E-commerce checkout optimization"

# 2. Break down requirements  
/parse-prd

# 3. Work through tasks systematically
/next-task                    # Load TASK-001
/plan-task TASK-001          # Plan payment integration
/execute-plan TASK-001       # Implement payment flow
/validate-implementation TASK-001  # Run all validations
/commit-task TASK-001        # Commit changes

/next-task                   # Load TASK-002
# ... repeat cycle
```

### **Scenario 2: Bug Fix with Unknowns**
```bash
/next-task                   # Load bug fix task
/plan-task TASK-005         # Plan investigation approach
/execute-step TASK-005 1    # Start debugging
# [cascading-debugger triggers automatically if errors cascade]
/execute-step TASK-005 2    # Continue with fixes
/validate-implementation TASK-005
/commit-task TASK-005
```

### **Scenario 3: Scope Change Mid-Development**
```bash
# Currently working on TASK-003
/pivot "Add OAuth instead of basic auth"
# [System analyzes impact on all tasks]
/sync-context               # Align documentation
/plan-task TASK-003         # Replan affected task
/execute-plan TASK-003      # Continue with updated approach
```

### **Scenario 4: Complex Refactoring**
```bash
/break-down TASK-010        # Split large refactor into steps
/next-task                  # Load TASK-010a
/plan-task TASK-010a       # Plan first refactor step
/review-plan TASK-010a     # Validate approach
/execute-step TASK-010a 1  # Execute carefully step-by-step
# [test-specialist ensures tests exist for refactored code]
/execute-step TASK-010a 2
/validate-implementation TASK-010a
/commit-task TASK-010a
```

---

## OPTIMIZATION TIPS

### **For Speed:**
- Use `/execute-plan` for straightforward implementations
- Skip `/review-plan` for simple, well-understood tasks
- Let hooks handle quality monitoring automatically

### **For Quality:**
- Always use `/validate-implementation` before committing
- Use `/execute-step` for complex or risky changes
- Let planning-specialist explore thoroughly for architectural decisions

### **For Team Collaboration:**
- Use `/sync-context` regularly in team environments
- Document scope changes with `/pivot` for transparency
- Maintain detailed plans for knowledge sharing

### **For Learning:**
- Review generated plans to understand best practices
- Study validation reports to improve code quality
- Analyze hook alerts to identify patterns

---

## SUCCESS METRICS

**Quality Indicators:**
- ✅ All tasks pass `/validate-implementation`
- ✅ Hooks generate minimal alerts
- ✅ Test coverage stays above 80%
- ✅ No error cascades during debugging

**Process Indicators:**
- 📊 Consistent task completion velocity
- 📊 Minimal rework due to planning accuracy
- 📊 Rare need for `/sync-context` (good alignment)
- 📊 Effective scope management with `/pivot`

**Your taskmaster.ai-style workflow is now complete - from idea to production-ready code with enterprise-grade quality controls!**