---
name: ai-employee-check-approval
description: |
  Check the approval status of files in the vault workflow.
  Monitor Pending_Approval, Approved, and Rejected folders.
  Implement human-in-the-loop pattern for sensitive actions.
---

# Check Approval Status

Monitor and process approval workflow files. Implements the human-in-the-loop pattern.

## Approval Workflow

```
┌─────────────────┐     ┌──────────┐     ┌───────────┐
│ Needs_Action    │────▶│ Pending  │────▶│ Approved  │
│ (AI processes)  │     │ Approval │     │ (Execute) │
└─────────────────┘     └──────────┘     └───────────┘
                              │                │
                              ▼                ▼
                        ┌──────────┐     ┌───────────┐
                        │ Rejected │     │   Done    │
                        │ (Archive)│     │           │
                        └──────────┘     └───────────┘
```

## When Approval is Required

Per Company_Handbook.md, approval is ALWAYS required for:

| Action Category | Threshold | Approval |
|-----------------|-----------|----------|
| Email replies | New contacts | ✅ Yes |
| Email replies | Bulk sends | ✅ Yes |
| Payments | Any amount | ✅ Yes |
| Payments | New payees | ✅ Yes (explicit) |
| Payments | > $100 | ✅ Yes |
| Social media | Replies, DMs | ✅ Yes |
| Social media | Scheduled posts | ⚪ Auto (draft only) |
| File operations | Delete | ❌ Never (archive instead) |
| File operations | Move outside vault | ❌ Never |

## Approval File Schema

```yaml
---
type: approval_request
action: <action_type>
description: <clear description>
created: 2026-02-27T10:30:00Z
expires: 2026-02-28T10:30:00Z
status: pending
---

# Approval Request: <Action Name>

## Details
- **Action Type**: <type>
- **Description**: <what needs to be done>
- **Parameters**: <relevant details>

## Context
<Why this action is needed>

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder.

## Questions?
Leave a comment in this file or contact human directly.
```

## Checking for Approvals

### Python Implementation

```python
from pathlib import Path
from datetime import datetime

def check_pending_approvals(vault_path: Path) -> list:
    """
    Check for files awaiting approval.
    
    Returns list of pending approval files.
    """
    pending_folder = vault_path / 'Pending_Approval'
    
    if not pending_folder.exists():
        return []
    
    pending_files = list(pending_folder.glob('*.md'))
    
    # Check for expired approvals
    expired = []
    for file in pending_files:
        content = file.read_text()
        if 'expires:' in content:
            # Parse expiry date and check
            pass
    
    return pending_files

def check_approved_ready(vault_path: Path) -> list:
    """
    Check for approved files ready for execution.
    
    Returns list of files in Approved folder.
    """
    approved_folder = vault_path / 'Approved'
    
    if not approved_folder.exists():
        return []
    
    return list(approved_folder.glob('*.md'))

def process_approval_cycle(vault_path: Path):
    """
    Main approval processing loop.
    
    1. Check for new approvals in Approved/
    2. Execute approved actions
    3. Move to Done after execution
    4. Log all actions
    """
    approved_files = check_approved_ready(vault_path)
    
    for file in approved_files:
        try:
            # Read approval details
            content = file.read_text()
            
            # Execute the approved action
            result = execute_approved_action(content, vault_path)
            
            # Log result
            log_approval_result(file.name, result)
            
            # Move to Done
            if result['success']:
                move_to_done(file, vault_path)
            else:
                move_to_rejected(file, vault_path, result['error'])
                
        except Exception as e:
            log_approval_result(file.name, {'success': False, 'error': str(e)})
```

## Creating Approval Requests

```python
def create_approval_request(vault_path: Path, action_type: str, 
                           description: str, parameters: dict,
                           expires_hours: int = 24) -> Path:
    """
    Create a new approval request file.
    
    Returns path to created file.
    """
    pending_folder = vault_path / 'Pending_Approval'
    pending_folder.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now()
    filename = f"APPROVAL_{action_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
    filepath = pending_folder / filename
    
    expires = datetime.now()
    from datetime import timedelta
    expires += timedelta(hours=expires_hours)
    
    content = f'''---
type: approval_request
action: {action_type}
description: {description}
created: {timestamp.isoformat()}
expires: {expires.isoformat()}
status: pending
---

# Approval Request: {description}

## Details
- **Action Type**: {action_type}
- **Created**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **Expires**: {expires.strftime('%Y-%m-%d %H:%M:%S')}

## Parameters
'''
    
    for key, value in parameters.items():
        content += f"- **{key}**: {value}\n"
    
    content += f'''
## Context
This action requires human approval per Company Handbook rules.

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder with a note explaining why.

---
*Created by AI Employee v0.1 (Bronze Tier)*
'''
    
    filepath.write_text(content)
    return filepath
```

## Examples

### Payment Approval Request

```markdown
---
type: approval_request
action: payment
description: Pay vendor invoice #1234
created: 2026-02-27T10:30:00Z
expires: 2026-02-28T10:30:00Z
status: pending
---

# Approval Request: Pay Vendor Invoice #1234

## Details
- **Amount**: $500.00
- **Recipient**: Vendor Name (Bank: XXXX1234)
- **Reference**: Invoice #1234
- **Due Date**: 2026-03-05

## Context
Invoice received and verified against purchase order.
Payment is within budget and approved threshold.

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder with a note explaining why.
```

### Email Send Approval

```markdown
---
type: approval_request
action: email_send
description: Send invoice to Client A
created: 2026-02-27T10:30:00Z
expires: 2026-02-28T10:30:00Z
status: pending
---

# Approval Request: Send Invoice Email

## Details
- **To**: client_a@example.com
- **Subject**: January 2026 Invoice - $1,500
- **Attachment**: /Invoices/2026-01_Client_A.pdf

## Email Body
Dear Client A,

Please find attached your invoice for January 2026.
Amount due: $1,500
Due date: 2026-03-15

Thank you for your business!

Best regards,
AI Employee

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder.
```

## Best Practices

1. **Always include expiry** - Approval requests should expire
2. **Be specific** - Clear description of what's being approved
3. **Include context** - Why is this action needed?
4. **Log everything** - Every approval action must be logged
5. **Check frequently** - Poll Approved/ folder regularly
6. **Handle rejections gracefully** - Learn from rejected actions

## Related Skills

- `ai-employee-read-vault` - Read approval files
- `ai-employee-write-vault` - Create approval requests
- `ai-employee-move-file` - Move approval files
- `ai-employee-update-dashboard` - Update approval status
