#!/usr/bin/env python3
"""
Context Drift Detection Hook
Purpose: Monitor alignment between implementation and original task intent
Trigger: PostToolUse (after significant code changes - Edit, MultiEdit, Write)
Priority: MEDIUM - Preventive monitoring
"""

import json
import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime


def main():
    """Main hook execution function"""
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
                      f"Task: {current_task['id']} - {current_task.get('title', 'Unknown')}\n"
                      f"Drift severity: {drift_analysis['severity']}\n"
                      f"Issues found: {drift_analysis['issues']}\n"
                      f"Recommendation: {drift_analysis['recommendation']}"
        }
    
    return {"action": "continue"}


def get_current_task():
    """Get the currently active task from tasks.json"""
    try:
        with open("tasks/tasks.json", "r", encoding='utf-8') as f:
            tasks_data = json.load(f)
            
        # Find task with status "in-progress" or "planning"
        for task in tasks_data.get("tasks", []):
            if task.get("status") in ["in-progress", "planning"]:
                return task
                
        return None
    except (IOError, json.JSONDecodeError, KeyError):
        return None


def analyze_context_drift(task):
    """Analyze if recent changes align with task intent"""
    # Get recent git changes
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
        
        # Also get staged changes
        staged_result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=10
        )
        staged_files = staged_result.stdout.strip().split("\n") if staged_result.stdout.strip() else []
        
        all_changed_files = list(set(changed_files + staged_files))
        all_changed_files = [f for f in all_changed_files if f]  # Remove empty strings
        
    except Exception:
        all_changed_files = []
    
    # Load task plan if exists
    task_id = task.get("id", "").lower()
    plan_file = f"tasks/plan-{task_id}.md"
    planned_files = []
    
    if os.path.exists(plan_file):
        try:
            with open(plan_file, "r", encoding='utf-8') as f:
                plan_content = f.read()
                # Extract file mentions from plan (pattern matching for file paths)
                file_patterns = [
                    r'`([^`]*\.[a-zA-Z]{2,4})`',  # Files in backticks
                    r'([a-zA-Z0-9_/-]+\.[a-zA-Z]{2,4})',  # General file paths
                ]
                
                for pattern in file_patterns:
                    matches = re.findall(pattern, plan_content)
                    planned_files.extend(matches)
                    
                # Remove duplicates and filter out common false positives
                planned_files = list(set(f for f in planned_files 
                                       if not f.startswith('http') and '.' in f))
        except IOError:
            pass
    
    # Detect drift
    issues = []
    
    # Files changed that weren't in plan
    unexpected_changes = []
    for changed_file in all_changed_files:
        file_basename = os.path.basename(changed_file)
        file_matches_plan = any(
            file_basename in planned_file or changed_file in planned_file
            for planned_file in planned_files
        )
        if not file_matches_plan:
            unexpected_changes.append(changed_file)
    
    if unexpected_changes:
        issues.append(f"Unexpected file changes: {', '.join(unexpected_changes[:5])}")
        if len(unexpected_changes) > 5:
            issues.append(f"... and {len(unexpected_changes) - 5} more files")
    
    # Large number of files changed - may indicate scope creep
    if len(all_changed_files) > 10:
        issues.append("Large number of files changed - may indicate scope creep")
    
    # Check for changes in critical system files
    critical_files = ['package.json', 'tsconfig.json', '.env', 'next.config.js', 'next.config.ts']
    critical_changes = [f for f in all_changed_files if os.path.basename(f) in critical_files]
    if critical_changes:
        issues.append(f"Critical system files modified: {', '.join(critical_changes)}")
    
    # Check task description alignment
    task_description = task.get("description", "").lower()
    task_title = task.get("title", "").lower()
    
    # Simple heuristic: if task is about specific functionality but we're changing unrelated files
    if task_description or task_title:
        task_keywords = extract_keywords(task_description + " " + task_title)
        file_context = " ".join(all_changed_files).lower()
        
        if task_keywords and not any(keyword in file_context for keyword in task_keywords):
            issues.append("Changed files don't seem related to task description")
    
    # Determine severity
    severity = "HIGH" if len(issues) > 2 else "MEDIUM" if issues else "LOW"
    
    return {
        "drift_detected": len(issues) > 0,
        "severity": severity,
        "issues": ", ".join(issues),
        "changed_files": all_changed_files,
        "planned_files": planned_files,
        "recommendation": "Review task scope and update plan" if severity == "HIGH" 
                         else "Monitor next changes" if severity == "MEDIUM"
                         else "Continue as planned"
    }


def extract_keywords(text):
    """Extract meaningful keywords from task description"""
    # Simple keyword extraction - could be enhanced
    common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    keywords = [word for word in words if len(word) > 3 and word not in common_words]
    return keywords[:5]  # Return top 5 keywords


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