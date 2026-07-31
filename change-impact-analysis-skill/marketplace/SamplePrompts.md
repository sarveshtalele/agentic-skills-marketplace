# Sample Prompts

Copy-paste prompts to try once the skill is installed. Grouped by what you're trying to
learn before you deploy.

---

## Analyzing a PR or branch

```
Analyse the change impact for this PR
```
```
I'm about to merge my feature branch. Can you do a change impact analysis?
```
```
Run change impact analysis --from-git --base-branch develop
```

## Explicit file lists (no usable git diff)

```
Run change impact analysis for: src/api/users.py src/models/user.py
```
```
What breaks if I change src/db/migrations/0042_users.sql?
```

## Risk and release questions

```
What is the deployment risk score for my changes?
Is it safe to deploy?
What is the blast radius of this change?
```

## Testing and ownership

```
What tests do I need to run before deploying?
Who owns the code I just changed? I need to notify them before deploying.
```

## API contracts

```
What APIs are broken by my changes?
Are there any breaking changes to the OpenAPI spec?
```

## Controlling output

```
Analyse the change impact and save the report to ./reports/
Give me the raw JSON only, no files written
```

---

## Tips

- You don't need to say "using change-impact-analysis" — the description in `SKILL.md`
  triggers automatically on phrases like "change impact", "deployment risk", "blast
  radius", "safe to deploy", or a list of changed files with "what will break".
- `--from-git` works even without a clean PR diff — it falls back through
  uncommitted changes, the last commit, and finally a filesystem mtime scan. The agent
  will tell you which method fired (`git` vs. `mtime`); if it's `mtime`, provide an
  explicit file list for a precise result.
- Run this **after** implementing a change planned by
  [`requirement-analysis-skill`](../../Requirement-analysis-skill/) to complete the
  plan → implement → impact-analyze pipeline.
