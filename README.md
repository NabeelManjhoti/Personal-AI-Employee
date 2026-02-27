# Personal AI Employee - Bronze Tier

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

This is the **Bronze Tier** implementation of the Personal AI Employee hackathon. It provides the foundational layer for an autonomous AI agent that manages personal and business affairs using Qwen Code and Obsidian.

## 🏆 Bronze Tier Deliverables

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System monitoring)
- [x] Qwen Code successfully reading from and writing to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] All AI functionality implemented as Agent Skills

## 📁 Project Structure

```
F:\Personal-AI-Employee/
├── AI_Employee_Vault/           # Obsidian vault (Memory/GUI)
│   ├── Dashboard.md             # Real-time status overview
│   ├── Company_Handbook.md      # Rules of engagement
│   ├── Business_Goals.md        # Objectives and targets
│   ├── Inbox/                   # Raw incoming items
│   ├── Needs_Action/            # Items requiring AI processing
│   ├── Plans/                   # Task execution plans
│   ├── Pending_Approval/        # Awaiting human decision
│   ├── Approved/                # Approved for execution
│   ├── Rejected/                # Declined actions
│   ├── Done/                    # Completed tasks
│   ├── Logs/                    # Action audit logs
│   ├── Briefings/               # CEO briefings and reports
│   ├── Accounting/              # Financial records
│   └── Invoices/                # Generated invoices
├── scripts/
│   ├── filesystem_watcher.py    # File system monitoring script
│   └── requirements.txt         # Python dependencies
├── .qwen/
│   ├── mcp.json                 # MCP server configurations
│   ├── skills-lock.json         # Registered agent skills
│   └── skills/
│       ├── ai-employee-read-vault/
│       ├── ai-employee-write-vault/
│       ├── ai-employee-analyze-task/
│       ├── ai-employee-create-plan/
│       ├── ai-employee-move-file/
│       ├── ai-employee-check-approval/
│       └── ai-employee-update-dashboard/
├── QWEN.md                      # Project documentation
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Qwen Code](https://github.com/anthropics/qwen-code) | Latest | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers (future use) |

### Installation

1. **Install Python dependencies:**
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

2. **Open the vault in Obsidian:**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select `F:\Personal-AI-Employee\AI_Employee_Vault`

3. **Verify Qwen Code:**
   ```bash
   qwen --version
   ```

### Running the System

You can run either the standalone File System Watcher or the full Orchestrator.

#### Option 1: Standalone File System Watcher

The File System Watcher monitors the `Inbox/` folder for new files and creates action files in `Needs_Action/`.

```bash
# Start the watcher
python scripts/filesystem_watcher.py

# Or specify custom paths
python scripts/filesystem_watcher.py "F:/Personal-AI-Employee/AI_Employee_Vault" "F:/Personal-AI-Employee/AI_Employee_Vault/Inbox"
```

**To stop:** Press `Ctrl+C`

#### Option 2: Full Orchestrator (Recommended - Automatic Processing)

The Orchestrator manages all components including the watcher and **automatically invokes Qwen Code** to process tasks.

```bash
# Start the orchestrator
python scripts/orchestrator.py

# Or with custom settings
python scripts/orchestrator.py --vault "F:/Personal-AI-Employee/AI_Employee_Vault" --interval 60
```

**To stop:** Press `Ctrl+C`

The Orchestrator will:
- Start the File System Watcher automatically
- Check for pending tasks every 30 seconds (or custom interval)
- **Automatically invoke Qwen Code** to process tasks in Needs_Action/
- Monitor approved actions ready for execution
- Log all activities to the Logs/ folder

### How Automatic Processing Works

```
1. File dropped in Inbox/
        ↓
2. Watcher detects → Creates action file in Needs_Action/
        ↓
3. Orchestrator detects task → Invokes Qwen Code automatically
        ↓
4. Qwen Code processes task → Creates plan, executes, updates Dashboard
        ↓
5. Task moved to Done/ when complete
```

**No manual `qwen` command needed!** The system is fully autonomous.

### Testing the System

1. **Drop a file in Inbox:**
   ```bash
   # Copy any file to the Inbox folder
   copy example.txt "F:\Personal-AI-Employee\AI_Employee_Vault\Inbox\"
   ```

2. **Watcher creates action file:**
   - Check `Needs_Action/` for new `.md` file
   - File will have YAML frontmatter with metadata

3. **Process with Qwen Code:**
   ```bash
   cd F:\Personal-AI-Employee\AI_Employee_Vault
   qwen
   ```

4. **Prompt Qwen Code:**
   ```
   Check the Needs_Action folder for new tasks. Read the Company_Handbook.md for rules, then analyze and process any pending tasks. Create a plan and update the Dashboard when done.
   ```

## 🤖 Agent Skills

The following Agent Skills are registered for Qwen Code:

| Skill | Purpose |
|-------|---------|
| `ai-employee-read-vault` | Read files from the vault |
| `ai-employee-write-vault` | Write/update vault files |
| `ai-employee-analyze-task` | Analyze task files |
| `ai-employee-create-plan` | Create structured plans |
| `ai-employee-move-file` | Move files between folders |
| `ai-employee-check-approval` | Check approval status |
| `ai-employee-update-dashboard` | Update Dashboard.md |

## 📋 Usage Workflow

### 1. File Drop Workflow

```
User drops file → Inbox/
     ↓
Watcher detects → Creates action file in Needs_Action/
     ↓
Claude reads → Analyzes task per Company_Handbook
     ↓
Claude creates → Plan in Plans/
     ↓
Claude executes → Moves task to Done/
     ↓
Claude updates → Dashboard.md
```

### 2. Approval Workflow

```
Claude detects → Action requires approval
     ↓
Claude creates → Approval file in Pending_Approval/
     ↓
Human reviews → Moves to Approved/ or Rejected/
     ↓
Claude detects → File in Approved/
     ↓
Claude executes → Action
     ↓
Claude moves → To Done/
```

## 📖 Key Files

### Dashboard.md
Real-time overview of AI Employee status, pending tasks, and recent activity.

### Company_Handbook.md
Rules of engagement that govern all AI actions. Includes:
- Communication rules
- Financial thresholds
- File operation permissions
- Priority levels
- Security guidelines

### Business_Goals.md
Business objectives, revenue targets, and key metrics to track.

## 🔧 Configuration

### MCP Servers

Configure MCP servers in `.qwen/mcp.json`:

```json
{
  "servers": [
    {
      "name": "filesystem",
      "command": "node",
      "args": ["@modelcontextprotocol/server-filesystem"],
      "env": {
        "VAULT_PATH": "F:/Personal-AI-Employee/AI_Employee_Vault"
      }
    }
  ]
}
```

### Environment Variables

Create a `.env` file (gitignored) for sensitive data:

```bash
# .env
DRY_RUN=true
VAULT_PATH=F:/Personal-AI-Employee/AI_Employee_Vault
LOG_LEVEL=INFO
```

## 🛡️ Security

### Bronze Tier Security Features

- **Local-first**: All data stays on your machine
- **No credentials stored**: Vault contains no secrets
- **Human-in-the-loop**: Sensitive actions require approval
- **Audit logging**: All actions logged to `Logs/` folder
- **Read-only by default**: AI reads more than it writes

### Security Best Practices

1. Never commit `.env` files
2. Review `Company_Handbook.md` rules regularly
3. Check `Logs/` folder weekly
4. Rotate any API credentials monthly
5. Keep Obsidian vault backed up (use Git or cloud sync)

## 📊 Monitoring

### Daily Check (2 minutes)

1. Open `Dashboard.md` in Obsidian
2. Review "Pending Tasks" count
3. Check "Recent Activity" section
4. Clear any alerts

### Weekly Review (15 minutes)

1. Review all files in `Done/`
2. Check `Logs/` for patterns
3. Update `Business_Goals.md` if needed
4. Review and update `Company_Handbook.md`

## 🐛 Troubleshooting

### Watcher not detecting files

1. Check watcher is running: `python scripts/filesystem_watcher.py`
2. Verify Inbox folder path is correct
3. Check for error messages in console
4. Ensure file is not hidden or temporary

### Qwen Code not reading vault

1. Navigate to vault directory: `cd AI_Employee_Vault`
2. Verify files exist: `ls Needs_Action/`
3. Check file permissions allow read access

### Dashboard not updating

1. Ensure Claude has write permissions to vault
2. Check `Company_Handbook.md` allows dashboard updates
3. Review logs for error messages

## 📈 Next Steps (Silver Tier)

To upgrade to Silver Tier, add:

- [ ] Gmail Watcher script
- [ ] WhatsApp Watcher script
- [ ] MCP server for sending emails
- [ ] Human-in-the-loop approval workflow
- [ ] Basic scheduling via cron/Task Scheduler

## 📚 Resources

- [Hackathon Document](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code Documentation](https://github.com/anthropics/qwen-code)
- [Obsidian Help](https://help.obsidian.md/)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)

## 📝 License

This project is part of the Personal AI Employee Hackathon 2026.

---

*Bronze Tier v0.1 - Built with Qwen Code & Obsidian*
