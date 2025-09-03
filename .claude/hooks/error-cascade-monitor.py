#!/usr/bin/env python3
"""
Error Cascade Monitor Hook
Purpose: Detect and prevent error cascades during debugging
Trigger: PostToolUse (after cascading-debugger agent execution)
Priority: HIGH - Critical for system stability
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
import re


def main():
    """Main hook execution function"""
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


def is_debugger_context():
    """Check if we're in a cascading-debugger context"""
    try:
        # Check for recent git commits or changes that suggest debugging activity
        result = subprocess.run(
            ["git", "log", "--oneline", "-3"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        recent_commits = result.stdout.lower()
        debug_keywords = ["fix", "debug", "error", "cascade", "debugger"]
        
        return any(keyword in recent_commits for keyword in debug_keywords)
    except Exception:
        return False


def scan_for_errors():
    """Scan for various types of errors in the codebase"""
    errors = []
    
    # TypeScript errors
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"], 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            ts_errors = parse_typescript_errors(result.stderr)
            errors.extend(ts_errors)
    except Exception:
        pass
    
    # Runtime errors from test runs
    try:
        result = subprocess.run(
            ["npm", "test", "--silent"], 
            capture_output=True, 
            text=True, 
            timeout=60
        )
        if result.returncode != 0:
            test_errors = parse_test_errors(result.stderr)
            errors.extend(test_errors)
    except Exception:
        pass
    
    # ESLint errors
    try:
        result = subprocess.run(
            ["npx", "eslint", ".", "--format", "json"], 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode != 0 and result.stdout:
            try:
                eslint_data = json.loads(result.stdout)
                for file_data in eslint_data:
                    for message in file_data.get("messages", []):
                        if message.get("severity", 0) >= 2:  # Error level
                            errors.append(f"ESLint error in {file_data['filePath']}: {message['message']}")
            except json.JSONDecodeError:
                pass
    except Exception:
        pass
    
    return errors


def parse_typescript_errors(stderr):
    """Parse TypeScript compiler errors from stderr"""
    errors = []
    lines = stderr.split('\n')
    
    for line in lines:
        # Look for TypeScript error patterns
        if '(' in line and ')' in line and ('error' in line.lower() or 'TS' in line):
            errors.append(f"TypeScript: {line.strip()}")
    
    return errors[:10]  # Limit to first 10 errors


def parse_test_errors(stderr):
    """Parse test errors from stderr"""
    errors = []
    lines = stderr.split('\n')
    
    for line in lines:
        # Look for common test error patterns
        if any(pattern in line.lower() for pattern in ['failed', 'error:', 'exception']):
            cleaned_line = line.strip()
            if cleaned_line:
                errors.append(f"Test: {cleaned_line}")
    
    return errors[:5]  # Limit to first 5 test errors


def analyze_error_cascade(errors):
    """Analyze if errors are related/cascading"""
    cascade_indicators = [
        "Cannot find module",
        "Property does not exist",
        "Type error", 
        "Import error",
        "is not assignable to",
        "does not exist on type",
        "Cannot resolve"
    ]
    
    cascade_count = sum(1 for error in errors 
                       if any(indicator.lower() in error.lower() for indicator in cascade_indicators))
    
    # Additional analysis: check for dependency-related errors
    dependency_errors = sum(1 for error in errors
                          if any(dep_word in error.lower() 
                               for dep_word in ["module", "import", "require", "dependency"]))
    
    total_error_count = len(errors)
    cascade_ratio = cascade_count / max(total_error_count, 1)
    
    # Determine risk level
    if cascade_count > 5 or cascade_ratio > 0.7:
        risk_level = "HIGH"
    elif cascade_count > 2 or cascade_ratio > 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    # Generate recommendation
    if risk_level == "HIGH":
        recommendation = "Stop and run cascading-debugger agent immediately"
    elif risk_level == "MEDIUM":
        recommendation = "Consider running cascading-debugger agent"
    else:
        recommendation = "Monitor next changes carefully"
    
    return {
        "is_cascade": cascade_count > 1 or cascade_ratio > 0.3,
        "risk_level": risk_level,
        "cascade_count": cascade_count,
        "total_errors": total_error_count,
        "dependency_errors": dependency_errors,
        "recommendation": recommendation
    }


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