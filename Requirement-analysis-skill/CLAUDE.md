# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Requirement Analysis Skill** — a deterministic pre-development planning engine for AI agents. Given a free-text feature/change request, it identifies which files to update, exact code locations, existing patterns to follow, and applicable security/compliance/formatting rules.

- **Polyglot**: Python, JavaScript/TypeScript, Java, C#, Go
- **Deterministic**: identical input → identical output (no randomness, no LLM calls in the engine)
- **Zero dependencies**: Python 3.8+ standard library only, no external packages
- **Offline**: no API keys or network calls required
- **Paired with**: [`change-impact-analysis-skill`](../change-impact-analysis-skill/marketplace/README.md) (runs *after* implementation to assess blast radius)

## Common Commands

### Standalone CLI Usage

```bash
# Analyze a requirement (writes to ./requirement-analysis-output/)
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add a discount_code field to the Order model and expose it on the orders API"

# Custom output directory
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
  --repo-path /path/to/repo \
  --requirement "Fix the login endpoint to reject expired tokens" \
  --output ./reports/

# JSON only (stdout, no files written)
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add dark mode toggle to the settings page" --json-only

# Return more candidates (default: 5)
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "Add rate limiting to all public API endpoints" --top-n 10
```

### Testing Individual Engines

Each engine module can be tested independently; they import only Python stdlib:

```bash
cd skill/requirement-analysis
python -c "
from scripts.engine.requirement_parser import RequirementParser
intent = RequirementParser.parse('Add a discount field to the Order model')
print(intent)
"
```

## Architecture

```
Free-text requirement
        │
        ▼
  Requirement Parser    → action, target_types, entities, domain_tags
        │
        ▼
  Codebase Indexer      → List[FileIndex] with paths, languages, symbols, tokens
        │
        ▼
  Location Resolver     → ranked candidate files + exact symbol/line suggestions
        │
        ▼
  Pattern Finder        → existing implementation as template (for "add" actions)
        │
        ▼
  Security Compliance   → rule-table-based checklist
  Checker               │
        │
        ▼
  Formatting Analyzer   → detected formatter/linter + per-file style sample
        │
        ▼
  Plan Generator        → implementation_plan.md + requirement_analysis.json
```

Each stage is **pure Python**, deterministic, and runs offline — there are no LLM calls in the engine itself. The host AI agent (Claude Code, Copilot, Cursor) reads the final JSON/Markdown and adds narrative.

### Key Modules

| Module | Purpose |
|--------|---------|
| `requirement_parser.py` | Extracts action (add/modify/remove/fix), target types (api_endpoint/database/service/ui_component/config/test), entities (extracted identifiers), and domain tags (security_sensitive/financial_critical/pii_data/external_integration). Uses regex + keyword matching. |
| `codebase_indexer.py` | Walks repo, builds file + symbol index via AST (Python, Go) or line-by-line regex (JS/TS, Java, C#). Detects module type (test/database/config/ui_component/api_endpoint/service/library/module). Extracts function/class/route symbols with line numbers. |
| `location_resolver.py` | **Core scoring engine**. Ranks files by additive scoring (path token matches, symbol matches, module_type relevance, domain tags, content hits). Returns top N candidates with match reasons. Also suggests new file if no existing file scores high. |
| `pattern_finder.py` | For "add" actions, finds an existing implementation of the target type to use as a structural template. Returns reference file/symbol/line. |
| `security_compliance_checker.py` | Rule-table-based checklist. Merges rules from target type, domain tags, action, and baseline rules. Dedupes and sorts by category (security/compliance/standard). See `skill/requirement-analysis/references/security-compliance-rules.md` for full rule table. |
| `formatting_analyzer.py` | Detects formatter/linter configs (Black, isort, Ruff, Prettier, ESLint, etc.). Samples indent, quote style, and line endings from each candidate file. |
| `plan_generator.py` | Renders Markdown report + JSON. Markdown is human-readable, JSON is machine-readable for CI/CD or further tooling. |

### Determinism Guarantees

All dict/set iteration is explicitly sorted; file-walk order doesn't affect final ranking (scores are re-sorted). No randomness or external network calls. **Same requirement text + same repo state = byte-identical output (modulo timestamp).**

## Key Design Decisions

### Entity Variant Normalization

Entities extracted from the requirement are normalized into variant sets so that `discount_code`, `discountCode`, `DiscountCode`, and `discount-code` all match each other. This allows the skill to find files regardless of the codebase's naming convention.

### Scoring Formula

Pure additive; no early termination. Bonus for path tokens, symbol names, module-type relevance, domain keywords, and content matches. Constants are in `location_resolver.py:_score_file()`.

### Module Type Detection

Fixed precedence (first match wins): test → database → config → ui_component → api_endpoint (by content) → path-keyword heuristics (controller/service/util) → language → other. **This precedence is identical to `change-impact-analysis-skill`'s `impact_analyzer.py`, so both skills agree on file roles.**

### Action Parsing

All action patterns across all categories are matched in the lowercased text; the action whose match has the **earliest position** in the text wins. This prevents misclassification when multiple action keywords appear — e.g., "Add a risk factor for deprecated dependencies" correctly parses as `action="add"` even though "deprecated" would match a `remove` pattern.

### Polyglot Symbol Extraction

- **Python**: uses `ast.parse()` + `ast.walk()` for exact syntax
- **JS/TS, Java, C#, Go**: line-by-line regex (no external parser dependency)
- Routes detected via `_ROUTE_PATTERNS` with `(HTTP method, path)` capture groups across Flask/FastAPI, Express, Spring, ASP.NET

## Output Format

### `implementation_plan.md` (Human-Readable)

Sections: Requirement → Parsed Intent → Files To Update (per-file suggestions + matched symbols) → New File Suggestion (if applicable) → Pattern To Follow → Security & Compliance Checklist (grouped by category) → Formatting & Linting Commands → Next Steps

### `requirement_analysis.json` (Machine-Readable)

```json
{
  "repo_path": "string",
  "intent": {
    "raw_text": "...",
    "action": "add|modify|remove|fix",
    "target_types": ["api_endpoint", ...],
    "entities": ["OrderService", ...],
    "domain_tags": ["financial_critical", ...]
  },
  "location": {
    "candidates": [
      {
        "path": "src/models/order.py",
        "module_type": "database",
        "score": 28,
        "match_reasons": ["path token match", ...],
        "matched_symbols": [
          {"name": "Order", "kind": "class", "line": 12, "detail": ""}
        ],
        "suggestion": "Add the new logic near existing related symbol(s): Order (class @ line 12)."
      }
    ],
    "new_file_suggestion": null
  },
  "pattern": {
    "reference_file": "src/api/orders.py",
    "reference_symbol": {...},
    "note": "Follow this existing route as a template..."
  },
  "security_compliance": [
    {"category": "security", "item": "Validate and sanitize all input parameters", "reference": "OWASP ASVS V5"}
  ],
  "formatting": {
    "detected_tools": [
      {"config_file": "pyproject.toml", "tool": "Black / isort / Ruff (Python)", "command": "black . && isort . && ruff check --fix ."}
    ],
    "candidate_file_styles": {
      "src/models/order.py": {"indent": "spaces:4", "quote_style": "double", "line_ending": "LF"}
    }
  }
}
```

## Known Limitations (v1)

1. **No file suggestion if repo has no files of the target type** — by design (won't fabricate conventions for types that don't exist in the repo).
2. **Entity extraction is regex-based** — multi-word natural-language phrases ("the user's shipping address") won't extract; use identifier-style names or quotes.
3. **Pattern finder only for `action == "add"` with target types that have templates** — api_endpoint, database, service, ui_component.
4. **Content-match scoring reads scoring-positive files in full** — minor I/O overhead on very large repos, but still sub-second for typical sizes.

## Deployment & CI/CD

This skill is designed for interactive planning, not gating — but the JSON output is stable enough to script:

```bash
# Example: auto-generate issue checklist from JSON
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
  --requirement "$ISSUE_BODY" --json-only \
  | jq '.security_compliance'
```

## Integration with Claude Code

When used as a Claude Code skill (in `.claude/skills/requirement-analysis/`):
1. Claude Code auto-discovers `SKILL.md`
2. User triggers via natural language ("I want to add...", "Plan this change", etc.)
3. Claude reads `SKILL.md` workflow steps, runs the Python engine, reads output
4. Claude narrates the plan with its own judgment and recommendations
5. Output files land in `./requirement-analysis-output/` by default (user-configurable)

## Testing & Validation

No unit test suite currently committed (v1.0.0). To validate a change:

1. **Manual CLI test**: run the engine on this repo with a test requirement, verify JSON/Markdown are sensible
2. **Regex correctness**: test entity/action/target-type patterns against edge cases (mixed case, multiple keywords, etc.)
3. **Symbol extraction**: add test cases in a target language (e.g., Python class with decorator route) and verify AST/regex extraction
4. **Determinism**: run the same requirement twice, diff the JSON — should be identical except timestamp

## References

- `skill/requirement-analysis/references/requirement-mapping.md` — action/target-type/domain keyword dictionaries + scoring formula
- `skill/requirement-analysis/references/security-compliance-rules.md` — full security/compliance rule table with citations (OWASP, PCI-DSS, etc.)
- `skill/requirement-analysis/SKILL.md` — agent workflow for Claude Code / Copilot / Cursor
- `marketplace/README.md` — user-facing overview and setup instructions
- `marketplace/UserGuide.pdf` — complete technical deep-dive on every module and algorithm, CLI reference, and troubleshooting
