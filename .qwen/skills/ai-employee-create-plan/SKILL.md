---
name: ai-employee-create-plan
description: |
  Create structured execution plans for tasks in the AI Employee vault.
  Plans break down complex tasks into actionable steps with checkboxes,
  track progress, and identify approval requirements.
---

# Create Task Plans

Generate structured, executable plans for tasks that require multiple steps or human approval.

## When to Create a Plan

Create a Plan.md file when:
- Task requires 3+ steps to complete
- Human approval is needed at some stage
- Task spans multiple work sessions
- You need to track progress over time
- Task involves multiple file operations

## Plan Schema

```yaml
---
type: plan
task_reference: Reference to original task file
objective: Clear, measurable objective
created: 2026-02-27T10:30:00Z
updated: 2026-02-27T10:30:00Z
status: draft|active|blocked|completed
priority: low|normal|high|urgent
---
```

## Plan Structure

```markdown
# Plan: <Clear Objective Statement>

## Context
- **Task Reference**: `<task_file.md>`
- **Created**: <timestamp>
- **Priority**: <priority level>

## Objective
<Clear statement of what success looks like>

## Steps
- [ ] Step 1: First action
- [ ] Step 2: Second action
- [ ] Step 3: Third action
- [ ] Move task to Done

## Approval Requirements
| Action | Type | Status |
|--------|------|--------|
| <action> | <approval type> | pending/approved/rejected |

## Resources
- Links to relevant files
- Reference documents
- Contact information

## Notes
<Additional context, observations, or blockers>

## Completion Criteria
- [ ] All steps completed
- [ ] Approvals obtained
- [ ] Dashboard updated
- [ ] Task file moved to /Done
```

## Examples

### File Processing Plan
```markdown
---
type: plan
task_reference: FILE_DROP_report_pdf_20260227_103000.md
objective: Process and categorize Q1 financial report
created: 2026-02-27T10:30:00Z
status: active
---

# Plan: Process Q1 Financial Report

## Context
- **Task Reference**: `FILE_DROP_report_pdf_20260227_103000.md`
- **Created**: 2026-02-27 10:30:00
- **Priority**: normal

## Objective
Read, analyze, and properly categorize the Q1 financial report PDF.

## Steps
- [x] Read task file from Needs_Action
- [x] Locate and read source PDF
- [ ] Identify report type and period
- [ ] Determine appropriate category
- [ ] Create approval request for categorization
- [ ] Upon approval, move to appropriate folder
- [ ] Update Dashboard with activity
- [ ] Move task file to /Done

## Approval Requirements
| Action | Type | Status |
|--------|------|--------|
| Categorize as Q1 Financial | file_classification | pending |

## Resources
- Source file: /Inbox/report.pdf
- Company Handbook: /Company_Handbook.md (Financial Records section)

## Notes
Report appears to be quarterly financial summary based on filename.
Need human confirmation for final categorization.

## Completion Criteria
- [ ] All steps completed
- [ ] Approval obtained
- [ ] Dashboard updated
- [ ] Task file in /Done
```

### Email Response Plan
```markdown
---
type: plan
task_reference: EMAIL_client_a_20260227.md
objective: Respond to client invoice request
created: 2026-02-27T10:30:00Z
status: active
---

# Plan: Send Invoice to Client A

## Context
- **Task Reference**: `EMAIL_client_a_20260227.md`
- **Created**: 2026-02-27 10:30:00
- **Priority**: high

## Objective
Generate and send January invoice to Client A.

## Steps
- [x] Read email task file
- [x] Identify client: Client A (client_a@email.com)
- [x] Calculate amount: $1,500 (from Business_Goals.md rates)
- [ ] Generate invoice PDF
- [ ] Create approval request for email send
- [ ] Wait for human approval
- [ ] Send email via MCP
- [ ] Log transaction
- [ ] Update Dashboard
- [ ] Move task to /Done

## Approval Requirements
| Action | Type | Status |
|--------|------|--------|
| Send email to client_a@email.com | email_send | pending |
| Invoice amount $1,500 | financial | pending |

## Resources
- Client email: client_a@email.com
- Rate card: /Business_Goals.md
- Invoice template: /Invoices/template.md

## Notes
Client is known contact (approved for auto-response).
Invoice amount requires approval per Handbook rules.

## Completion Criteria
- [ ] All steps completed
- [ ] Approvals obtained
- [ ] Email sent
- [ ] Dashboard updated
```

## Best Practices

1. **One plan per task** - Keep plans focused and atomic
2. **Use checkboxes** - Enable progress tracking
3. **Reference original task** - Maintain audit trail
4. **List approvals upfront** - Clear about what needs human input
5. **Update status** - Keep plan current as work progresses
6. **Define completion** - Clear criteria for when done

## Plan Lifecycle

```
draft → active → (blocked) → completed
         ↓
      (rejected)
```

1. **Draft**: Initial creation
2. **Active**: Work in progress
3. **Blocked**: Waiting on approval or external factor
4. **Completed**: All steps done, task in /Done
5. **Rejected**: Human rejected, move to /Rejected

## Related Skills

- `ai-employee-read-vault` - Read existing files
- `ai-employee-write-vault` - Create plan files
- `ai-employee-analyze-task` - Analyze tasks before planning
- `ai-employee-update-dashboard` - Update progress
