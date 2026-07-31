# QuickStart

Get from zero to your first impact report in under five minutes.

---

## 1. Copy the skill into your project

```bash
mkdir -p .claude/skills
cp -r skill/change-impact-analysis .claude/skills/change-impact-analysis
```

Your project should now look like:

```
your-project/
└── .claude/
    └── skills/
        └── change-impact-analysis/
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

(GitHub Copilot and Cursor users: use `.github/skills/` instead — same folder, same
contents. Cursor also needs a small `.cursor/rules/change-impact-analysis.mdc` rule; see
[README.md](README.md).)

## 2. Check Python is available

```bash
python --version
```

Needs 3.8+. No `pip install` required for the core engine — PyYAML is only needed if you
want YAML-format OpenAPI specs validated (JSON specs always work without it).

## 3. Open your AI assistant's chat

Claude Code, GitHub Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`), or Cursor — all work the
same way.

## 4. Ask for an impact analysis

```
Analyse the change impact for this PR
```
or, if the repo has no Git history to diff against:
```
Run change impact analysis for: src/api/users.py src/models/user.py
```

## 5. Answer one question

Your assistant asks how to identify changed files (auto-detect from git is the default)
and where to save output. Press Enter to accept the defaults.

## 6. Read the report

Open `impact_report.md` first — it has the risk score, blast radius, and release
recommendation all in one place.

---

## What you get, every run

| File | Purpose |
|------|---------|
| `impact_report.md` | The full report — read this first |
| `impact_analysis.json` | Machine-readable result (CI/CD integration) |
| `deployment_checklist.md` | Pre/post deploy sign-off checklist |

A worked example of all three is in [SampleOutputs/](SampleOutputs/).

---

## Next steps

- Try the prompt variations in [SamplePrompts.md](SamplePrompts.md)
- See how the pipeline works under the hood in [Architecture.png](Architecture.png)
- Full CLI reference, risk-scoring formula, and troubleshooting in [UserGuide.pdf](UserGuide.pdf)
- Run [`requirement-analysis-skill`](../../Requirement-analysis-skill/) **before** you
  write code next time, to plan the change before assessing its impact
