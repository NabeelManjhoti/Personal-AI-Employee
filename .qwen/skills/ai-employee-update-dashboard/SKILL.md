---
name: ai-employee-update-dashboard
description: |
  Update the Dashboard.md file with current status, recent activity,
  and key metrics. This is the main UI for humans to monitor AI Employee.
---

# Update Dashboard

Keep Dashboard.md current with accurate status, activity logs, and metrics.

## Dashboard Sections to Update

### 1. Quick Stats Table

| Metric | How to Calculate |
|--------|------------------|
| Pending Tasks | Count files in `Needs_Action/` |
| In Progress | Count files in `In_Progress/` (if used) |
| Awaiting Approval | Count files in `Pending_Approval/` |
| Completed Today | Count files in `Done/` with today's date |
| Completed This Week | Count files in `Done/` from last 7 days |

### 2. Inbox Status

List new items in Inbox or note "No new items"

### 3. Needs Action

Summarize items requiring AI attention

### 4. Pending Approval

List items awaiting human decision

### 5. Recent Activity

Add new entries with timestamp:
```markdown
- [YYYY-MM-DD HH:MM] <Action description>
```

### 6. Business Health

Update revenue tracking if applicable

### 7. Alerts & Notifications

Add or remove alerts based on current state

## Update Function

```python
from pathlib import Path
from datetime import datetime, timedelta

def update_dashboard(vault_path: Path, new_activity: str = None):
    """
    Update Dashboard.md with current state.
    
    Args:
        vault_path: Path to AI_Employee_Vault
        new_activity: Optional new activity to log
    """
    dashboard = vault_path / 'Dashboard.md'
    
    # Count files in each folder
    pending = len(list((vault_path / 'Needs_Action').glob('*.md')))
    awaiting_approval = len(list((vault_path / 'Pending_Approval').glob('*.md')))
    
    # Count completed today
    done_folder = vault_path / 'Done'
    today = datetime.now().strftime('%Y%m%d')
    completed_today = len([f for f in done_folder.glob('*.md') if today in f.name])
    
    # Count completed this week
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    completed_week = len([f for f in done_folder.glob('*.md') 
                         if f.name >= week_ago])
    
    # Read current dashboard
    content = dashboard.read_text()
    
    # Update timestamp
    content = content.replace(
        'last_updated: .*',
        f'last_updated: {datetime.now().isoformat()}'
    )
    
    # Update stats table
    stats_section = f'''| Metric | Value |
|--------|-------|
| Pending Tasks | {pending} |
| In Progress | 0 |
| Awaiting Approval | {awaiting_approval} |
| Completed Today | {completed_today} |
| Completed This Week | {completed_week} |'''
    
    # Update recent activity if new activity provided
    if new_activity:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        activity_entry = f'- [{timestamp}] {new_activity}\n'
        
        # Find Recent Activity section and add entry
        if '## ✅ Recent Activity' in content:
            # Insert after the header
            lines = content.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                if '## ✅ Recent Activity' in line:
                    # Skip empty line and comment
                    if i+1 < len(lines) and lines[i+1].startswith('<!--'):
                        new_lines.append(lines[i+1])
                        new_lines.append(activity_entry)
                        i += 2
            
            content = '\n'.join(new_lines)
    
    # Write updated dashboard
    dashboard.write_text(content)
```

## Examples

### Simple Activity Log

```python
update_dashboard(vault_path, "Processed file drop: report.pdf")
```

Result in Dashboard.md:
```markdown
## ✅ Recent Activity
- [2026-02-27 10:45] Processed file drop: report.pdf
- [2026-02-27 10:30] System started (Bronze Tier)
```

### Full Dashboard Update

```python
from pathlib import Path

vault_path = Path('F:/Personal-AI-Employee/AI_Employee_Vault')

# After completing a task
update_dashboard(vault_path, "Completed: Categorized Q1 financial report")

# Update alerts if needed
add_alert(vault_path, "Low priority: 3 files pending in Needs_Action")
```

## Alert Management

```python
def add_alert(vault_path: Path, alert_message: str, priority: str = 'normal'):
    """Add an alert to the Dashboard."""
    dashboard = vault_path / 'Dashboard.md'
    content = dashboard.read_text()
    
    alert_entry = f'- **[{priority.upper()}]** {alert_message}\n'
    
    if '## 🔔 Alerts & Notifications' in content:
        # Insert alert in alerts section
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if '## 🔔 Alerts & Notifications' in line:
                new_lines.append('')
                new_lines.append(alert_entry)
        
        content = '\n'.join(new_lines)
        dashboard.write_text(content)

def clear_alert(vault_path: Path, alert_text: str):
    """Remove a specific alert from Dashboard."""
    dashboard = vault_path / 'Dashboard.md'
    content = dashboard.read_text()
    
    # Find and remove alert line
    lines = content.split('\n')
    new_lines = [line for line in lines if alert_text not in line]
    
    dashboard.write_text('\n'.join(new_lines))
```

## Best Practices

1. **Update frequently** - After every significant action
2. **Be concise** - Short, clear activity descriptions
3. **Include timestamps** - All entries should have time
4. **Keep stats accurate** - Always count from actual folders
5. **Clear old alerts** - Remove resolved alerts
6. **Maintain history** - Keep last 10-20 activity entries

## Related Skills

- `ai-employee-read-vault` - Read current dashboard
- `ai-employee-write-vault` - Write dashboard sections
- `ai-employee-move-file` - Trigger dashboard updates after moves
