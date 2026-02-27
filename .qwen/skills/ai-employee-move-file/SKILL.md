---
name: ai-employee-move-file
description: |
  Move files between vault folders as part of task workflow.
  Implements the claim-by-move rule and maintains audit trail.
  Used for task progression: Needs_Action → In_Progress → Done
  and approval workflow: Pending_Approval → Approved/Rejected → Done
---

# Move Files Between Folders

Move files through the vault workflow system while maintaining audit trails and preventing conflicts.

## Vault Folder Workflow

```
Inbox → Needs_Action → [In_Progress] → Done
                            ↓
                    Pending_Approval → Approved → Done
                                         ↓
                                      Rejected
```

## Move Operations

### Standard Task Flow
| From | To | Trigger |
|------|-----|---------|
| `Inbox/` | `Needs_Action/` | New item detected |
| `Needs_Action/` | `Done/` | Task completed |
| `Needs_Action/` | `Pending_Approval/` | Approval needed |
| `Pending_Approval/` | `Approved/` | Human approved |
| `Pending_Approval/` | `Rejected/` | Human rejected |
| `Approved/` | `Done/` | Action executed |

## Claim-by-Move Rule

To prevent multiple agents working on the same task:

1. **First agent to move** a file from `Needs_Action/` to `In_Progress/<agent>/` owns it
2. **Other agents must ignore** files in `In_Progress/` folders
3. **Single writer rule** for Dashboard.md (only one agent updates at a time)

## Move Function

```python
def move_file(source: Path, destination: Path, reason: str) -> bool:
    """
    Move a file and log the action.
    
    Args:
        source: Source file path
        destination: Destination file path
        reason: Reason for the move (for audit log)
    
    Returns:
        True if successful, False otherwise
    """
```

## Examples

### Complete Task Flow (Bash/Python)

```bash
# Move completed task to Done
mv "F:/Personal-AI-Employee/AI_Employee_Vault/Needs_Action/TASK_file_drop_20260227.md" \
   "F:/Personal-AI-Employee/AI_Employee_Vault/Done/TASK_file_drop_20260227.md"

# Log the action
echo "Moved task to Done - completed successfully" >> "F:/Personal-AI-Employee/AI_Employee_Vault/Logs/2026-02-27.md"
```

### Approval Workflow

```bash
# 1. Create approval request in Pending_Approval
# (AI creates file here when approval needed)

# 2. Human reviews and moves to Approved
# mv "F:/Personal-AI-Employee/AI_Employee_Vault/Pending_Approval/APPROVAL_payment.md" \
#    "F:/Personal-AI-Employee/AI_Employee_Vault/Approved/APPROVAL_payment.md"

# 3. AI detects file in Approved, executes action
# 4. Move to Done after execution
# mv "F:/Personal-AI-Employee/AI_Employee_Vault/Approved/APPROVAL_payment.md" \
#    "F:/Personal-AI-Employee/AI_Employee_Vault/Done/APPROVAL_payment.md"
```

### Python Implementation

```python
from pathlib import Path
from datetime import datetime
import shutil

def move_task_to_done(task_file: str, vault_path: Path):
    """Move a completed task to Done folder."""
    source = vault_path / 'Needs_Action' / task_file
    dest = vault_path / 'Done' / task_file
    
    if source.exists():
        shutil.move(str(source), str(dest))
        log_action('move_to_done', task_file, 'success')
        return True
    return False

def log_action(action_type: str, file_name: str, status: str):
    """Log an action to the daily log file."""
    log_file = vault_path / 'Logs' / f'{datetime.now().strftime("%Y-%m-%d")}.md'
    
    timestamp = datetime.now().isoformat()
    log_entry = f'''
---
type: log
timestamp: {timestamp}
action_type: {action_type}
file: {file_name}
status: {status}
---

## Action
Moved {file_name} to {action_type}
'''
    
    with open(log_file, 'a') as f:
        f.write(log_entry)
```

## Audit Log Format

Every move operation must be logged:

```yaml
---
type: log
timestamp: 2026-02-27T10:30:00Z
action_type: file_move
source_folder: Needs_Action
destination_folder: Done
file_name: TASK_file_drop_20260227.md
actor: ai
status: success
---

## Move Details
- **From**: `/Needs_Action/TASK_file_drop_20260227.md`
- **To**: `/Done/TASK_file_drop_20260227.md`
- **Reason**: Task completed successfully
- **Actor**: AI Employee
```

## Safety Checks

Before moving a file:

1. **Verify source exists**
2. **Check destination folder exists** (create if needed)
3. **Ensure not overwriting** existing file (add timestamp if conflict)
4. **Validate move type** is allowed per workflow
5. **Log the action** before moving

## Allowed Move Types

| Move | Allowed | Notes |
|------|---------|-------|
| Inbox → Needs_Action | ✅ Yes | Auto on detection |
| Needs_Action → Done | ✅ Yes | Task completed |
| Needs_Action → Pending_Approval | ✅ Yes | AI decision |
| Pending_Approval → Approved | ⚠️ Human only | Requires human action |
| Pending_Approval → Rejected | ⚠️ Human only | Requires human action |
| Approved → Done | ✅ Yes | After execution |
| Any → Archive | ✅ Yes | For old items |
| Done → Needs_Action | ❌ No | Re-open as new task |

## Error Handling

```python
def safe_move(source: Path, dest: Path) -> bool:
    """Safely move a file with error handling."""
    try:
        # Check source exists
        if not source.exists():
            logger.error(f"Source does not exist: {source}")
            return False
        
        # Create destination folder if needed
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle name conflicts
        if dest.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest = dest.parent / f'{dest.stem}_{timestamp}{dest.suffix}'
        
        # Perform move
        shutil.move(str(source), str(dest))
        
        # Log success
        log_action('file_move', source.name, 'success', str(dest))
        return True
        
    except Exception as e:
        logger.error(f"Move failed: {e}")
        log_action('file_move', source.name, 'failure', str(e))
        return False
```

## Related Skills

- `ai-employee-read-vault` - Read vault structure
- `ai-employee-write-vault` - Create task/approval files
- `ai-employee-update-dashboard` - Update after moves
- `ai-employee-check-approval` - Check approval status
