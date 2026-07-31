# QuickStart

Get from zero to your first implementation plan in under two minutes.

---

## 1. Copy the skill into your project

```bash
mkdir -p .claude/skills
cp -r skill/requirement-analysis .claude/skills/requirement-analysis
```

Your project should now look like:

```
your-project/
└── .claude/
    └── skills/
        └── requirement-analysis/
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

(GitHub Copilot and Cursor users: use `.github/skills/` or `.cursor/skills/` instead —
same folder, same contents.)

## 2. Check Python is available

```bash
python --version
```

Needs 3.8+. No `pip install` required — the engine uses only the standard library.

## 3. Open your AI assistant's chat

Claude Code, GitHub Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`), or Cursor — all work the
same way.

## 4. Describe what you want to build

```
I want to add a discount_code field to the Order model and expose it on the orders API
```

Mention concrete names (class names, field names, file names) if you know them — it
sharply improves the match quality.

## 5. Answer one question

Your assistant asks where to save the output. Press Enter to accept the default
(`./requirement-analysis-output/`), or type a different path — or say "don't save,
just show me" for JSON-only mode.

## 6. Read the plan

Open `implementation_plan.md` first — it lists the exact files to change, the pattern
to follow, and the security/compliance checklist, all in one place.

---

## What you get, every run

| File | Purpose |
|------|---------|
| `implementation_plan.md` | The plan — read this first |
| `requirement_analysis.json` | Machine-readable result (parsed intent, candidates, checklist, formatting) |

A worked example of both is in [SampleOutputs/](SampleOutputs/).

---

## Next steps

- Try the prompt variations in [SamplePrompts.md](SamplePrompts.md)
- See how the pipeline works under the hood in [Architecture.png](Architecture.png)
- Full CLI reference, JSON schema, and troubleshooting in [UserGuide.pdf](UserGuide.pdf)
- Once you've implemented the change, run
  [`change-impact-analysis-skill`](../../change-impact-analysis-skill/) on the modified
  files to check the deployment risk before you merge
