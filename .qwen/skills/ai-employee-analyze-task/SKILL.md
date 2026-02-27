---
name: ai-employee-analyze-task
description: |
  Analyze task files in the AI Employee vault to understand what needs to be done.
  Extract key information, determine priority, identify required actions,
  and check against Company_Handbook rules.
---

# Analyze Task Files

Systematically analyze task files to understand requirements and determine appropriate actions.

## Analysis Process

### Step 1: Read Task File
```bash
# Read the task file from Needs_Action
read "F:/Personal-AI-Employee/AI_Employee_Vault/Needs_Action/<task_file>.md"
```

### Step 2: Extract Key Information
From the YAML frontmatter and content, extract:
- **Type**: What kind of task is this? (email, file_drop, approval_request, etc.)
- **Source**: Where did this task originate?
- **Priority**: What urgency level is assigned?
- **Status**: Current state of the task
- **Content**: What is the actual request/content?

### Step 3: Check Company Handbook
```bash
# Review relevant rules
read "F:/Personal-AI-Employee/AI_Employee_Vault/Company_Handbook.md"
```

Determine:
- Does this action require approval?
- What are the response time expectations?
- Are there any restrictions or guidelines?

### Step 4: Determine Actions
Based on analysis, identify:
- Immediate actions (do now)
- Deferred actions (schedule for later)
- Approval-required actions (create approval request)
- Information gathering needed (read more files)

## Task Type Handlers

### File Drop Tasks
```yaml
type: file_drop
```
**Actions:**
1. Read the source file
2. Determine file type and purpose
3. Categorize appropriately
4. Suggest next steps

### Email Tasks
```yaml
type: email
```
**Actions:**
1. Read email content
2. Identify sender (known/unknown)
3. Check priority keywords
4. Draft response or flag for human

### Approval Tasks
```yaml
type: approval_request
```
**Actions:**
1. Review requested action
2. Check against Handbook thresholds
3. Create clear approval file
4. Wait for human decision

## Priority Assessment

| Keyword | Priority | Response Time |
|---------|----------|---------------|
| urgent, asap, emergency | Urgent | 15 minutes |
| invoice, payment, help | High | 1 hour |
| meeting, deadline | Normal | 24 hours |
| general, info | Low | Batch process |

## Examples

### Analyzing a File Drop
```
Task: FILE_DROP_report_pdf_20260227_103000.md

1. Read frontmatter:
   - type: file_drop
   - source_file: report.pdf
   - priority: normal

2. Read source file content

3. Check Handbook:
   - Financial documents → flag for review
   - No auto-categorization for reports

4. Determine actions:
   - [ ] Read report.pdf content
   - [ ] Identify report type and period
   - [ ] Create approval request for categorization
```

### Analyzing an Email Task
```
Task: EMAIL_client_a_20260227.md

1. Read frontmatter:
   - type: email
   - from: client_a@example.com
   - subject: Invoice Request
   - priority: high

2. Check Handbook:
   - Known contact → can auto-respond
   - Invoice request → requires approval

3. Determine actions:
   - [ ] Draft invoice based on rates
   - [ ] Create approval request for sending
   - [ ] Update Dashboard with activity
```

## Output Format

After analysis, create or update a Plan file:

```markdown
---
type: plan
objective: Clear statement of what needs to be accomplished
created: 2026-02-27T10:30:00Z
status: active
---

# Plan: <Objective>

## Task Analysis
- **Source**: <task file>
- **Type**: <task type>
- **Priority**: <priority level>
- **Constraints**: <any handbook rules that apply>

## Steps
- [x] Read task file
- [x] Analyze requirements
- [ ] <next action>
- [ ] <next action>
- [ ] Move to Done when complete

## Approval Required
- <list any actions needing human approval>

## Notes
<additional context or observations>
```

## Related Skills

- `ai-employee-read-vault` - Read vault files
- `ai-employee-create-plan` - Create structured plans
- `ai-employee-write-vault` - Write task files
