#!/usr/bin/env python3
"""
Task Quality Gate Hook
Purpose: Enforce code quality standards before task progression
Trigger: PostToolUse (after any code modification during task execution)
Priority: HIGH - Blocks execution on failure
"""

import subprocess
import json
import os
import sys
from pathlib import Path


def main():
    """Main hook execution function"""
    # Check if we're in a task execution context
    if not os.path.exists("tasks/tasks.json"):
        return {"action": "continue"}
    
    quality_checks = []
    
    # TypeScript compilation check
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"], 
            capture_output=True, 
            text=True, 
            timeout=30,
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            quality_checks.append(f"TypeScript errors: {result.stderr}")
    except subprocess.TimeoutExpired:
        quality_checks.append("TypeScript check timed out")
    except FileNotFoundError:
        # TypeScript not available, skip check
        pass
    except Exception as e:
        quality_checks.append(f"TypeScript check failed: {str(e)}")
    
    # ESLint code quality validation
    try:
        result = subprocess.run(
            ["npx", "eslint", ".", "--format", "json"], 
            capture_output=True, 
            text=True, 
            timeout=30,
            cwd=os.getcwd()
        )
        if result.returncode != 0 and result.stdout:
            try:
                errors = json.loads(result.stdout)
                error_count = sum(len(file.get("messages", [])) for file in errors)
                if error_count > 0:
                    quality_checks.append(f"ESLint violations: {error_count} issues found")
            except json.JSONDecodeError:
                # If JSON parsing fails, treat as error
                if result.stderr:
                    quality_checks.append(f"ESLint check failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        quality_checks.append("ESLint check timed out")
    except FileNotFoundError:
        # ESLint not available, skip check
        pass
    except Exception as e:
        quality_checks.append(f"ESLint check failed: {str(e)}")
    
    # Pattern consistency verification
    pattern_issues = check_code_patterns()
    quality_checks.extend(pattern_issues)
    
    if quality_checks:
        return {
            "action": "block",
            "message": f"Quality gate failed:\n" + "\n".join(f"• {check}" for check in quality_checks) + 
                      "\n\nPlease fix these issues before proceeding."
        }
    
    return {"action": "continue"}


def check_code_patterns():
    """Check for common anti-patterns and consistency issues"""
    issues = []
    
    try:
        # Check for common anti-patterns in TypeScript/JavaScript files
        ts_files = list(Path(".").rglob("*.ts")) + list(Path(".").rglob("*.tsx"))
        js_files = list(Path(".").rglob("*.js")) + list(Path(".").rglob("*.jsx"))
        
        all_files = ts_files + js_files
        
        # Filter out node_modules
        all_files = [f for f in all_files if "node_modules" not in str(f)]
        
        for file_path in all_files[:20]:  # Limit to first 20 files for performance
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for console.log in production code (excluding test files)
                if not any(test_pattern in str(file_path).lower() 
                          for test_pattern in ['test', 'spec', '__tests__']):
                    if 'console.log(' in content:
                        issues.append(f"console.log found in {file_path}")
                
                # Check for TODO/FIXME comments in committed code
                if any(marker in content for marker in ['TODO', 'FIXME', 'XXX']):
                    issues.append(f"TODO/FIXME comments found in {file_path}")
                        
            except (IOError, UnicodeDecodeError):
                # Skip files that can't be read
                continue
                
        # Limit to first 3 pattern issues to avoid overwhelming output
        issues = issues[:3]
        
    except Exception:
        # Fail silently on pattern checking errors
        pass
    
    return issues


if __name__ == "__main__":
    try:
        result = main()
        print(json.dumps(result))
        sys.exit(0 if result["action"] == "continue" else 1)
    except Exception as e:
        print(json.dumps({
            "action": "continue",
            "message": f"Hook execution failed: {str(e)}"
        }))
        sys.exit(0)