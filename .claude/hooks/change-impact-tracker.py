#!/usr/bin/env python3
"""
Change Impact Tracker Hook
Purpose: Track ripple effects of scope changes and pivots
Trigger: PostToolUse (after /pivot command execution)
Priority: MEDIUM - Impact analysis
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path


def main():
    """Main hook execution function"""
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


def is_pivot_context():
    """Check if we're in a pivot command context"""
    try:
        # Check for recent changes to PRD or tasks.json
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
        
        # Look for pivot-related file changes
        pivot_indicators = [
            "docs/prd.md",
            "tasks/tasks.json",
            "docs/change-log.md"
        ]
        
        return any(indicator in changed_files for indicator in pivot_indicators)
    except Exception:
        return False


def analyze_change_impact():
    """Analyze the impact of recent changes"""
    # Get recent changes
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        changed_files = []
    
    # Analyze affected systems
    affected_systems = analyze_affected_systems(changed_files)
    
    # Check task impacts
    affected_tasks = check_task_impacts(changed_files)
    
    # Determine if this is high impact
    high_impact = len(affected_systems) > 2 or len(affected_tasks) > 5 or has_critical_changes(changed_files)
    
    return {
        "high_impact": high_impact,
        "affected_systems": affected_systems,
        "affected_tasks": affected_tasks,
        "changed_files": changed_files,
        "impact_score": calculate_impact_score(affected_systems, affected_tasks, changed_files),
        "recommendation": generate_recommendation(high_impact, affected_systems, affected_tasks)
    }


def analyze_affected_systems(changed_files):
    """Determine which systems are affected by the changes"""
    affected_systems = []
    
    system_patterns = {
        "Authentication": ["auth", "login", "session", "jwt", "oauth"],
        "API Layer": ["api", "endpoint", "route", "controller"],
        "Database": ["database", "db", "schema", "migration", "model"],
        "UI Components": ["component", "page", "ui", "interface"],
        "Build System": ["package.json", "tsconfig", "next.config", "webpack"],
        "Testing": ["test", "spec", "__tests__", "jest", "cypress"],
        "Documentation": ["readme", "docs", ".md"],
        "Configuration": [".env", "config", "settings"]
    }
    
    for system, patterns in system_patterns.items():
        if any(any(pattern.lower() in file.lower() for pattern in patterns) 
               for file in changed_files):
            affected_systems.append(system)
    
    return affected_systems


def check_task_impacts(changed_files):
    """Check which tasks might be affected by the changes"""
    try:
        with open("tasks/tasks.json", "r", encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        affected_tasks = []
        
        for task in tasks_data.get("tasks", []):
            task_id = task.get("id", "")
            task_description = task.get("description", "").lower()
            task_title = task.get("title", "").lower()
            
            # Check if task mentions any changed files
            task_content = f"{task_description} {task_title}".lower()
            
            for changed_file in changed_files:
                file_basename = os.path.basename(changed_file).lower()
                file_parts = changed_file.lower().split('/')
                
                # Check various matching strategies
                if (file_basename in task_content or 
                    changed_file.lower() in task_content or
                    any(part in task_content for part in file_parts if len(part) > 2)):
                    affected_tasks.append(task_id)
                    break
        
        return affected_tasks
        
    except (IOError, json.JSONDecodeError, KeyError):
        return []


def has_critical_changes(changed_files):
    """Check if any critical system files have been changed"""
    critical_files = [
        "package.json",
        "tsconfig.json",
        "next.config.js",
        "next.config.ts",
        ".env",
        ".gitignore",
        "docs/prd.md"
    ]
    
    return any(os.path.basename(file) in critical_files for file in changed_files)


def calculate_impact_score(affected_systems, affected_tasks, changed_files):
    """Calculate a numerical impact score"""
    score = 0
    
    # System impact
    score += len(affected_systems) * 2
    
    # Task impact
    score += len(affected_tasks) * 1
    
    # File count impact
    score += min(len(changed_files), 10)  # Cap at 10
    
    # Critical file bonus
    if has_critical_changes(changed_files):
        score += 5
    
    return score


def generate_recommendation(high_impact, affected_systems, affected_tasks):
    """Generate appropriate recommendation based on impact analysis"""
    if high_impact:
        recommendations = [
            "Update all affected task plans immediately",
            "Review system integration points",
            "Consider breaking changes into smaller increments"
        ]
        
        if len(affected_tasks) > 10:
            recommendations.append("Run /sync-context to realign project state")
            
        return "; ".join(recommendations)
    else:
        return "Monitor affected tasks and update plans as needed"


def log_change_impact(impact_analysis):
    """Log the change impact analysis to a file"""
    try:
        # Ensure docs directory exists
        os.makedirs("docs", exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "impact_analysis": impact_analysis
        }
        
        log_file = "docs/change-impact-log.json"
        
        if os.path.exists(log_file):
            with open(log_file, "r", encoding='utf-8') as f:
                log_data = json.load(f)
        else:
            log_data = {"impacts": []}
        
        log_data["impacts"].append(log_entry)
        
        # Keep only last 50 entries
        log_data["impacts"] = log_data["impacts"][-50:]
        
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