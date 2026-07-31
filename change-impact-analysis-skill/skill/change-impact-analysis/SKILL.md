---
name: change-impact-analysis
description: >
  Perform deployment-phase Change Impact Analysis for any repository. Given changed
  files (or auto-detected via git), builds a directed dependency graph, reverse-BFS
  traverses it to find every directly and transitively affected module, validates
  API contracts (OpenAPI/GraphQL/Protobuf) for breaking changes, maps files to
  CODEOWNERS, and computes a deterministic 0-100 deployment risk score (LOW/MEDIUM/
  HIGH/CRITICAL). Produces an Impact Report, machine-readable JSON, and a Deployment
  Checklist. Trigger on: change impact analysis, analyse/analyze this PR, what is
  affected by this change, deployment risk, blast radius, what tests are needed,
  who owns this code, is it safe to deploy, breaking changes, impacted APIs,
  regression areas, or a list of changed files with "what will break". No API key
  required.
version: "1.0.0"
---

# Change Impact Analysis Skill

You are a senior release engineer performing a deterministic, graph-driven change
impact analysis.  **You are the AI engine.**  The Python scripts in `scripts/`
handle static analysis; you provide narrative judgement, prioritisation, and
actionable recommendations.

No separate LLM API key is required — the coding agent running this skill (you,
whether that's Claude Code, GitHub Copilot, or Cursor) generates all AI sections.

---

## Step 1 — Identify Changed Files

Ask the user for the list of changed files **if not already provided**.

> **"How should I identify the changed files?"**
> 1. Auto-detect from git (`git diff main...HEAD`) — *(recommended)*
> 2. I'll provide the list manually
> 3. Analyse a specific PR — provide the branch or PR number

If the user chooses option 1 or says nothing specific, use `--from-git`.

If they provide an explicit list, collect the paths.

### If the project has no Git diff available

`--from-git` works in **layers**, and the engine reports which one fired via
`change_detection_method` in the JSON output (`"git"`, `"mtime"`, or `"explicit"`):

1. `git diff --name-only <base>...HEAD` (PR-style diff against the base branch)
2. `git diff --name-only HEAD` + untracked files (uncommitted / staged / brand-new working-tree changes)
3. `git diff --name-only HEAD~1 HEAD` (most recent commit)
4. **Filesystem fallback** — if the folder is not a Git repository at all (no
   `.git`), Git is not installed, or none of steps 1–3 produced any files, the
   engine scans the repo for files modified within the last `--since-minutes`
   window (default `1440` = 24h) and uses those as the changed-file set.
5. If even the filesystem scan finds nothing, the script prints a warning and
   exits **without writing any reports**.

**Tell the user clearly** when the fallback was used — e.g.:

> "This project doesn't have a usable Git diff (no `.git` folder / no commits
> ahead of `main`), so I used files modified in the last 24 hours instead.
> For a precise result, tell me the exact files you changed and I'll re-run
> with `--changed-files`."

If step 5 happens (no files at all), ask the user for an explicit file list
and re-run with `--changed-files`.

---

## Step 2 — Ask for Output Location

> **"Where should I save the output files?"**
> 1. `./change-impact-output/` inside the current directory — *(recommended)*
> 2. Directly in the current directory
> 3. A specific path — type it

Map to `--output` flag:
- Option 1 / no answer → omit `--output`
- Option 2 → `--output .`
- Option 3 → `--output <user-supplied-path>`

---

## Step 3 — Run the Analysis Engine

The analysis script lives at `scripts/change_impact_skill.py`, **relative to this
SKILL.md file's own folder**. Resolve `<skill_dir>` from wherever you loaded this
file from — it is whichever of these exists in the current repository:

- `.claude/skills/change-impact-analysis/` (Claude Code)
- `.github/skills/change-impact-analysis/` (GitHub Copilot / Cursor)
- the repository root itself (this skill's own source repo)

**Check Python is available:**
```bash
python --version
```

**Run the engine** (substitute the resolved `<skill_dir>` below):

```bash
# Option 1 — auto-detect from git
python <skill_dir>/scripts/change_impact_skill.py \
  --from-git --base-branch main

# Option 2 — explicit file list
python <skill_dir>/scripts/change_impact_skill.py \
  --changed-files src/api/users.py src/models/user.py src/services/auth.py

# Option 3 — custom output directory
python <skill_dir>/scripts/change_impact_skill.py \
  --from-git --base-branch main --output ./reports/

# Get raw JSON to stdout (for piping / CI integration)
python <skill_dir>/scripts/change_impact_skill.py \
  --from-git --json-only
```

**If the script is not found at any of the candidate paths**, run
`file_search`/`Glob` for `change_impact_skill.py` in the repo before falling
back to [Manual Fallback](#manual-fallback) — do not guess a path.

Wait for the script to complete.  Output files produced:

| File | Description |
|------|-------------|
| `impact_report.md` | **Primary artifact** — full structured impact report |
| `impact_analysis.json` | Machine-readable result (CI/CD integration) |
| `deployment_checklist.md` | Ready-to-use pre/post deployment checklist |

**If Python or the script is missing**, proceed to [Manual Fallback](#manual-fallback).

---

## Step 4 — Read the Analysis Data

Read the generated files:
```
{output_dir}/impact_report.md
{output_dir}/impact_analysis.json
```

Key fields in `impact_analysis.json` to study:

```json
{
  "impact": {
    "changed_files":           [...],   // normalised paths of changed files
    "impacted_modules":        [...],   // every affected module with type + proximity
    "impacted_apis":           [...],   // API endpoint files in the blast radius
    "regression_areas":        [...],   // high-risk areas to regression-test
    "required_test_suites":    [...],   // unit / integration / e2e suites needed
    "consumer_apps":           [...],   // downstream applications affected
    "direct_impact_count":     N,
    "transitive_impact_count": N
  },
  "contract_violations": [...],         // OpenAPI / GraphQL / Protobuf violations
  "risk": {
    "score":   N,                       // 0–100
    "level":   "LOW|MEDIUM|HIGH|CRITICAL",
    "action":  "...",
    "factors": [...]                    // per-factor breakdown
  }
}
```

Also read:
- [`references/dependency-analysis.md`](references/dependency-analysis.md) — graph algorithm reference
- [`references/risk-scoring.md`](references/risk-scoring.md) — risk factor reference

---

## Step 5 — Provide AI Analysis (You Are the AI Engine)

Think like a senior release engineer who reviewed the complete blast radius.
Produce four AI-quality sections:

---

### 5a — Impact Summary

Write a crisp executive summary (3–5 sentences):
- What changed and why it matters for this release
- Highest-risk modules and why
- Whether this deployment should proceed as-is, needs monitoring, or should be blocked
- One-line recommendation for the release manager

---

### 5b — Blast Radius Explanation

For each **directly changed file**:
1. What does this module do?
2. Which other modules depend on it (transitive chain)?
3. Is there a test that covers this path?
4. What is the worst-case failure mode if this change is faulty?

For the **top 3 highest-risk transitively affected modules**, explain:
- Why they are affected (import chain)
- What would break if the change is incorrect
- Who owns it (from CODEOWNERS / ownership map)

---

### 5c — API Contract Assessment

For each contract violation detected:
1. **What changed** — endpoint / field / type affected
2. **Who is impacted** — which consumers use this endpoint
3. **Migration path** — how consumers should adapt
4. **Recommended action** — deprecate gracefully / block deployment / coordinate release

If no violations: confirm that the API surface is stable and consumers are safe.

---

### 5d — Release Recommendation

Provide a concrete, structured recommendation:

**Verdict:** `PROCEED` / `PROCEED WITH MONITORING` / `BLOCK — REQUIRES REVIEW`

**Rationale:** (2–3 sentences linking the risk score to the specific changes)

**Before deploying:**
- (numbered list of required actions)

**After deploying:**
- (numbered list of verification steps)

**Rollback trigger:** describe the exact condition that should trigger a rollback

---

## Step 6 — Output AI Analysis in Chat

Present the complete analysis in structured markdown:

```
---
## Impact Summary
[Section 5a]

---
## Blast Radius Explanation
[Section 5b]

---
## API Contract Assessment
[Section 5c]

---
## Release Recommendation
[Section 5d]
```

---

## Step 7 — Write AI Content Into Report File

**Do NOT ask** — automatically update the report immediately after the analysis.

Locate the report:
- Default: `./change-impact-output/impact_report.md`
- Custom path: `{output_dir}/impact_report.md`

Append a new section `## AI Release Analysis` at the end of the report containing
all four AI sections.  Use `insert_edit_into_file` to append, or `create_file` to
overwrite if simpler.

Print confirmation:
```
[ok] AI analysis appended to: {report_path}
```

---

## Step 8 — Report Completion

```
Change Impact Analysis complete [ok]

Repository   : {repo_path}
Base branch  : {base_branch}
Changed files: {N}

Risk Score   : {score}/100 — {level}
Action       : {action}

Impact
  Direct modules     : {direct_count}
  Transitive modules : {transitive_count}
  Impacted APIs      : {api_count}
  Consumer apps      : {consumer_count}

Output files in {output_dir}:
  impact_report.md          ← open this first
  impact_analysis.json
  deployment_checklist.md

AI engine: {agent_name} (no separate API key required)
```

---

## Manual Fallback (Script Not Found)

If `change_impact_skill.py` is not found or Python is unavailable:

1. List all source files in the repository:
   ```bash
   git diff --name-only main...HEAD
   ```
   Or ask the user to provide the changed files.

2. For each changed file, use `grep_search` to find all files that import it:
   ```
   Pattern: import.*{module_name}|require.*{module_name}|from.*{module_name}
   ```

3. Repeat for each newly found file (manual BFS, up to 3 hops).

4. Use `file_search` to find `CODEOWNERS` and map files to owners.

5. Use `file_search` to find `openapi.yaml`, `swagger.json`, `*.graphql` for contract checks.

6. Manually calculate risk score using the table in
   [`references/risk-scoring.md`](references/risk-scoring.md).

7. Use [`templates/impact_report.md`](templates/impact_report.md) to produce the report.

8. Write the report to `./impact_report.md`.

9. Continue with Steps 5–8.

---

## Notes

- **No API key required** — the host coding agent (Claude Code / Copilot / Cursor) is the AI engine
- **Deterministic** — given the same inputs the score is always the same
- **Polyglot** — supports Python, JS/TS, Java, C#, Go import graphs
- **CODEOWNERS** — automatically maps every affected file to its owner
- **Contract detection** — OpenAPI, Swagger, GraphQL schema, Protobuf
- **CI/CD ready** — `--json-only` flag emits structured JSON to stdout
- **No-Git fallback** — `--from-git` degrades to a filesystem mtime scan
  (`--since-minutes`, default 1440) when there's no `.git` directory, Git
  isn't installed, or `git diff` returns nothing; check
  `change_detection_method` in the JSON output (`git` / `mtime` / `explicit`)
- **Script path** — resolve relative to this file's own folder (see Step 3);
  never hardcode a single platform's install path
