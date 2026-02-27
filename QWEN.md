# Personal AI Employee Project

## Project Overview

This is a **code project** for building a "Digital FTE" (Full-Time Equivalent) — an autonomous AI employee that manages personal and business affairs 24/7. The system uses **Qwen Code** as the reasoning engine, **Obsidian** as the knowledge base/dashboard, and **MCP (Model Context Protocol)** servers for external integrations.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Personal AI Employee                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  Watchers   │───▶│  Qwen Code   │───▶│  MCP Servers  │  │
│  │  (Python)   │    │  (Brain)     │    │  (Hands)      │  │
│  │  - Gmail    │    │  + Ralph     │    │  - Email      │  │
│  │  - WhatsApp │    │    Wiggum    │    │  - Browser    │  │
│  │  - FileSystem│   │    Loop      │    │  - FileSystem │  │
│  └─────────────┘    └──────────────┘    └───────────────┘  │
│         │                  │                    │           │
│         ▼                  ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Obsidian Vault (Memory/GUI)             │   │
│  │  /Inbox  /Needs_Action  /Done  /Pending_Approval    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Watchers** | Python scripts monitoring Gmail, WhatsApp, filesystem | Planned (see hackathon doc) |
| **Qwen Code** | Reasoning engine with Ralph Wiggum persistence loop | External (CLI tool) |
| **MCP Servers** | External system integration (browser, email, filesystem) | `@modelcontextprotocol/*` |
| **Obsidian Vault** | Long-term memory, dashboard, task state | `AI_Employee_Vault/` (to be created) |
| **Skills** | Agent capabilities for Qwen Code | `.qwen/skills/` |

### Key Concepts

- **Watcher Pattern**: Lightweight Python scripts run continuously, detecting triggers (new emails, messages, files) and creating `.md` action files in `/Needs_Action`
- **Ralph Wiggum Loop**: A Qwen Code plugin that keeps the agent working autonomously until tasks are complete (intercepts exit and re-injects prompts)
- **Human-in-the-Loop**: Sensitive actions (payments, sending emails) require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Agent Skills**: Modular AI capabilities defined in `.qwen/skills/` directory

---

## Building and Running

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Qwen Code](https://github.com/anthropics/qwen-code) | Latest | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts & orchestration |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers & automation |
| [GitHub Desktop](https://desktop.github.com/download/) | Latest | Version control |

### Hardware Requirements

- **Minimum**: 8GB RAM, 4-core CPU, 20GB free disk
- **Recommended**: 16GB RAM, 8-core CPU, SSD storage
- **For always-on**: Dedicated mini-PC or cloud VM

### Setup Steps

1. **Install prerequisites** listed above
2. **Create Obsidian vault** named `AI_Employee_Vault` at `F:/Personal-AI-Employee/`
3. **Verify Qwen Code**: `qwen --version`
4. **Install Playwright** (for browser automation):
   ```bash
   npx @playwright/mcp@latest --port 8808 --shared-browser-context
   ```
5. **Configure MCP servers** in `.qwen/mcp.json`

### Running the System

#### Start Browser MCP Server
```bash
# Recommended: Use helper script
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Or manually
npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

#### Verify Server
```bash
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

#### Stop Browser MCP Server
```bash
# Recommended: Use helper script
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh

# Or manually
python .qwen/skills/browsing-with-playwright/scripts/mcp-client.py call -u http://localhost:8808 -t browser_close -p '{}'
pkill -f "@playwright/mcp"
```

#### Start Watcher Scripts (TODO)
Watcher scripts for Gmail, WhatsApp, and filesystem monitoring are documented in the hackathon guide but not yet implemented. See `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` for implementation templates.

#### Run Ralph Wiggum Loop (TODO)
```bash
# Start a Ralph loop for autonomous task processing
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

---

## Development Conventions

### Project Structure

```
F:\Personal-AI-Employee/
├── .qwen/
│   ├── mcp.json              # MCP server configurations
│   ├── skills-lock.json      # Registered agent skills
│   └── skills/
│       └── browsing-with-playwright/
│           ├── SKILL.md              # Skill documentation
│           ├── references/
│           │   └── playwright-tools.md  # Auto-generated tool schemas
│           └── scripts/
│               ├── mcp-client.py     # Universal MCP client (HTTP + stdio)
│               ├── verify.py         # Server health check
│               ├── start-server.sh   # Server startup helper
│               └── stop-server.sh    # Server shutdown helper
├── AI_Employee_Vault/        # Obsidian vault (to be created)
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Business_Goals.md
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── In_Progress/
│   ├── Pending_Approval/
│   ├── Approved/
│   └── Done/
└── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md
```

### Coding Style

- **Python**: Use type hints, follow PEP 8, docstrings for all functions
- **Shell scripts**: Use `#!/bin/bash` shebang, quote variables
- **Markdown**: Use YAML frontmatter for metadata in vault files
- **Agent Skills**: Follow the pattern in `.qwen/skills/browsing-with-playwright/SKILL.md`

### Testing Practices

- **MCP Server Verification**: Run `verify.py` after starting any MCP server
- **Watcher Testing**: Test each watcher independently before integration
- **Human-in-the-Loop**: Always test approval workflows with mock data first

### Contribution Guidelines

1. **New Watchers**: Follow the `BaseWatcher` abstract class pattern (see hackathon doc)
2. **New MCP Servers**: Add configuration to `.qwen/mcp.json`
3. **New Skills**: Create skill directory under `.qwen/skills/` with `SKILL.md`
4. **Vault Schema**: Document any new file types/templates in `Company_Handbook.md`

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_...md` | Comprehensive hackathon guide with architecture, templates, and tiered deliverables |
| `skills-lock.json` | Registry of agent skills (local and GitHub-sourced) |
| `.qwen/mcp.json` | MCP server configurations (currently: filesystem server) |
| `.qwen/skills/browsing-with-playwright/SKILL.md` | Browser automation skill documentation |
| `.qwen/skills/browsing-with-playwright/scripts/mcp-client.py` | Universal MCP client supporting HTTP and stdio transports |

---

## Hackathon Tiers

| Tier | Description | Estimated Time |
|------|-------------|----------------|
| **Bronze** | Foundation: Obsidian vault, one watcher, basic Claude integration | 8-12 hours |
| **Silver** | Functional: Multiple watchers, MCP servers, approval workflow | 20-30 hours |
| **Gold** | Autonomous: Full integration, Odoo accounting, weekly audits | 40+ hours |
| **Platinum** | Production: Cloud deployment, domain specialization, A2A sync | 60+ hours |

---

## Weekly Research Meetings

- **When**: Wednesdays at 10:00 PM
- **Where**: [Zoom](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1) (Meeting ID: 871 8870 7642, Passcode: 744832)
- **Archive**: [YouTube](https://www.youtube.com/@panaversity)

---

## TODO Items

- [ ] Create Obsidian vault structure (`AI_Employee_Vault/`)
- [ ] Implement Gmail Watcher script
- [ ] Implement WhatsApp Watcher script (Playwright-based)
- [ ] Implement File System Watcher script
- [ ] Set up email MCP server
- [ ] Configure Ralph Wiggum persistence loop
- [ ] Create `Dashboard.md` template
- [ ] Create `Company_Handbook.md` with engagement rules
- [ ] Implement weekly CEO Briefing generation
