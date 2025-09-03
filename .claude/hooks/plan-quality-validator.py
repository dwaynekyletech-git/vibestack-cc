#!/usr/bin/env python3
"""
Plan Quality Validator Hook
Purpose: Validate implementation plans before execution begins
Trigger: PostToolUse (after /plan-task command completion)
Priority: HIGH - Quality assurance
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime


def main():
    """Main hook execution function"""
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
                      f"Plan: {latest_plan.name}\n"
                      f"Issues found: {len(validation_result['issues'])}\n"
                      f"Critical issues: {validation_result['critical_count']}\n"
                      f"Quality score: {validation_result['quality_score']}/100\n"
                      f"Recommendations:\n" + "\n".join(f"• {rec}" for rec in validation_result['recommendations'])
        }
    
    return {"action": "continue"}


def is_plan_task_context():
    """Check if we're in a plan-task command context"""
    try:
        # Check for recent creation of plan files
        tasks_dir = Path("tasks")
        if not tasks_dir.exists():
            return False
            
        plan_files = list(tasks_dir.glob("plan-*.md"))
        if not plan_files:
            return False
            
        # Check if any plan file was recently modified (within last 5 minutes)
        now = datetime.now().timestamp()
        recent_plans = [
            f for f in plan_files 
            if (now - f.stat().st_mtime) < 300  # 5 minutes
        ]
        
        return len(recent_plans) > 0
    except Exception:
        return False


def find_latest_plan():
    """Find the most recently created or modified plan file"""
    tasks_dir = Path("tasks")
    if not tasks_dir.exists():
        return None
    
    plan_files = list(tasks_dir.glob("plan-*.md"))
    if not plan_files:
        return None
    
    # Return most recently modified
    return max(plan_files, key=lambda f: f.stat().st_mtime)


def validate_plan_quality(plan_file):
    """Validate the quality of an implementation plan"""
    try:
        with open(plan_file, "r", encoding='utf-8') as f:
            plan_content = f.read()
    except IOError:
        return {
            "has_issues": True,
            "issues": ["Could not read plan file"],
            "critical_count": 1,
            "quality_score": 0,
            "recommendations": ["Ensure plan file is accessible"]
        }
    
    issues = []
    recommendations = []
    quality_score = 100
    
    # Check for required sections
    required_sections = [
        "## Context",
        "## Steps", 
        "## Acceptance Criteria"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in plan_content:
            missing_sections.append(section)
    
    if missing_sections:
        issues.append(f"Missing required sections: {', '.join(missing_sections)}")
        recommendations.append("Add missing sections to provide complete plan structure")
        quality_score -= 20 * len(missing_sections)
    
    # Check for step numbering/structure
    steps = re.findall(r'^\d+\.\s', plan_content, re.MULTILINE)
    if len(steps) < 3:
        issues.append("Plan has too few implementation steps (minimum 3 recommended)")
        recommendations.append("Break down implementation into more detailed steps")
        quality_score -= 15
    elif len(steps) > 20:
        issues.append("Plan has too many steps (may be overly complex)")
        recommendations.append("Consider consolidating related steps")
        quality_score -= 5
    
    # Check for file mentions (should specify what files to modify)
    file_mentions = extract_file_mentions(plan_content)
    if len(file_mentions) < 1:
        issues.append("Plan doesn't specify which files to modify")
        recommendations.append("Add specific file paths that will be modified")
        quality_score -= 15
    
    # Check for edge case considerations
    edge_case_keywords = [
        "edge case", "error handling", "validation", "fallback",
        "exception", "boundary", "limit", "timeout"
    ]
    edge_case_score = sum(1 for keyword in edge_case_keywords 
                         if keyword.lower() in plan_content.lower())
    
    if edge_case_score == 0:
        issues.append("Plan may not consider edge cases or error handling")
        recommendations.append("Add consideration for edge cases and error scenarios")
        quality_score -= 10
    
    # Check for testing mentions
    test_keywords = [
        "test", "spec", "jest", "cypress", "validate", 
        "verify", "assert", "expect"
    ]
    test_score = sum(1 for keyword in test_keywords 
                    if keyword.lower() in plan_content.lower())
    
    if test_score == 0:
        issues.append("Plan doesn't mention testing strategy")
        recommendations.append("Add testing approach to validate implementation")
        quality_score -= 10
    
    # Check for architectural considerations
    arch_keywords = [
        "architecture", "pattern", "design", "structure",
        "component", "module", "interface", "abstraction"
    ]
    arch_score = sum(1 for keyword in arch_keywords 
                    if keyword.lower() in plan_content.lower())
    
    if arch_score == 0 and len(steps) > 10:
        issues.append("Complex plan lacks architectural considerations")
        recommendations.append("Add architectural design considerations")
        quality_score -= 5
    
    # Check plan length and detail
    word_count = len(plan_content.split())
    if word_count < 200:
        issues.append("Plan appears too brief for proper implementation guidance")
        recommendations.append("Add more detailed explanations and context")
        quality_score -= 10
    elif word_count > 2000:
        issues.append("Plan is very lengthy - may be overly complex")
        recommendations.append("Consider simplifying or breaking into subtasks")
        quality_score -= 5
    
    # Check for dependency mentions
    if "dependencies" not in plan_content.lower() and "prerequisite" not in plan_content.lower():
        issues.append("Plan doesn't explicitly mention dependencies")
        recommendations.append("Add dependency analysis section")
        quality_score -= 5
    
    # Determine critical issues
    critical_keywords = ["missing", "doesn't specify", "too few", "could not"]
    critical_count = len([issue for issue in issues 
                         if any(critical.lower() in issue.lower() 
                               for critical in critical_keywords)])
    
    # Ensure quality score doesn't go below 0
    quality_score = max(0, quality_score)
    
    return {
        "has_issues": len(issues) > 0,
        "issues": issues,
        "critical_count": critical_count,
        "quality_score": quality_score,
        "recommendations": recommendations,
        "plan_stats": {
            "word_count": word_count,
            "step_count": len(steps),
            "file_mentions": len(file_mentions),
            "edge_case_score": edge_case_score,
            "test_score": test_score,
            "arch_score": arch_score
        }
    }


def extract_file_mentions(plan_content):
    """Extract file path mentions from the plan content"""
    file_patterns = [
        r'`([^`]*\.[a-zA-Z]{2,4})`',  # Files in backticks
        r'([a-zA-Z0-9_/-]+\.[a-zA-Z]{2,4})',  # General file paths
        r'([a-zA-Z0-9_/-]+/[a-zA-Z0-9_/-]*)',  # Directory paths
    ]
    
    file_mentions = []
    for pattern in file_patterns:
        matches = re.findall(pattern, plan_content)
        file_mentions.extend(matches)
    
    # Filter out common false positives and duplicates
    filtered_mentions = []
    for mention in file_mentions:
        if (not mention.startswith('http') and 
            not mention.startswith('www.') and
            '.' in mention and
            len(mention) > 2 and
            mention not in filtered_mentions):
            filtered_mentions.append(mention)
    
    return filtered_mentions


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