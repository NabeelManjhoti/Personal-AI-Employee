---
name: ai-employee-write-vault
description: |
  Write or update files in the AI Employee Obsidian vault. Use to create
  action files, update Dashboard, log activities, or create plans.
  Always follow the YAML frontmatter schema for consistency.
---

# Write Vault Files

Create or update markdown files in the AI Employee Obsidian vault with proper YAML frontmatter.

## Usage

Use this skill when you need to:
- Update Dashboard.md with new status
- Create task files in Needs_Action
- Write plans in Plans/
- Log activities in Logs/
- Create approval requests in Pending_Approval/
- Update Business_Goals.md with progress

## YAML Frontmatter Standards

### Task File Schema
```yaml
---
type: task|email|file_drop|approval_request|plan
source: source description
created: 2026-02-27T10:30:00Z
status: pending|in_progress|completed|approved|rejected
priority: low|normal|high|urgent
---
```

### Approval Request Schema
```yaml
---
type: approval_request
action: action_type
description: What action is needed
created: 2026-02-27T10:30:00Z
expires: 2026-02-28T10:30:00Z
status: pending
---
```

### Plan Schema
```yaml
---
type: plan
objective: Clear objective statement
created: 2026-02-27T10:30:00Z
status: draft|active|completed
---
```

### Log Entry Schema
```yaml
---
type: log
timestamp: 2026-02-27T10:30:00Z
action_type: action category
actor: ai|human
status: success|failure|pending
---
```

## Examples

### Create Task File
```markdown
---
type: file_drop
source_file: report.pdf
detected: 2026-02-27T10:30:00Z
status: pending
priority: normal
---

# File Drop for Processing

## Source Information
- **Original File**: `report.pdf`
- **Detected**: 2026-02-27 10:30:00

## Suggested Actions
- [ ] Read and analyze file contents
- [ ] Categorize the file type
- [ ] Determine required actions
```

### Update Dashboard
```markdown
## ✅ Recent Activity
- [2026-02-27 10:45] Processed file drop: report.pdf
- [2026-02-27 10:30] System started (Bronze Tier)
```

### Create Approval Request
```markdown
---
type: approval_request
action: file_categorization
description: Categorize report.pdf as Q1 Financial Report
created: 2026-02-27T10:30:00Z
status: pending
---

## Action Details
- **File**: report.pdf
- **Proposed Category**: Q1 Financial Report
- **Destination**: /Done/Financial/

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

### Write Log Entry
```markdown
---
type: log
timestamp: 2026-02-27T10:30:00Z
action_type: file_processed
actor: ai
status: success
---

## Action
Processed file drop: report.pdf

## Result
File analyzed and categorized as Q1 Financial Report

## Next Steps
Awaiting human approval for final categorization
```

## Best Practices

1. **Always include YAML frontmatter** with required fields
2. **Use ISO 8601 format** for timestamps
3. **Be descriptive** in file content
4. **Include checkboxes** for actionable items
5. **Log all actions** for audit trail
6. **Never delete files** - move to appropriate folder

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Task | `TASK_<type>_<date>.md` | `TASK_file_drop_20260227.md` |
| Plan | `PLAN_<objective>_<date>.md` | `PLAN_invoice_client_20260227.md` |
| Approval | `APPROVAL_<action>_<date>.md` | `APPROVAL_payment_vendor_20260227.md` |
| Log | `LOG_<date>.md` | `LOG_2026-02-27.md` |
| Email | `EMAIL_<sender>_<date>.md` | `EMAIL_client_a_20260227.md` |

## Related Skills

- `ai-employee-read-vault` - Read vault files
- `ai-employee-create-plan` - Create structured plans
- `ai-employee-move-file` - Move files between folders
- `ai-employee-update-dashboard` - Update Dashboard.md
