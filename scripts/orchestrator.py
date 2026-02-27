#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator for AI Employee - Bronze Tier

Master process that coordinates all AI Employee components:
- Manages Watcher processes
- Triggers Qwen Code for task processing
- Handles scheduling (future: cron integration)
- Monitors system health

Usage:
    python orchestrator.py

Or with custom vault path:
    python orchestrator.py --vault "F:/Personal-AI-Employee/AI_Employee_Vault"
"""

import argparse
import logging
import subprocess
import sys
import time
import signal
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)


class Orchestrator:
    """
    Main orchestrator class that manages all AI Employee components.
    """

    def __init__(self, vault_path: Path, check_interval: int = 30):
        self.vault_path = vault_path.resolve()
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Subprocess handles
        self.watcher_process: Optional[subprocess.Popen] = None
        
        # Control flags
        self.running = False
        
        # Validate vault path
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {self.vault_path}")
        
        # Ensure required folders exist
        self._ensure_folders()
        
        self.logger.info(f"Orchestrator initialized for vault: {self.vault_path}")

    def _ensure_folders(self):
        """Ensure all required vault folders exist."""
        folders = [
            'Inbox',
            'Needs_Action',
            'Done',
            'Pending_Approval',
            'Approved',
            'Rejected',
            'Plans',
            'Logs',
            'Briefings',
        ]
        
        for folder in folders:
            (self.vault_path / folder).mkdir(parents=True, exist_ok=True)

    def start_watcher(self):
        """Start the File System Watcher process."""
        script_dir = Path(__file__).parent
        watcher_script = script_dir / 'filesystem_watcher.py'
        
        if not watcher_script.exists():
            self.logger.error(f"Watcher script not found: {watcher_script}")
            return False
        
        try:
            self.logger.info("Starting File System Watcher...")
            # Use DEVNULL for stdin to avoid input redirection issues on Windows
            startupinfo = None
            if sys.platform == 'win32':
                import subprocess
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.watcher_process = subprocess.Popen(
                [sys.executable, str(watcher_script), str(self.vault_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                startupinfo=startupinfo
            )
            self.logger.info(f"Watcher started with PID: {self.watcher_process.pid}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start watcher: {e}")
            return False

    def stop_watcher(self):
        """Stop the File System Watcher process."""
        if self.watcher_process:
            self.logger.info("Stopping File System Watcher...")
            self.watcher_process.terminate()
            try:
                self.watcher_process.wait(timeout=5)
                self.logger.info("Watcher stopped gracefully")
            except subprocess.TimeoutExpired:
                self.logger.warning("Watcher did not stop gracefully, forcing...")
                self.watcher_process.kill()
            self.watcher_process = None

    def check_needs_action(self) -> List[Path]:
        """
        Check for files in Needs_Action folder.
        Returns list of files pending processing.
        """
        needs_action_folder = self.vault_path / 'Needs_Action'
        
        if not needs_action_folder.exists():
            return []
        
        return list(needs_action_folder.glob('*.md'))

    def trigger_qwen_code(self, task_files: List[Path], auto_process: bool = True):
        """
        Trigger Qwen Code to process pending tasks.
        
        Args:
            task_files: List of task files to process
            auto_process: If True, automatically invoke Qwen Code subprocess
        """
        if not task_files:
            return

        self.logger.info(f"Found {len(task_files)} task(s) requiring processing:")

        for task_file in task_files:
            self.logger.info(f"  - {task_file.name}")

        if auto_process:
            # Automatically invoke Qwen Code
            self._invoke_qwen_code(task_files)
        else:
            # Just log for manual processing
            self._log_pending_tasks(task_files)
            self.logger.info("Hint: Run 'qwen' in the vault directory to process these tasks")

    def _invoke_qwen_code(self, task_files: List[Path]):
        """
        Automatically invoke Qwen Code to process tasks.
        
        This runs Qwen Code in non-interactive mode with a prompt to process
        all files in Needs_Action folder.
        """
        self.logger.info("Invoking Qwen Code for automatic processing...")
        
        try:
            # Build the prompt for Qwen Code
            prompt = """You are the AI Employee Bronze Tier. Process all task files in the Needs_Action folder.

For each task file:
1. Read the task file and understand what needs to be done
2. Read the Company_Handbook.md for rules and guidelines
3. Create a plan in the Plans folder
4. Execute the plan step by step
5. Update the Dashboard.md with your activities
6. Move completed tasks to the Done folder

Be thorough and follow all rules in the Company Handbook. Log all your actions.

Start by listing all files in Needs_Action and then process each one."""

            # On Windows, use CREATE_NO_WINDOW to prevent console popup
            startupinfo = None
            if sys.platform == 'win32':
                import subprocess
                CREATE_NO_WINDOW = 0x08000000
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                # Run Qwen Code in non-interactive mode (positional prompt)
                qwen_process = subprocess.Popen(
                    ['qwen', '--prompt-interactive', prompt],
                    cwd=str(self.vault_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    creationflags=CREATE_NO_WINDOW
                )
            else:
                # Run Qwen Code in non-interactive mode
                qwen_process = subprocess.Popen(
                    ['qwen', '--prompt-interactive', prompt],
                    cwd=str(self.vault_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
            
            self.logger.info(f"Qwen Code invoked with PID: {qwen_process.pid}")
            
            # Don't wait for completion - let it run in background
            # The orchestrator will continue monitoring
            
        except FileNotFoundError:
            self.logger.error("Qwen Code not found. Make sure 'qwen' command is in your PATH.")
            self.logger.error("Falling back to manual mode - tasks logged for manual processing.")
            self._log_pending_tasks(task_files)
        except Exception as e:
            self.logger.error(f"Error invoking Qwen Code: {e}")
            self._log_pending_tasks(task_files)

    def _log_pending_tasks(self, task_files: List[Path]):
        """Log pending tasks to the Logs folder."""
        log_file = self.vault_path / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}.md'
        
        # Ensure Logs folder exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().isoformat()
        
        log_entry = f'''
---
type: orchestrator_log
timestamp: {timestamp}
action_type: pending_tasks_detected
count: {len(task_files)}
status: info
---

## Pending Tasks Detected

The following tasks are awaiting processing in Needs_Action:

'''
        
        for task_file in task_files:
            log_entry += f"- `{task_file.name}`\n"
        
        log_entry += f'''
## Next Steps
1. Run `qwen` in the vault directory
2. Process the pending tasks
3. Move completed tasks to Done folder

---
*Logged by Orchestrator v0.1 (Bronze Tier)*
'''
        
        # Append to log file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def check_approved_actions(self) -> List[Path]:
        """
        Check for approved actions ready for execution.
        Returns list of files in Approved folder.
        """
        approved_folder = self.vault_path / 'Approved'
        
        if not approved_folder.exists():
            return []
        
        return list(approved_folder.glob('*.md'))

    def process_approved_actions(self, approved_files: List[Path]):
        """
        Process approved actions.
        
        Note: In Bronze Tier, this just logs the approved actions.
        In Silver/Gold tiers, this would execute MCP server actions.
        """
        if not approved_files:
            return
        
        self.logger.info(f"Found {len(approved_files)} approved action(s):")
        
        for approved_file in approved_files:
            self.logger.info(f"  - {approved_file.name}")
        
        # Log for human review
        self._log_approved_actions(approved_files)
        
        self.logger.info("Hint: These actions have been approved and are ready for execution")

    def _log_approved_actions(self, approved_files: List[Path]):
        """Log approved actions to the Logs folder."""
        log_file = self.vault_path / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}.md'
        
        timestamp = datetime.now().isoformat()
        
        log_entry = f'''
---
type: orchestrator_log
timestamp: {timestamp}
action_type: approved_actions_ready
count: {len(approved_files)}
status: info
---

## Approved Actions Ready for Execution

The following actions have been approved:

'''
        
        for approved_file in approved_files:
            log_entry += f"- `{approved_file.name}`\n"
        
        log_entry += '''
## Next Steps
These actions require execution via MCP servers or manual processing.

---
*Logged by Orchestrator v0.1 (Bronze Tier)*
'''
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def run_cycle(self):
        """Run one orchestration cycle."""
        # Check for pending tasks
        pending_tasks = self.check_needs_action()
        if pending_tasks:
            self.trigger_qwen_code(pending_tasks)
        
        # Check for approved actions
        approved_actions = self.check_approved_actions()
        if approved_actions:
            self.process_approved_actions(approved_actions)

    def run(self):
        """Start the orchestrator and run until interrupted."""
        self.running = True
        
        self.logger.info("=" * 60)
        self.logger.info("AI Employee Orchestrator v0.1 (Bronze Tier)")
        self.logger.info("=" * 60)
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info("Press Ctrl+C to stop")
        self.logger.info("=" * 60)
        
        # Start watcher process
        if not self.start_watcher():
            self.logger.error("Failed to start watcher, exiting...")
            return 1
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                self.run_cycle()
                time.sleep(self.check_interval)
        except Exception as e:
            self.logger.error(f"Orchestrator error: {e}")
            return 1
        finally:
            self.shutdown()
        
        return 0

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, initiating shutdown...")
        self.running = False

    def shutdown(self):
        """Gracefully shutdown all components."""
        self.logger.info("Shutting down Orchestrator...")
        
        # Stop watcher
        self.stop_watcher()
        
        self.logger.info("Orchestrator shutdown complete")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Employee Orchestrator - Bronze Tier"
    )
    
    parser.add_argument(
        '--vault', '-v',
        type=str,
        default=None,
        help='Path to AI Employee Vault'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Determine vault path
    if args.vault:
        vault_path = Path(args.vault)
    else:
        # Default: relative to script location
        script_dir = Path(__file__).parent
        vault_path = script_dir.parent / 'AI_Employee_Vault'
    
    # Validate vault path
    if not vault_path.exists():
        logging.error(f"Vault path does not exist: {vault_path}")
        logging.info("Create the vault first or specify --vault path")
        return 1
    
    try:
        orchestrator = Orchestrator(vault_path, args.interval)
        return orchestrator.run()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
