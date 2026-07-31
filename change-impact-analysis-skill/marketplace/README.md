# Change Impact Analysis Skill

A polyglot agent skill for the **Deployment / Release** phase of the SDLC. Given a set of
changed files (or auto-detected via git), it builds a directed dependency graph,
traverses it to find every directly and transitively affected module, validates API
contracts for breaking changes, maps files to owners, and computes a deterministic 0–100
deployment risk score — no Anthropic API key required, the host AI (Claude Code, GitHub
Copilot, or Cursor) is the narrative engine.

| # | Output | What it covers |
|---|--------|-----------------|
| 1 | **Impact Report** | Full structured analysis — impacted modules, APIs, regression areas |
| 2 | **Risk Score** | 0–100 deployment risk score: LOW / MEDIUM / HIGH / CRITICAL |
| 3 | **Required Tests** | Per-module test suite recommendations |
| 4 | **Consumer Apps** | Downstream applications in the blast radius |
| 5 | **API Violations** | OpenAPI / GraphQL / Protobuf breaking changes detected |
| 6 | **Deploy Checklist** | Ready-to-use pre/post deployment sign-off checklist |

See it in action → [QuickStart.md](QuickStart.md) · [SamplePrompts.md](SamplePrompts.md) ·
[SampleOutputs/](SampleOutputs/) · [Architecture.png](Architecture.png) ·
[UserGuide.pdf](UserGuide.pdf)

---

## Why use it

Code review catches bugs. Test suites catch regressions. But neither tells you which
modules are *transitively* affected by your change (N hops away in the import graph),
whether any API contracts break for downstream consumers, or what the deployment risk
score is — a single number your release manager can act on.

- **Deterministic** — same inputs always produce the same outputs. No randomness.
- **Explainable** — every affected file has a traceable import-chain path back to the
  change.
- **Transitive** — catches indirect dependencies that code review always misses.
- **Polyglot** — Python, JavaScript/TypeScript, Java, C#, Go.
- **Fast** — sub-second BFS on an in-memory graph, even at 100k files.
- **No-Git fallback** — `--from-git` degrades gracefully to a filesystem mtime scan when
  there's no usable Git diff; see [UserGuide.pdf](UserGuide.pdf) for the fallback chain.

---

## How it complements `requirement-analysis-skill`

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

Use [`requirement-analysis-skill`](../../Requirement-analysis-skill/) **before** writing
code, then this skill **after**, to assess the blast radius of what you wrote. See a
worked example of the full pipeline in [SampleOutputs/](SampleOutputs/).

---

## Requirements

| Tool | Version | Required |
|------|---------|----------|
| Python | 3.8 or later | Yes |
| Git | any, on PATH | Recommended — enables `--from-git`; not required with `--changed-files` |
| PyYAML | 6.0+ | Optional — enables YAML-format OpenAPI spec parsing |

---

## Installation (one-time, ~2 minutes)

Copy [`skill/change-impact-analysis/`](../skill/change-impact-analysis/) from this
repository into your own project's skills folder:

**Claude Code**
```
your-project/
└── .claude/
    └── skills/
        └── change-impact-analysis/   ← paste this folder here
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

**GitHub Copilot** — same layout under `.github/skills/change-impact-analysis/`.
**Cursor** — same layout under `.cursor/skills/change-impact-analysis/`, plus a
`.cursor/rules/change-impact-analysis.mdc` rule pointing at the skill's `SKILL.md`.

**Verify Python:**
```bash
python --version
# Should print Python 3.8 or higher
```

**(Optional) install PyYAML for YAML OpenAPI spec support:**
```bash
pip install -r .claude/skills/change-impact-analysis/assets/requirements.txt
```

For a guided first run, see [QuickStart.md](QuickStart.md).

---

## Usage

Ask any of these (or similar) in your AI assistant's chat:

```
Analyse the change impact for this PR
What is the deployment risk score for my changes?
What tests do I need to run before deploying?
Who owns the code I just changed?
Is it safe to deploy?
What APIs are broken by my changes?
```

The assistant will:
- Ask how to identify changed files (auto-detect from git, or you list them)
- Ask where to save output (or use the default `./change-impact-output/`)
- Run the Python analysis engine
- Provide AI-quality narrative — blast radius, contract assessment, release recommendation
- Write the final report and checklist to your chosen location

More example prompts in [SamplePrompts.md](SamplePrompts.md).

---

## Where Output Files Land

By default, output is written to `./change-impact-output/` inside your current working
directory:

```
your-project/
└── change-impact-output/
    ├── impact_report.md          ← open this first
    ├── impact_analysis.json      ← machine-readable (CI/CD)
    └── deployment_checklist.md   ← sign-off checklist
```

See a real example in [SampleOutputs/](SampleOutputs/).

---

## Running Without an AI Agent (CLI / CI)

```bash
# Auto-detect changes from git (recommended)
python .claude/skills/change-impact-analysis/scripts/change_impact_skill.py \
  --from-git --base-branch main

# Explicit file list
python .claude/skills/change-impact-analysis/scripts/change_impact_skill.py \
  --changed-files src/api/users.py src/models/user.py

# JSON-only (stdout) — pipe into CI gates
python .claude/skills/change-impact-analysis/scripts/change_impact_skill.py \
  --from-git --json-only | jq '.risk.score'
```

### CI/CD gate example (GitHub Actions)

```yaml
- name: Change Impact Gate
  run: |
    SCORE=$(python .claude/skills/change-impact-analysis/scripts/change_impact_skill.py \
      --from-git --json-only \
      | python -c "import sys,json; print(json.load(sys.stdin)['risk']['score'])")
    if [ "$SCORE" -gt "80" ]; then
      echo "CRITICAL risk ($SCORE/100) — deployment blocked"
      exit 1
    fi
```

---

## Risk Score Quick Reference

| Score | Level | Action |
|-------|-------|--------|
| 0–30 | **LOW** | Standard release pipeline |
| 31–60 | **MEDIUM** | Deploy with monitoring; notify on-call |
| 61–80 | **HIGH** | Senior review + rollback plan required |
| 81–100 | **CRITICAL** | Block deployment; tech lead escalation |

Five factors drive the score: change volume · transitive spread · API contract
violations · module type risk (database/API surface) · consumer breadth. See
[UserGuide.pdf](UserGuide.pdf) for the full breakdown.

---

## Repository Layout

This repository follows the team's standard marketplace skill layout:

```
change-impact-analysis-skill/
├── skill/
│   └── change-impact-analysis/   ← the installable skill (copy this into .claude/skills/)
│       ├── SKILL.md
│       ├── manifest.yaml
│       ├── scripts/
│       ├── assets/
│       ├── references/
│       └── templates/
└── marketplace/                   ← this folder — docs, guide, samples
    ├── README.md
    ├── QuickStart.md
    ├── UserGuide.pdf
    ├── Architecture.png
    ├── SamplePrompts.md
    └── SampleOutputs/
```

---

## Sharing With Your Team

- Commit `skill/change-impact-analysis/` inside your project's `.claude/skills/` (or
  `.github/skills/` / `.cursor/skills/`) folder
- Every developer on the team gets the skill automatically when they pull
- No additional setup required beyond Python 3.8+
