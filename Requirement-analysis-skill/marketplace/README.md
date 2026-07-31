# Requirement Analysis Skill

A polyglot agent skill for the **Planning / Pre-development** phase of the SDLC. Given a
free-text feature or change request, it deterministically identifies which file(s) to
touch, the exact function/class/line to change, an existing pattern to follow, and the
security, compliance, and formatting rules that apply — no Anthropic API key required,
the host AI (Claude Code, GitHub Copilot, or Cursor) is the narrative engine.

| # | Output | What it covers |
|---|--------|-----------------|
| 1 | **Files To Update** | Ranked candidate files, each with a match-reason and exact symbol/line to change or add near |
| 2 | **New File Suggestion** | If no existing file fits, a suggested path and naming convention |
| 3 | **Pattern To Follow** | An existing implementation of the same kind, as a structural template |
| 4 | **Security & Compliance Checklist** | Rule-based checklist keyed to the change type and domain (auth, payments, PII, external integrations) |
| 5 | **Formatting & Linting** | Detected formatter/linter plus the existing indent/quote/line-ending style of each target file |

See it in action → [QuickStart.md](QuickStart.md) · [SamplePrompts.md](SamplePrompts.md) ·
[SampleOutputs/](SampleOutputs/) · [Architecture.png](Architecture.png) ·
[UserGuide.pdf](UserGuide.pdf)

---

## Why use it

LLMs are great at writing code once you tell them where. They are much less reliable at
*finding* where — especially in a large, unfamiliar codebase, where a guess can mean
editing the wrong service, missing an existing convention, or skipping a security control
every other endpoint already has.

- **Deterministic** — the same requirement text and repo state always produce the same
  file ranking and checklist. No randomness, no LLM calls in the engine itself.
- **Explainable** — every candidate file lists *why* it was selected (path, symbol, and
  content matches).
- **Security & compliance aware** — the checklist is generated from the type of change
  (API, database, UI, config) and the domain it touches (auth, payments, PII, external
  integrations), each item citing a standard (OWASP, PCI-DSS, etc.).
- **Polyglot** — Python, JavaScript/TypeScript, Java, C#, Go.
- **Zero dependencies** — pure Python standard library, no API key, fully offline.

---

## How it complements `change-impact-analysis-skill`

```
  Requirement Analysis Skill                Change Impact Analysis Skill
  ──────────────────────────                ────────────────────────────
  "I want to add X"                         "I already changed these files"
        │                                            │
        ▼                                            ▼
  Which file(s)? Where exactly?             What breaks? What's the risk?
  What pattern? What security/              What tests are needed? Who
  compliance/formatting rules?              owns the affected code?
        │                                            │
        ▼                                            ▼
   implementation_plan.md                     impact_report.md
                                               deployment_checklist.md
```

Use this skill **before** writing code, then
[`change-impact-analysis-skill`](../../change-impact-analysis-skill/) **after**, to
assess the blast radius of what you wrote. See a worked example of the full pipeline in
[SampleOutputs/](SampleOutputs/).

---

## Requirements

| Tool | Version | Required |
|------|---------|----------|
| Python | 3.8 or later | Yes |
| Git | any | No — this skill does not use git at all |

No third-party packages. No API key.

---

## Installation (one-time, ~1 minute)

Copy [`skill/requirement-analysis/`](../skill/requirement-analysis/) from this
repository into your own project's skills folder:

**Claude Code**
```
your-project/
└── .claude/
    └── skills/
        └── requirement-analysis/   ← paste this folder here
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

**GitHub Copilot** — same layout under `.github/skills/requirement-analysis/`.
**Cursor** — same layout under `.cursor/skills/requirement-analysis/`.

If the parent directory doesn't exist yet, create it.

**Verify Python:**
```bash
python --version
# Should print Python 3.8 or higher
```

For a guided first run, see [QuickStart.md](QuickStart.md).

---

## Usage

Ask any of these (or similar) in your AI assistant's chat:

```
I want to add a discount_code field to the Order model and expose it on the orders API
Where should I implement dark mode for the settings page?
What files do I need to change to add 2FA to login?
Plan the changes needed to fix the expired-token bug in the auth endpoint
```

The assistant will:
- Ask where to save the output (or use the default `./requirement-analysis-output/`)
- Run the Python analysis engine
- Read the JSON result and present a narrative plan
- Write `implementation_plan.md` and `requirement_analysis.json` to your chosen location

More example prompts in [SamplePrompts.md](SamplePrompts.md).

---

## Where Output Files Land

By default, output is written to `./requirement-analysis-output/` inside your current
working directory:

```
your-project/
└── requirement-analysis-output/
    ├── implementation_plan.md      ← open this first
    └── requirement_analysis.json   ← machine-readable
```

You can also say:
- **"don't save, just show me"** → JSON-only mode (`--json-only`), nothing written
- **"save to ./reports"** → writes to a custom path

See a real example in [SampleOutputs/](SampleOutputs/).

---

## Running Without an AI Agent (CLI Only)

```bash
# Default output location
python .claude/skills/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add a discount_code field to the Order model and expose it on the orders API"

# Custom repo path and output directory
python .claude/skills/requirement-analysis/scripts/requirement_analysis_skill.py \
  --repo-path /path/to/repo \
  --requirement "Fix the login endpoint to reject expired tokens" \
  --output ./reports/

# JSON only (stdout) — pipe into other tooling
python .claude/skills/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add a dark mode toggle to the settings page" --json-only

# Return more candidate files (default: 5)
python .claude/skills/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add rate limiting to all public API endpoints" --top-n 10
```

---

## Repository Layout

This repository follows the team's standard marketplace skill layout:

```
Requirement-analysis-skill/
├── skill/
│   └── requirement-analysis/   ← the installable skill (copy this into .claude/skills/)
│       ├── SKILL.md
│       ├── manifest.yaml
│       ├── scripts/
│       ├── assets/
│       ├── references/
│       └── templates/
└── marketplace/                 ← this folder — docs, guide, samples
    ├── README.md
    ├── QuickStart.md
    ├── UserGuide.pdf
    ├── Architecture.png
    ├── SamplePrompts.md
    └── SampleOutputs/
```

---

## Sharing With Your Team

- Commit `skill/requirement-analysis/` inside your project's `.claude/skills/` (or
  `.github/skills/` / `.cursor/skills/`) folder
- Every developer on the team gets the skill automatically when they pull
- No additional setup required beyond Python 3.8+
