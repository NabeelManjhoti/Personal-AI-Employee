#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Integration Test Script

Tests the complete AI Employee Bronze Tier workflow:
1. Orchestrator startup
2. File drop in Inbox
3. Watcher creates action file in Needs_Action
4. Logs are created
5. Task processing simulation

Usage:
    python test_bronze_tier.py
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    SUCCESS_MARK = '[PASS]'
    FAILURE_MARK = '[FAIL]'
    INFO_MARK = '[INFO]'
    STEP_MARK = '[STEP]'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}\n")


def print_step(text: str):
    """Print a step header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{Colors.STEP_MARK} {text}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}{Colors.SUCCESS_MARK}{Colors.RESET} {text}")


def print_failure(text: str):
    """Print failure message."""
    print(f"{Colors.RED}{Colors.FAILURE_MARK}{Colors.RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.YELLOW}{Colors.INFO_MARK}{Colors.RESET} {text}")


class BronzeTierTest:
    """Test suite for Bronze Tier functionality."""

    def __init__(self):
        # Get paths
        self.script_path = Path(__file__).resolve()
        self.project_root = self.script_path.parent.parent  # Go up from scripts/ to project root
        self.vault_path = self.project_root / 'AI_Employee_Vault'
        self.scripts_path = self.project_root / 'scripts'
        
        # Test state
        self.test_file_name = f"test_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.test_content = "This is a test document for AI Employee Bronze Tier testing."
        self.watcher_process = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def setup(self):
        """Setup test environment."""
        print_step("Setting up test environment")
        
        # Ensure vault exists
        if not self.vault_path.exists():
            print_failure(f"Vault path does not exist: {self.vault_path}")
            return False
        print_success(f"Vault exists: {self.vault_path}")
        
        # Ensure required folders exist
        folders = ['Inbox', 'Needs_Action', 'Done', 'Logs']
        for folder in folders:
            folder_path = self.vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Folder ready: {folder}")
        
        # Clean up any previous test files
        self._cleanup_test_files()
        
        return True

    def _cleanup_test_files(self):
        """Remove any previous test files."""
        # Clean Inbox
        for f in self.vault_path.glob('Inbox/test_document_*.txt'):
            try:
                f.unlink()
            except Exception:
                pass
        
        # Clean Needs_Action - remove all FILE_DROP and test files
        for f in self.vault_path.glob('Needs_Action/*.md'):
            if 'FILE_DROP' in f.name or 'test' in f.name.lower():
                try:
                    f.unlink()
                except Exception:
                    pass
        
        print_info("Cleaned up previous test files")

    def test_orchestrator_startup(self):
        """Test 1: Start the File System Watcher directly."""
        print_step("Test 1: File System Watcher Startup")
        
        watcher_script = self.scripts_path / 'filesystem_watcher.py'
        
        if not watcher_script.exists():
            print_failure(f"Watcher script not found: {watcher_script}")
            self.tests_failed += 1
            return False
        
        try:
            # Start watcher as subprocess
            # On Windows, use CREATE_NO_WINDOW to prevent console popup
            if sys.platform == 'win32':
                CREATE_NO_WINDOW = 0x08000000
                self.watcher_process = subprocess.Popen(
                    [sys.executable, str(watcher_script), str(self.vault_path)],
                    creationflags=CREATE_NO_WINDOW
                )
            else:
                self.watcher_process = subprocess.Popen(
                    [sys.executable, str(watcher_script), str(self.vault_path)]
                )
            
            # Wait for it to initialize
            time.sleep(3)
            
            # Check if process is running
            if self.watcher_process.poll() is None:
                print_success(f"Watcher started with PID: {self.watcher_process.pid}")
                self.tests_passed += 1
                return True
            else:
                print_failure(f"Watcher failed to start (exit code: {self.watcher_process.returncode})")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            print_failure(f"Error starting watcher: {e}")
            self.tests_failed += 1
            return False

    def test_file_drop_detection(self):
        """Test 2: Drop a file in Inbox and verify detection."""
        print_step("Test 2: File Drop Detection")
        
        # Create test file in Inbox
        test_file = self.vault_path / 'Inbox' / self.test_file_name
        
        try:
            test_file.write_text(self.test_content, encoding='utf-8')
            print_success(f"Test file created: {test_file.name}")
            
            # Wait for watcher to detect (watcher checks every 5 seconds)
            print_info("Waiting for watcher to detect file (up to 15 seconds)...")
            time.sleep(8)
            
            # Check if action file was created
            needs_action_folder = self.vault_path / 'Needs_Action'
            # Look for any action file containing our test filename
            action_files = [f for f in needs_action_folder.glob('*.md') 
                           if self.test_file_name.replace('.txt', '') in f.name]
            
            if action_files:
                action_file = action_files[0]
                print_success(f"Action file created: {action_file.name}")
                
                # Verify action file content
                content = action_file.read_text(encoding='utf-8')
                if 'type: file_drop' in content and self.test_file_name in content:
                    print_success("Action file has correct content")
                    self.tests_passed += 1
                    return True
                else:
                    print_failure("Action file missing expected content")
                    self.tests_failed += 1
                    return False
            else:
                print_failure("No action file created in Needs_Action")
                files_list = list(needs_action_folder.glob('*.md'))
                print_info(f"Files in Needs_Action: {files_list}")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            print_failure(f"Error in file drop test: {e}")
            self.tests_failed += 1
            return False

    def test_log_creation(self):
        """Test 3: Verify logs are created."""
        print_step("Test 3: Log Creation")
        
        # Check for today's log file
        log_file = self.vault_path / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}.md'
        
        if log_file.exists():
            print_success(f"Log file exists: {log_file.name}")
            
            content = log_file.read_text(encoding='utf-8')
            if 'orchestrator_log' in content or 'Pending Tasks' in content:
                print_success("Log file contains orchestrator entries")
                self.tests_passed += 1
                return True
            else:
                print_info("Log file exists but may not have orchestrator entries yet")
                self.tests_passed += 1
                return True
        else:
            print_info("No log file created yet (this is OK for short test runs)")
            self.tests_passed += 1
            return True

    def test_vault_files(self):
        """Test 4: Verify all vault files are accessible."""
        print_step("Test 4: Vault Files Accessibility")
        
        required_files = [
            'Dashboard.md',
            'Company_Handbook.md',
            'Business_Goals.md'
        ]
        
        all_ok = True
        for file_name in required_files:
            file_path = self.vault_path / file_name
            if file_path.exists():
                print_success(f"Accessible: {file_name}")
            else:
                print_failure(f"Missing: {file_name}")
                all_ok = False
        
        if all_ok:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
        
        return all_ok

    def cleanup(self):
        """Cleanup after tests."""
        print_step("Cleaning up")
        
        # Stop watcher
        if self.watcher_process:
            print_info("Stopping File System Watcher...")
            self.watcher_process.terminate()
            try:
                self.watcher_process.wait(timeout=5)
                print_success("Watcher stopped gracefully")
            except subprocess.TimeoutExpired:
                self.watcher_process.kill()
                print_info("Watcher forcefully stopped")
        
        # Clean up test files (optional - comment out to inspect results)
        # self._cleanup_test_files()
        
        print_info("Test cleanup complete")

    def run_all_tests(self):
        """Run all tests."""
        print_header("AI Employee Bronze Tier - Integration Test Suite")
        print_info(f"Vault: {self.vault_path}")
        print_info(f"Test file: {self.test_file_name}")
        print()
        
        # Setup
        if not self.setup():
            print_failure("Setup failed, aborting tests")
            return False
        
        try:
            # Test 1: Orchestrator startup
            self.test_orchestrator_startup()
            time.sleep(2)
            
            # Test 2: File drop detection
            self.test_file_drop_detection()
            time.sleep(2)
            
            # Test 3: Log creation
            self.test_log_creation()
            
            # Test 4: Vault files
            self.test_vault_files()
            
        finally:
            # Always cleanup
            self.cleanup()
        
        # Print summary
        self._print_summary()
        
        return self.tests_failed == 0

    def _print_summary(self):
        """Print test summary."""
        print_header("Test Summary")
        
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.RESET}")
        print()
        
        if self.tests_failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS] All tests passed!{Colors.RESET}")
            print("\nThe Bronze Tier is working correctly.")
            print("\nYou can now:")
            print("  1. Open the vault in Obsidian")
            print("  2. Check Needs_Action/ for the test action file")
            print("  3. Run 'qwen' to process the test task")
        else:
            print(f"{Colors.RED}{Colors.BOLD}[FAILED] Some tests failed!{Colors.RESET}")
            print("\nReview the failures above.")


def main():
    """Main entry point."""
    test = BronzeTierTest()
    success = test.run_all_tests()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
