# Reverse Engineering Skill

A GitHub Copilot Agent Skill that reverse engineers **any GitHub repository, or any project
already sitting on your local disk**, and produces a focused 4-section report — no Anthropic
API key required, GitHub Copilot itself is the AI engine.

| # | Section | What it covers |
|---|---------|-----------------|
| 1 | **System Design Overview** | Full architecture, codebase metrics, API catalog, data model, dependency graph, modernization roadmap |
| 2 | **Authentication & Access Control** | Detects RBAC, ABAC, and ReBAC patterns with named roles, policies, and a route protection map |
| 3 | **Business Logic Extractor** | Business domain, end-to-end workflows, user roles, business rules, entity glossary |
| 4 | **Screen-by-Screen Navigation** | Complete UI screen inventory and Mermaid navigation flowchart (ASPX, Razor, React, Vue, JSP) |

See it in action → [QuickStart.md](QuickStart.md) · [SamplePrompts.md](SamplePrompts.md) ·
[SampleOutputs/](SampleOutputs/) · [Architecture.png](Architecture.png) ·
[UserGuide.pdf](UserGuide.pdf)

---

## Why use it

- **Zero API key setup** — GitHub Copilot Chat is the AI engine; the bundled Python analyzer
  needs nothing but the standard library.
- **Works on remote or local code** — point it at a GitHub URL (shallow-cloned, analyzed,
  then deleted) or a folder already on your disk (read in place, never modified).
- **One Markdown report** — the dependency graph and navigation flow render as Mermaid diagrams
  inline, so the report displays natively on GitHub, GitLab, and the VS Code preview pane with
  no extra files to open.
- **Self-excluding** — when analyzing a local project, the skill's own folder is always pruned
  from the walk, so "reverse engineer this project" never analyzes itself.

---

## Requirements

| Tool | Version |
|------|---------|
| VS Code | 1.90 or later |
| GitHub Copilot Chat extension | latest |
| Python | 3.8 or later |
| Git | any version, on PATH — only needed when analyzing a GitHub URL; not required for local-folder analysis |

---

## Installation (one-time, 2 minutes)

### Step 1 — Copy the skill folder into your project

Copy [`skill/reverse-engineering-skill/`](../skill/reverse-engineering-skill/) from this
repository into your own project's `.github/skills/` folder:

```
Your project/
└── .github/
    └── skills/
        └── reverse-engineering-skill/   ← paste this folder here
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

If `.github/skills/` doesn't exist yet, create it.

### Step 2 — Verify Python is installed

```bash
python --version
# Should print Python 3.8 or higher
```

### Step 3 — Done. Open Copilot Chat and use the skill

For a guided first run, see [QuickStart.md](QuickStart.md).

---

## Usage in VS Code

### Option A — Analyze a GitHub repository

```
Reverse engineer https://github.com/owner/repo
```

### Option B — Analyze a project already on your local disk

No cloning, no internet access — the folder is read in place and never modified.

```
Reverse engineer this project
Analyze the codebase in C:\Projects\LegacyApp
Reverse engineer ./my-app
```

Copilot will:
- Ask where to save the output files
- Run the Python analysis engine automatically (clones if it's a URL, reads in place if it's
  a local folder)
- Produce AI-quality narrative for all 4 sections
- Write the final report directly to your chosen location

More example prompts in [SamplePrompts.md](SamplePrompts.md).

---

## Where Output Files Land

By default, output is written to `./{repo-name}/` inside your current working directory:

```
your-project/
└── nopCommerce/                       ← created automatically
    ├── nopCommerce_report.md          ← 4-section focused report — open this first
    ├── nopCommerce_sdd.json           ← full system design document (JSON)
    ├── nopCommerce_evaluation.md      ← 100-point quality score
    └── manifest.json                 ← run metrics
```

No SVG diagrams or HTML dashboard are written — the dependency graph and navigation flow
render as Mermaid diagrams inline inside the report. See a real example in
[SampleOutputs/](SampleOutputs/).

You can also say:
- **"save in current folder"** → files land next to your project files
- **"save to C:\Reports"** → writes to a custom path

**Analyzing a local project?** If you're already sitting inside the folder you want analyzed,
the default option creates the output subfolder nested inside that same project — harmless
(the generated `.md`/`.json` files aren't picked up as source code on a re-run), but if you'd
rather keep outputs separate, say **"save to ../my-project-analysis"**.

---

## Running Without Copilot (CLI Only)

The script auto-detects whether the target is a remote URL (`https://`, `http://`, `git://`,
`user@host:...`) or an existing local directory — no separate flag needed.

```bash
# Remote — default output → ./{repo-name}/ in current directory
python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py \
    https://github.com/owner/repo --heuristic

# Remote — output directly to current directory
python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py \
    https://github.com/owner/repo --heuristic --output .

# Local folder — analyzed in place, nothing cloned or deleted
python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py \
    C:\Projects\LegacyApp --heuristic

# Local folder — the current directory itself
python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py \
    . --heuristic --output ..\legacyapp-analysis
```

---

## Repository Layout

This repository follows the team's standard marketplace skill layout:

```
reverse-engineering-skill-github-copilot/
├── skill/
│   └── reverse-engineering-skill/   ← the installable skill (copy this into .github/skills/)
│       ├── SKILL.md
│       ├── manifest.yaml
│       ├── scripts/
│       ├── assets/
│       ├── references/
│       └── templates/
└── marketplace/                     ← this folder — docs, guide, samples
    ├── README.md
    ├── QuickStart.md
    ├── UserGuide.pdf
    ├── Architecture.png
    ├── SamplePrompts.md
    └── SampleOutputs/
```

---

## Sharing With Your Team

- Commit `skill/reverse-engineering-skill/` inside your project's `.github/skills/` folder
- Every developer on the team gets the skill automatically when they pull
- No additional setup required for team members who already have Copilot + Python
