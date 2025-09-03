#!/usr/bin/env python3
"""
Plan Drift Monitor Hook
Purpose: Monitor deviation between implementation and plan during execution
Trigger: PostToolUse (during plan execution when code changes don't match plan)
Priority: MEDIUM - Alignment monitoring
"""

import json
import os
import sys
import subprocess
import re
from pathlib import Path


def main():
    """Main hook execution function"""
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


def is_plan_execution_context():
    """Check if we're currently executing a plan"""
    try:
        # Check if there's an active task and recent code changes
        with open("tasks/tasks.json", "r", encoding='utf-8') as f:
            tasks_data = json.load(f)
            
        # Look for in-progress task
        active_task = None
        for task in tasks_data.get("tasks", []):
            if task.get("status") == "in-progress":
                active_task = task
                break
        
        if not active_task:
            return False
            
        # Check for recent git activity
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        # If there are unstaged or staged changes, we're likely executing
        return bool(result.stdout.strip())
        
    except Exception:
        return False


def analyze_plan_drift():
    """Analyze if implementation is drifting from the plan"""
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
        with open(plan_file, "r", encoding='utf-8') as f:
            plan_content = f.read()
    except IOError:
        return {"drift_detected": False}
    
    # Get recent changes
    recent_changes = get_recent_changes()
    
    # Analyze drift
    drift_issues = analyze_drift_indicators(plan_content, recent_changes)
    
    if not drift_issues:
        return {"drift_detected": False}
    
    severity = determine_drift_severity(drift_issues)
    drift_type = categorize_drift_type(drift_issues)
    
    return {
        "drift_detected": True,
        "task_id": task_id,
        "drift_type": drift_type,
        "severity": severity,
        "details": "; ".join(drift_issues),
        "recommendation": generate_drift_recommendation(severity, drift_type)
    }


def get_current_task():
    """Get the currently active task"""
    try:
        with open("tasks/tasks.json", "r", encoding='utf-8') as f:
            tasks_data = json.load(f)
            
        for task in tasks_data.get("tasks", []):
            if task.get("status") == "in-progress":
                return task
                
        return None
    except (IOError, json.JSONDecodeError):
        return None


def get_recent_changes():
    """Get information about recent code changes"""
    changes = {
        "modified_files": [],
        "added_files": [],
        "deleted_files": [],
        "recent_commits": []
    }
    
    try:
        # Get modified files (staged and unstaged)
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        for line in result.stdout.strip().split('\n'):
            if line:
                status = line[:2]
                filename = line[3:]
                
                if 'M' in status:
                    changes["modified_files"].append(filename)
                elif 'A' in status:
                    changes["added_files"].append(filename)
                elif 'D' in status:
                    changes["deleted_files"].append(filename)
        
        # Get recent commit messages
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        changes["recent_commits"] = result.stdout.strip().split('\n')
        
    except Exception:
        pass
    
    return changes


def analyze_drift_indicators(plan_content, recent_changes):
    """Analyze various indicators of plan drift"""
    drift_issues = []
    
    # Extract planned files from plan
    planned_files = extract_planned_files(plan_content)
    
    # Check if modified files are mentioned in plan
    unplanned_modifications = []
    for modified_file in recent_changes["modified_files"]:
        if not file_matches_plan(modified_file, planned_files):
            unplanned_modifications.append(modified_file)
    
    if unplanned_modifications:
        drift_issues.append(f"Modified files not in plan: {', '.join(unplanned_modifications[:3])}")
        if len(unplanned_modifications) > 3:
            drift_issues.append(f"... and {len(unplanned_modifications) - 3} more unplanned files")
    
    # Check for scope expansion
    total_changed_files = len(recent_changes["modified_files"] + recent_changes["added_files"])
    planned_file_count = len(planned_files)
    
    if total_changed_files > planned_file_count * 1.5:
        drift_issues.append("Implementation scope appears larger than planned")
    
    # Check commit messages for drift indicators
    commit_drift_score = 0
    drift_keywords = ["refactor", "fix", "debug", "change approach", "different", "pivot", "rework"]
    
    for commit in recent_changes["recent_commits"]:
        commit_lower = commit.lower()
        for keyword in drift_keywords:
            if keyword in commit_lower:
                commit_drift_score += 1
                break
    
    if commit_drift_score >= 2:
        drift_issues.append("Recent commits suggest multiple approach changes")
    elif commit_drift_score == 1:
        drift_issues.append("Recent commits suggest approach deviation")
    
    # Check for technology/library drift
    tech_drift = detect_technology_drift(plan_content, recent_changes)
    if tech_drift:
        drift_issues.extend(tech_drift)
    
    # Check for pattern/architecture drift  
    pattern_drift = detect_pattern_drift(plan_content, recent_changes)
    if pattern_drift:
        drift_issues.extend(pattern_drift)
    
    return drift_issues


def extract_planned_files(plan_content):
    """Extract file paths mentioned in the plan"""
    file_patterns = [
        r'`([^`]*\.[a-zA-Z]{2,4})`',  # Files in backticks
        r'([a-zA-Z0-9_/-]+\.[a-zA-Z]{2,4})',  # General file paths
    ]
    
    planned_files = []
    for pattern in file_patterns:
        matches = re.findall(pattern, plan_content)
        planned_files.extend(matches)
    
    # Filter and deduplicate
    return list(set(f for f in planned_files if not f.startswith('http')))


def file_matches_plan(changed_file, planned_files):
    """Check if a changed file matches any planned file"""
    changed_basename = os.path.basename(changed_file)
    
    for planned_file in planned_files:
        planned_basename = os.path.basename(planned_file)
        
        # Direct match
        if changed_file == planned_file or changed_basename == planned_basename:
            return True
            
        # Partial match (for files in same directory)
        if changed_basename in planned_file or planned_basename in changed_file:
            return True
    
    return False


def detect_technology_drift(plan_content, recent_changes):
    """Detect if implementation is using different technologies than planned"""
    drift_issues = []
    
    # Extract technology mentions from plan
    plan_lower = plan_content.lower()
    tech_keywords = {
        'react': ['react', 'jsx', 'tsx'],
        'vue': ['vue', 'vuex'],
        'angular': ['angular', 'ng'],
        'express': ['express', 'app.js'],
        'fastapi': ['fastapi', 'uvicorn'],
        'database': ['mongoose', 'prisma', 'sequelize', 'sqlite', 'postgres'],
        'testing': ['jest', 'cypress', 'mocha', 'vitest']
    }
    
    planned_tech = []
    for tech_type, keywords in tech_keywords.items():
        if any(keyword in plan_lower for keyword in keywords):
            planned_tech.append(tech_type)
    
    # Check if modified files suggest different technologies
    for file_path in recent_changes["modified_files"]:
        file_content_tech = infer_technology_from_file(file_path)
        if file_content_tech and file_content_tech not in planned_tech:
            drift_issues.append(f"Using {file_content_tech} technology not mentioned in plan")
    
    return drift_issues


def infer_technology_from_file(file_path):
    """Infer technology from file path and potentially content"""
    file_lower = file_path.lower()
    
    if '.vue' in file_lower:
        return 'vue'
    elif any(ext in file_lower for ext in ['.jsx', '.tsx']) and 'react' in file_lower:
        return 'react'
    elif 'angular' in file_lower:
        return 'angular'
    elif 'express' in file_lower or file_lower.endswith('server.js'):
        return 'express'
    elif 'fastapi' in file_lower or 'main.py' in file_lower:
        return 'fastapi'
    
    return None


def detect_pattern_drift(plan_content, recent_changes):
    """Detect if implementation patterns differ from plan"""
    drift_issues = []
    
    # Look for architectural pattern mentions in plan
    pattern_keywords = ['component', 'service', 'controller', 'model', 'view', 'middleware']
    plan_patterns = [kw for kw in pattern_keywords if kw in plan_content.lower()]
    
    # Simple heuristic: if plan mentions specific patterns but files suggest others
    if plan_patterns and recent_changes["modified_files"]:
        # This is a simplified check - could be enhanced with actual file content analysis
        pass
    
    return drift_issues


def determine_drift_severity(drift_issues):
    """Determine the severity of detected drift"""
    issue_count = len(drift_issues)
    
    # Check for high-impact keywords
    high_impact_keywords = ["scope", "technology", "architecture", "multiple"]
    high_impact_count = sum(1 for issue in drift_issues 
                           if any(keyword in issue.lower() for keyword in high_impact_keywords))
    
    if high_impact_count >= 2 or issue_count >= 4:
        return "HIGH"
    elif high_impact_count >= 1 or issue_count >= 2:
        return "MEDIUM"
    else:
        return "LOW"


def categorize_drift_type(drift_issues):
    """Categorize the type of drift detected"""
    issue_text = " ".join(drift_issues).lower()
    
    if "scope" in issue_text:
        return "Scope Expansion"
    elif "technology" in issue_text or "different" in issue_text:
        return "Technology Change"
    elif "approach" in issue_text or "commits suggest" in issue_text:
        return "Approach Change"
    elif "files not in plan" in issue_text:
        return "File Deviation"
    else:
        return "General Drift"


def generate_drift_recommendation(severity, drift_type):
    """Generate appropriate recommendation based on drift analysis"""
    base_recommendations = {
        "HIGH": "Stop implementation and update plan immediately",
        "MEDIUM": "Update plan to reflect actual implementation approach",
        "LOW": "Document deviations and continue monitoring"
    }
    
    type_specific = {
        "Scope Expansion": "Consider breaking into subtasks",
        "Technology Change": "Update plan with new technology stack",
        "Approach Change": "Document rationale for approach changes",
        "File Deviation": "Add new files to plan documentation"
    }
    
    recommendation = base_recommendations.get(severity, "Monitor next changes")
    
    if drift_type in type_specific:
        recommendation += f"; {type_specific[drift_type]}"
    
    return recommendation


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