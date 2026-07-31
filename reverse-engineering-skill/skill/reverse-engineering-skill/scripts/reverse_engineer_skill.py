#!/usr/bin/env python3
"""
Reverse Engineer Skill — Entry Point (GitHub Copilot Agent Skill)

Skill location: .github/skills/reverse-engineering-skill/scripts/
Run via SKILL.md instruction or directly:
    python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py <url>
=====================================
Analyzes any public GitHub repository OR an existing project already on your
local disk, and generates four professional output files. The default and
recommended mode is **pure static analysis** — no API keys, no LLM accounts,
no internet access beyond git clone (and no internet at all for local
projects).

Usage:
    python reverse_engineer_skill.py <github-repo-url | local-folder-path>
        [--heuristic | --ai] [--output <dir>] [--help]

Examples (remote — shallow-cloned to a temp dir, analyzed, then deleted):
    python reverse_engineer_skill.py https://github.com/nopSolutions/nopCommerce
    python reverse_engineer_skill.py https://github.com/spring-projects/spring-petclinic
    python reverse_engineer_skill.py https://github.com/django/django

Examples (local — analyzed in place, nothing cloned or deleted):
    python reverse_engineer_skill.py C:/Projects/my-legacy-app
    python reverse_engineer_skill.py ./my-project
    python reverse_engineer_skill.py .

Output files (in ./{repo_name}/ by default, or --output <dir>):
    {repo_name}_sdd.json        — System Design Document (JSON, all sections)
    {repo_name}_report.md       — 4-section focused report (primary artifact)
    {repo_name}_evaluation.md   — Automated quality score (100-point)
    manifest.json               — Run record with metrics and file sizes

    No SVG diagrams or HTML dashboard are generated — the dependency graph
    and navigation flow render as Mermaid diagrams directly inside
    {repo_name}_report.md, so it displays natively on GitHub, GitLab, and
    the VS Code preview pane with no extra files to open.

Report sections:
    1. System Design Overview      — architecture, metrics, dependencies, data model
    2. Authentication & Access Control — RBAC / ABAC / ReBAC detection
    3. Business Logic Extractor    — domain, workflows, rules, entity glossary
    4. Screen-by-Screen Navigation — end-to-end UI journey and screen inventory

Output options:
    (no flag)       — creates ./{repo_name}/ folder in current directory
    --output .      — writes directly to current directory
    --output <dir>  — writes to the specified directory

Analysis modes:
    --heuristic     — (default, recommended) pure static-heuristic analysis.
                      No API key, no LLM account, no `anthropic` package
                      required.
    --ai            — optional: calls the Claude API directly for richer
                      executive-summary / roadmap / business-logic narrative
                      instead of the static heuristics. Requires the
                      ANTHROPIC_API_KEY environment variable and the
                      `anthropic` Python package (see assets/requirements.txt).
                      Falls back to --heuristic automatically if the key or
                      package is missing, or if the API call fails.
    --no-ai         — synonym for --heuristic.
    (no flag)       — prompts interactively to choose [1] Heuristic or
                      [2] AI-powered; defaults to Heuristic on Enter/EOF.

How AI narrative works when using --heuristic (NO API key required):
    All analysis — executive summary, architecture pattern, business domain,
    modernisation roadmap — is produced by pure static code heuristics:
    class/method naming conventions, ORM entity detection, import analysis,
    and API route extraction. No LLM is called by the Python script in this
    (default) mode.

    To get AI-powered narrative on top of the static results, without using
    --ai / an Anthropic API key:
      • Claude Code   : run /reverse-engineer <url> — Claude reads the
                        output files and provides AI explanation in chat.
      • GitHub Copilot: use the prompt in .github/prompts/reverse-engineer.prompt.md
                        — Copilot reads the SDD JSON and provides AI narrative.
      • Any other LLM : open the generated *_report.md or *_sdd.json and ask
                        your preferred AI to explain or enhance the content.
"""

import sys
import io
import os

# Ensure 'engine/' is resolved relative to THIS file, not the caller's CWD.
# This allows running the script from the workspace root:
#   python .github/skills/reverse-engineering-skill/scripts/reverse_engineer_skill.py <url>
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# Force UTF-8 output on Windows so print() never raises UnicodeEncodeError
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from engine.pipeline import run_pipeline

_HELP = __doc__


def _ask_mode(args: list) -> str:
    """Ask the user to choose analysis mode, unless overridden by a CLI flag.

    Returns:
        ``"ai"`` or ``"heuristic"``.
    """
    if "--ai" in args:
        return "ai"
    if "--heuristic" in args or "--no-ai" in args:
        return "heuristic"

    print()
    print("  ┌──────────────────────────────────────────────┐")
    print("  │  Select Analysis Mode                        │")
    print("  ├──────────────────────────────────────────────┤")
    print("  │  [1] Heuristic-only  (fast, no API key)      │")
    print("  │  [2] AI-powered      (Claude API, richer)    │")
    print("  └──────────────────────────────────────────────┘")
    print()
    try:
        choice = input("  Enter choice [1]: ").strip() or "1"
    except EOFError:
        choice = "1"
        print()
    except KeyboardInterrupt:
        print()
        raise

    if choice not in ("1", "2"):
        print(f"  [!] Invalid choice '{choice}' — defaulting to [1] Heuristic.\n")
        choice = "1"

    if choice == "2":
        import os
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print()
            print("  [!] ANTHROPIC_API_KEY environment variable not set.")
            print("      Set it with:  set ANTHROPIC_API_KEY=sk-ant-...")
            print("      Falling back to heuristic mode.\n")
            return "heuristic"
        try:
            import anthropic  # noqa: F401
        except ImportError:
            print()
            print("  [!] 'anthropic' package not installed.")
            print("      Install with:  pip install anthropic")
            print("      Falling back to heuristic mode.\n")
            return "heuristic"
        print()
        return "ai"
    print()
    return "heuristic"


def main() -> None:
    """CLI entry point. Parses arguments and starts the pipeline."""
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(_HELP)
        sys.exit(0 if args else 1)

    # Extract URL or local path (first positional arg — ignore flag arguments)
    repo_url = next((a for a in args if not a.startswith("--")), None)
    if not repo_url:
        print("Error: No GitHub URL or local folder path provided.\n")
        print("Usage: python reverse_engineer_skill.py <github-repo-url | local-folder-path>")
        sys.exit(1)

    mode = _ask_mode(args)

    # Resolve --output <dir> flag
    output_dir = None
    for i, a in enumerate(args):
        if a in ("--output", "-o") and i + 1 < len(args):
            output_dir = args[i + 1]
            break
        if a.startswith("--output="):
            output_dir = a.split("=", 1)[1]
            break

    try:
        run_pipeline(repo_url, mode=mode, output_dir=output_dir)
    except ValueError as e:
        print(f"\nError: {e}\n")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nError: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
