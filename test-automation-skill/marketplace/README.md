# Test Automation & QA Skill Suite

A complete agent skill suite for the **Testing, BDD & QA Automation** phase of the SDLC.

| Skill | Description | Output |
| :--- | :--- | :--- |
| **`test-design-generator`** | Systematic test matrices covering positive, negative, and edge boundaries | `test_design_matrix.md` |
| **`test-data-generator`** | Contextually valid synthetic mock datasets (JSON, CSV, SQL) | `mock_data.json` / `.csv` |
| **`gherkin-generator`** | Given-When-Then BDD scenarios aligned with acceptance criteria | `features/*.feature` |
| **`playwright-test-generator`** | Robust Playwright E2E browser test automation suites | `tests/*.spec.ts` |
| **`playwright-test-executor`** | Headless/UI test runner with automated trace failure triage | `playwright-report/` |

---

## 🚀 Quick Installation

```bash
# Claude Code:
cp -r skill/* ~/.claude/skills/

# Cursor:
cp -r skill/* .cursor/skills/
```
