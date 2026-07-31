# Sample Prompts

Copy-paste prompts to try in GitHub Copilot Chat once the skill is installed. Grouped by what
you're trying to learn about a codebase.

---

## Remote repositories

```
Reverse engineer https://github.com/django/django
```
```
Analyze this repo: https://github.com/nopSolutions/nopCommerce
```
```
Reverse engineer https://github.com/owner/repo and save it to C:\Reports
```

## Local projects

```
Reverse engineer this project
```
```
Analyze the codebase in C:\Projects\LegacyApp
```
```
Document the folder I'm in
```
```
Reverse engineer ./my-app and save to ../my-app-analysis
```

## Targeting a specific section of the report

The skill always produces all four sections, but you can steer the conversation once the
report is generated:

```
What does this codebase do, in plain English?
```
```
Explain the system design and architecture of this repo
```
```
What auth model does this project use — RBAC, ABAC, or ReBAC?
```
```
Extract the business logic and core workflows from this app
```
```
Show me how this web app navigates, screen by screen
```
```
What are the biggest tech-debt risks visible in this codebase?
```

## Choosing where output goes

```
Reverse engineer https://github.com/owner/repo — save in the current folder
```
```
Reverse engineer this project — save to ../legacyapp-analysis
```

## Framework-specific navigation questions

```
Walk me through the screen flow of this ASP.NET Web Forms app
```
```
Map the navigation for this React SPA, including protected routes
```
```
What Razor views exist and how does the user move between them?
```

---

## Tips

- You don't need to say "using reverse-engineering-skill" — the description in `SKILL.md`
  triggers automatically on phrases like "reverse engineer", "analyze this repo/codebase",
  "explain the system design", or any `github.com` URL.
- For local folders, mention "this project" or give an explicit path — both work.
- Re-running on the same target is safe; it re-analyzes and overwrites the previous report.
