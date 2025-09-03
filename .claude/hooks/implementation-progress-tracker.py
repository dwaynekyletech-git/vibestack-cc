#!/usr/bin/env python3
"""
Implementation Progress Tracker Hook
Purpose: Track implementation progress and update plan documents
Trigger: PostToolUse (after /execute-step command execution)
Priority: LOW - Progress monitoring
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path


def main():
    """Main hook execution function"""
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
                      f"Step completed: {progress_update['completed_step']}/{progress_update['total_steps']}\n"
                      f"Overall progress: {progress_update['progress_percentage']}%\n"
                      f"Time estimate: {progress_update['time_estimate']}\n"
                      f"Status: {progress_update['status']}"
        }
    
    return {"action": "continue"}


def is_execute_step_context():
    """Check if we're in an execute-step command context"""
    try:
        # Check for recent modifications to plan files (indicating step execution)
        tasks_dir = Path("tasks")
        if not tasks_dir.exists():
            return False
            
        plan_files = list(tasks_dir.glob("plan-*.md"))
        if not plan_files:
            return False
            
        # Check if any plan file was recently modified (within last 2 minutes)
        now = datetime.now().timestamp()
        recent_updates = [
            f for f in plan_files 
            if (now - f.stat().st_mtime) < 120  # 2 minutes
        ]
        
        return len(recent_updates) > 0
    except Exception:
        return False


def track_implementation_progress():
    """Track and update implementation progress"""
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
    
    # Determine if we should alert (every 25% completion or significant milestones)
    should_alert = (
        progress_info["progress_percentage"] > 0 and
        (progress_info["progress_percentage"] % 25 == 0 or
         progress_info["milestone_reached"] or
         progress_info["progress_percentage"] == 100)
    )
    
    return {
        "should_alert": should_alert,
        "task_id": task_id,
        "completed_step": progress_info["last_completed_step"],
        "total_steps": progress_info["total_steps"],
        "progress_percentage": progress_info["progress_percentage"],
        "time_estimate": progress_info["time_estimate"],
        "status": progress_info["status"]
    }


def get_current_task():
    """Get the currently active task"""
    try:
        with open("tasks/tasks.json", "r", encoding='utf-8') as f:
            tasks_data = json.load(f)
            
        # Find task with status "in-progress"
        for task in tasks_data.get("tasks", []):
            if task.get("status") == "in-progress":
                return task
                
        return None
    except (IOError, json.JSONDecodeError, KeyError):
        return None


def update_plan_progress(plan_file, task_id):
    """Update plan file with current progress"""
    try:
        with open(plan_file, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Count total steps and completed steps
        total_steps = len(re.findall(r'^\d+\.\s', content, re.MULTILINE))
        completed_steps = len(re.findall(r'^\d+\.\s.*[✓✅]', content, re.MULTILINE))
        
        # Also check for alternative completion markers
        completed_steps += len(re.findall(r'^\d+\.\s.*\[COMPLETED\]', content, re.MULTILINE))
        completed_steps += len(re.findall(r'^\d+\.\s.*\(DONE\)', content, re.MULTILINE))
        
        progress_percentage = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0
        
        # Determine status and time estimate
        if progress_percentage == 100:
            status = "Completed"
            time_estimate = "Task finished"
        elif progress_percentage >= 75:
            status = "Nearly complete"
            time_estimate = "Almost done"
        elif progress_percentage >= 50:
            status = "Good progress"
            time_estimate = "On track"
        elif progress_percentage >= 25:
            status = "Early progress"
            time_estimate = "Getting started"
        else:
            status = "Just started"
            time_estimate = "Beginning implementation"
        
        # Check for milestone markers
        milestone_reached = check_milestones(content, progress_percentage)
        
        # Add or update progress section
        progress_section = generate_progress_section(
            completed_steps, total_steps, progress_percentage, status
        )
        
        if "## Progress Tracking" not in content:
            content += progress_section
        else:
            # Update existing progress section
            content = re.sub(
                r'## Progress Tracking.*?(?=\n##|\Z)', 
                progress_section.strip(), 
                content, 
                flags=re.DOTALL
            )
        
        # Write updated content back
        with open(plan_file, "w", encoding='utf-8') as f:
            f.write(content)
        
        return {
            "progress_percentage": progress_percentage,
            "last_completed_step": completed_steps,
            "total_steps": total_steps,
            "time_estimate": time_estimate,
            "status": status,
            "milestone_reached": milestone_reached
        }
        
    except (IOError, re.error) as e:
        return {
            "progress_percentage": 0,
            "last_completed_step": 0,
            "total_steps": 0,
            "time_estimate": "Unknown",
            "status": "Error tracking progress",
            "milestone_reached": False,
            "error": str(e)
        }


def generate_progress_section(completed_steps, total_steps, progress_percentage, status):
    """Generate the progress tracking section for the plan"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Create progress bar
    bar_length = 20
    filled_length = int(bar_length * progress_percentage / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    return f"""

## Progress Tracking
- **Steps completed:** {completed_steps}/{total_steps}
- **Progress:** {progress_percentage}% {bar}
- **Status:** {status}
- **Last updated:** {timestamp}

### Implementation Notes
- Track any deviations from the original plan here
- Note any blockers or issues encountered
- Record decisions made during implementation
"""


def check_milestones(content, progress_percentage):
    """Check if any implementation milestones have been reached"""
    milestone_keywords = [
        "milestone", "phase complete", "major step", 
        "integration point", "key feature", "core functionality"
    ]
    
    # Look for milestone markers in recently completed steps
    recent_content = content.lower()
    return any(keyword in recent_content for keyword in milestone_keywords)


def log_progress(task_id, progress_info):
    """Log progress information to a progress log file"""
    try:
        # Ensure tasks directory exists
        os.makedirs("tasks", exist_ok=True)
        
        log_file = "tasks/progress-log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "progress": progress_info
        }
        
        # Load existing log
        if os.path.exists(log_file):
            with open(log_file, "r", encoding='utf-8') as f:
                log_data = json.load(f)
        else:
            log_data = {"progress_entries": []}
        
        log_data["progress_entries"].append(log_entry)
        
        # Keep only last 100 entries
        log_data["progress_entries"] = log_data["progress_entries"][-100:]
        
        # Write updated log
        with open(log_file, "w", encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
            
    except Exception:
        # Fail silently if logging fails
        pass


if __name__ == "__main__":
    try:
        result = main()
        print(json.dumps(result))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({
            "action": "continue",
            "message": f"Hook execution failed: {str(e)}"
        }))
        sys.exit(0)