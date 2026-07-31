# QuickStart

Get from zero to your first report in under five minutes.

---

## 1. Copy the skill into your project

```bash
mkdir -p .github/skills
cp -r skill/reverse-engineering-skill .github/skills/reverse-engineering-skill
```

Your project should now look like:

```
your-project/
└── .github/
    └── skills/
        └── reverse-engineering-skill/
            ├── SKILL.md
            ├── manifest.yaml
            ├── scripts/
            ├── assets/
            ├── references/
            └── templates/
```

## 2. Check Python is available

```bash
python --version
```

Needs 3.8+. No `pip install` required — the analyzer uses only the standard library.

## 3. Open GitHub Copilot Chat

`Ctrl+Alt+I` (Windows/Linux) or `Cmd+Alt+I` (Mac).

## 4. Ask it to reverse engineer something

**A GitHub repo:**
```
Reverse engineer https://github.com/django/django
```

**The project you're already sitting in:**
```
Reverse engineer this project
```

**A folder on disk:**
```
Analyze the codebase in C:\Projects\LegacyApp
```

## 5. Answer one question

Copilot asks where to save the output. Press Enter to accept the default
(`./{repo-name}/` in your current directory), or type a different path.

## 6. Read the report

Open `{repo-name}_report.md` first — it's the single self-contained artifact with all four
sections (System Design, Auth, Business Logic, Screen Navigation) and Mermaid diagrams that
render natively in GitHub, GitLab, and the VS Code preview pane.

---

## What you get, every run

| File | Purpose |
|------|---------|
| `{repo}_report.md` | The 4-section report — read this first |
| `{repo}_sdd.json` | Full System Design Document (machine-readable) |
| `{repo}_evaluation.md` | 100-point quality score for the analysis itself |
| `manifest.json` | Run metrics (files analyzed, classes, methods, endpoints) |

A worked example of all four is in [SampleOutputs/](SampleOutputs/).

---

## Next steps

- Try the prompt variations in [SamplePrompts.md](SamplePrompts.md)
- See how the pipeline works under the hood in [Architecture.png](Architecture.png)
- Full CLI reference and troubleshooting in [UserGuide.pdf](UserGuide.pdf)
