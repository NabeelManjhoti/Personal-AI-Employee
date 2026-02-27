#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Verification Script

Verifies that all Bronze Tier components are properly set up and functional.

Usage:
    python verify_bronze_tier.py
"""

import sys
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    # Windows-safe checkmarks
    SUCCESS_MARK = '[OK]'
    FAILURE_MARK = '[FAIL]'
    INFO_MARK = '[INFO]'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}{Colors.SUCCESS_MARK}{Colors.RESET} {text}")


def print_failure(text: str):
    """Print failure message."""
    print(f"{Colors.RED}{Colors.FAILURE_MARK}{Colors.RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.YELLOW}{Colors.INFO_MARK}{Colors.RESET} {text}")


def check_directory(path: Path, name: str) -> bool:
    """Check if a directory exists."""
    if path.exists() and path.is_dir():
        print_success(f"Directory exists: {name}")
        return True
    else:
        print_failure(f"Directory missing: {name}")
        return False


def check_file(path: Path, name: str) -> bool:
    """Check if a file exists."""
    if path.exists() and path.is_file():
        print_success(f"File exists: {name}")
        return True
    else:
        print_failure(f"File missing: {name}")
        return False


def check_file_content(path: Path, required_strings: list, name: str) -> bool:
    """Check if a file contains required strings."""
    if not path.exists():
        print_failure(f"File missing: {name}")
        return False
    
    try:
        content = path.read_text(encoding='utf-8')
        missing = []
        for s in required_strings:
            if s not in content:
                missing.append(s)
        
        if missing:
            print_failure(f"File {name} missing content: {missing}")
            return False
        else:
            print_success(f"File {name} has required content")
            return True
    except Exception as e:
        print_failure(f"Error reading {name}: {e}")
        return False


def check_skill_directory(path: Path, name: str) -> bool:
    """Check if a skill directory exists with SKILL.md."""
    if not path.exists() or not path.is_dir():
        print_failure(f"Skill directory missing: {name}")
        return False
    
    skill_file = path / 'SKILL.md'
    if not skill_file.exists():
        print_failure(f"SKILL.md missing in: {name}")
        return False
    
    print_success(f"Skill configured: {name}")
    return True


def verify_python_dependencies() -> bool:
    """Check if required Python packages are installed."""
    try:
        import watchdog
        print_success("Python dependency installed: watchdog")
        return True
    except ImportError:
        print_failure("Python dependency missing: watchdog")
        print_info("Install with: pip install -r scripts/requirements.txt")
        return False


def main():
    """Run all verification checks."""
    print_header("Personal AI Employee - Bronze Tier Verification")
    
    # Get project root (scripts/ is inside project root)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent  # Go up from scripts/ to project root
    vault_path = project_root / 'AI_Employee_Vault'
    
    all_passed = True
    
    # 1. Check Project Structure
    print_header("1. Project Structure")
    
    directories = [
        (vault_path, "AI_Employee_Vault"),
        (vault_path / 'Inbox', "Inbox"),
        (vault_path / 'Needs_Action', "Needs_Action"),
        (vault_path / 'Done', "Done"),
        (vault_path / 'Pending_Approval', "Pending_Approval"),
        (vault_path / 'Approved', "Approved"),
        (vault_path / 'Rejected', "Rejected"),
        (vault_path / 'Plans', "Plans"),
        (vault_path / 'Logs', "Logs"),
        (vault_path / 'Briefings', "Briefings"),
        (vault_path / 'Accounting', "Accounting"),
        (vault_path / 'Invoices', "Invoices"),
        (project_root / 'scripts', "scripts"),
        (project_root / '.qwen' / 'skills', ".qwen/skills"),
    ]
    
    for dir_path, name in directories:
        if not check_directory(dir_path, name):
            all_passed = False
    
    # 2. Check Core Vault Files
    print_header("2. Core Vault Files")
    
    vault_files = [
        (vault_path / 'Dashboard.md', "Dashboard.md"),
        (vault_path / 'Company_Handbook.md', "Company_Handbook.md"),
        (vault_path / 'Business_Goals.md', "Business_Goals.md"),
    ]
    
    for file_path, name in vault_files:
        if not check_file(file_path, name):
            all_passed = False
    
    # 3. Check Vault File Content
    print_header("3. Vault File Content Validation")
    
    # Dashboard.md checks
    check_file_content(
        vault_path / 'Dashboard.md',
        ['last_updated:', 'Quick Stats', 'Recent Activity'],
        "Dashboard.md"
    ) or (all_passed := False)
    
    # Company_Handbook.md checks
    check_file_content(
        vault_path / 'Company_Handbook.md',
        ['Rules of Engagement', 'Security Guidelines', 'version:'],
        "Company_Handbook.md"
    ) or (all_passed := False)
    
    # Business_Goals.md checks
    check_file_content(
        vault_path / 'Business_Goals.md',
        ['Q1 2026 Objectives', 'Key Metrics', 'review_frequency:'],
        "Business_Goals.md"
    ) or (all_passed := False)
    
    # 4. Check Agent Skills
    print_header("4. Agent Skills")
    
    skills = [
        "ai-employee-read-vault",
        "ai-employee-write-vault",
        "ai-employee-analyze-task",
        "ai-employee-create-plan",
        "ai-employee-move-file",
        "ai-employee-check-approval",
        "ai-employee-update-dashboard",
    ]
    
    for skill in skills:
        skill_path = project_root / '.qwen' / 'skills' / skill
        if not check_skill_directory(skill_path, skill):
            all_passed = False
    
    # 5. Check Scripts
    print_header("5. Watcher Scripts")

    scripts = [
        (project_root / 'scripts' / 'filesystem_watcher.py', "filesystem_watcher.py"),
        (project_root / 'scripts' / 'orchestrator.py', "orchestrator.py"),
        (project_root / 'scripts' / 'requirements.txt', "requirements.txt"),
    ]

    for file_path, name in scripts:
        if not check_file(file_path, name):
            all_passed = False

    # 6. Check Python Dependencies
    print_header("6. Python Dependencies")
    
    if not verify_python_dependencies():
        all_passed = False
    
    # 7. Check Configuration Files
    print_header("7. Configuration Files")
    
    config_files = [
        (project_root / 'skills-lock.json', "skills-lock.json"),
        (project_root / '.qwen' / 'mcp.json', ".qwen/mcp.json"),
        (project_root / 'README.md', "README.md"),
    ]
    
    for file_path, name in config_files:
        if not check_file(file_path, name):
            all_passed = False
    
    # 8. Check skills-lock.json content
    print_header("8. Skills Registry Validation")
    
    check_file_content(
        project_root / 'skills-lock.json',
        ['ai-employee-read-vault', 'ai-employee-write-vault', 'ai-employee-analyze-task'],
        "skills-lock.json"
    ) or (all_passed := False)
    
    # 9. Final Summary
    print_header("Verification Summary")
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS] All Bronze Tier checks passed!{Colors.RESET}\n")
        print("Your AI Employee Bronze Tier is ready to use.")
        print("\nNext steps:")
        print("  1. Open the vault in Obsidian:")
        print(f"     {vault_path}")
        print("\n  2. Start the Orchestrator (recommended):")
        print("     python scripts/orchestrator.py")
        print("\n  3. Drop a file in the Inbox folder to test")
        print("\n  4. Use Qwen Code to process tasks:")
        print("     qwen")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}[FAILED] Some checks failed!{Colors.RESET}\n")
        print("Please review the failures above and fix them.")
        print("\nCommon fixes:")
        print("  - Install Python dependencies: pip install -r scripts/requirements.txt")
        print("  - Ensure all directories are created")
        print("  - Check that all .md files exist in AI_Employee_Vault/")
        return 1


if __name__ == '__main__':
    sys.exit(main())
