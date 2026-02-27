---
name: ai-employee-read-vault
description: |
  Read files from the AI Employee Obsidian vault. Use to access Dashboard.md,
  Company_Handbook.md, Business_Goals.md, or any file in the vault folders.
  Essential for understanding current state before taking actions.
---

# Read Vault Files

Read files from the AI Employee Obsidian vault to understand current state, tasks, and configuration.

## Usage

Use this skill when you need to:
- Check the current Dashboard status
- Read Company_Handbook rules before taking action
- Review Business_Goals for context
- Access files in Needs_Action, Inbox, or other folders
- Read task files to understand what needs to be done

## File Paths

The vault is located at: `F:/Personal-AI-Employee/AI_Employee_Vault/`

### Key Files
| File | Purpose |
|------|---------|
| `Dashboard.md` | Real-time status overview |
| `Company_Handbook.md` | Rules of engagement |
| `Business_Goals.md` | Objectives and targets |

### Folders
| Folder | Purpose |
|--------|---------|
| `Inbox/` | Raw incoming items |
| `Needs_Action/` | Items requiring AI processing |
| `Plans/` | Task execution plans |
| `Pending_Approval/` | Awaiting human decision |
| `Approved/` | Approved for execution |
| `Rejected/` | Declined actions |
| `Done/` | Completed tasks |
| `Logs/` | Action audit logs |

## Examples

### Read Dashboard
```bash
# Using Qwen Code's built-in file reading
read "F:/Personal-AI-Employee/AI_Employee_Vault/Dashboard.md"
```

### Read All Pending Tasks
```bash
# List files in Needs_Action
ls "F:/Personal-AI-Employee/AI_Employee_Vault/Needs_Action/"

# Then read each .md file
```

### Read Company Handbook
```bash
# Before taking any action, review the rules
read "F:/Personal-AI-Employee/AI_Employee_Vault/Company_Handbook.md"
```

## Best Practices

1. **Always read Company_Handbook.md** before taking new types of actions
2. **Check Dashboard.md** to understand current system state
3. **Read all files in Needs_Action/** when starting a work session
4. **Log what you read** in your thought process for auditability

## Related Skills

- `ai-employee-write-vault` - Write/update vault files
- `ai-employee-analyze-task` - Analyze task files
- `ai-employee-move-file` - Move files between folders
