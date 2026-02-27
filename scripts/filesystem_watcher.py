#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher for AI Employee - Bronze Tier

Monitors a drop folder for new files and creates corresponding action files
in the Needs_Action folder of the Obsidian vault.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder

Or run with defaults (uses vault in project root):
    python filesystem_watcher.py
"""

import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class FileDropHandler(FileSystemEventHandler):
    """
    Handles file creation events in the drop folder.
    Creates corresponding .md action files in the vault's Needs_Action folder.
    """

    def __init__(self, vault_path: Path, drop_path: Path):
        super().__init__()
        self.vault_path = vault_path
        self.drop_path = drop_path
        self.needs_action = vault_path / 'Needs_Action'
        self.processed_files = set()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_file_hash(self, file_path: Path) -> str:
        """Generate a hash for the file to track if we've processed it."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return str(file_path.stat().st_mtime)

    def _create_action_file(self, source: Path) -> Path:
        """
        Create a markdown action file in Needs_Action folder.
        Returns the path to the created file.
        """
        # Generate unique ID based on filename and timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = source.name.replace(' ', '_').replace('.', '_')
        action_filename = f'FILE_DROP_{safe_name}_{timestamp}.md'
        action_path = self.needs_action / action_filename

        # Get file metadata
        try:
            stat = source.stat()
            file_size = stat.st_size
            created = datetime.fromtimestamp(stat.st_ctime).isoformat()
            modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception as e:
            self.logger.warning(f"Could not get file metadata: {e}")
            file_size = 0
            created = datetime.now().isoformat()
            modified = created

        # Create markdown content with YAML frontmatter
        content = f'''---
type: file_drop
source_file: {source.name}
source_path: {source.absolute()}
file_size: {file_size}
created: {created}
modified: {modified}
detected: {datetime.now().isoformat()}
status: pending
priority: normal
---

# File Drop for Processing

## Source Information
- **Original File**: `{source.name}`
- **Location**: `{source.absolute()}`
- **Size**: {file_size:,} bytes
- **Detected**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## File Content Preview
<!-- AI Employee should read the source file and analyze its contents -->

## Suggested Actions
- [ ] Read and analyze file contents
- [ ] Categorize the file type and purpose
- [ ] Determine required actions
- [ ] Move to appropriate folder after processing
- [ ] Update Dashboard.md with activity

## Notes
<!-- AI Employee or human can add notes here -->

---
*Created by File System Watcher v0.1 (Bronze Tier)*
'''

        # Write the action file
        action_path.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {action_path}")

        # Also create a copy of the file in Needs_Action if it's a text-based file
        text_extensions = {'.txt', '.md', '.csv', '.json', '.xml', '.yaml', '.yml', '.log'}
        if source.suffix.lower() in text_extensions:
            try:
                import shutil
                dest_file = self.needs_action / f'{source.name}_{timestamp}'
                shutil.copy2(source, dest_file)
                self.logger.info(f"Copied source file to: {dest_file}")
            except Exception as e:
                self.logger.warning(f"Could not copy source file: {e}")

        return action_path

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Skip if already processed
        file_hash = self._get_file_hash(source)
        if file_hash in self.processed_files:
            self.logger.debug(f"File already processed: {source}")
            return

        # Skip temporary files and hidden files
        if source.name.startswith('~') or source.name.startswith('.'):
            self.logger.debug(f"Skipping temporary/hidden file: {source}")
            return

        # Skip files in subdirectories
        if source.parent != self.drop_path:
            self.logger.debug(f"Skipping file in subdirectory: {source}")
            return

        self.logger.info(f"New file detected: {source}")

        try:
            # Small delay to ensure file is fully written
            time.sleep(0.5)

            # Create the action file
            action_path = self._create_action_file(source)

            # Mark as processed
            self.processed_files.add(file_hash)

            self.logger.info(f"Successfully processed: {source} -> {action_path}")

        except Exception as e:
            self.logger.error(f"Error processing file {source}: {e}")


class FileSystemWatcher:
    """
    Main watcher class that sets up and runs the file system observer.
    """

    def __init__(self, vault_path: str, drop_path: str = None, check_interval: int = 5):
        self.vault_path = Path(vault_path).resolve()
        
        # Default drop folder is "Inbox" in vault
        if drop_path:
            self.drop_path = Path(drop_path).resolve()
        else:
            self.drop_path = self.vault_path / 'Inbox'

        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        # Validate paths
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {self.vault_path}")

        # Create drop folder if it doesn't exist
        self.drop_path.mkdir(parents=True, exist_ok=True)

        # Ensure Needs_Action folder exists
        needs_action = self.vault_path / 'Needs_Action'
        needs_action.mkdir(parents=True, exist_ok=True)

    def run(self):
        """Start the file watcher and run until interrupted."""
        self.logger.info(f"Starting File System Watcher")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Drop folder: {self.drop_path}")

        # Create event handler and observer
        event_handler = FileDropHandler(self.vault_path, self.drop_path)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_path), recursive=False)

        # Start observing
        observer.start()
        self.logger.info(f"Watching for new files in: {self.drop_path}")
        self.logger.info("Press Ctrl+C to stop")

        try:
            while True:
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info("Stopping watcher...")
            observer.stop()

        observer.join()
        self.logger.info("Watcher stopped")


def main():
    """Main entry point."""
    import sys

    # Default paths (relative to script location)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up from scripts/ to project root
    default_vault = project_root / 'AI_Employee_Vault'
    default_drop = default_vault / 'Inbox'

    # Parse command line arguments
    if len(sys.argv) >= 2:
        vault_path = sys.argv[1]
    else:
        vault_path = str(default_vault)

    if len(sys.argv) >= 3:
        drop_path = sys.argv[2]
    else:
        drop_path = str(default_drop)

    try:
        watcher = FileSystemWatcher(vault_path, drop_path)
        watcher.run()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
