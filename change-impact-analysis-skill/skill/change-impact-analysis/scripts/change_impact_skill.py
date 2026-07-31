#!/usr/bin/env python3
"""
Change Impact Analysis Skill — CLI Entry Point

Usage
-----
# Explicit file list
python change_impact_skill.py --changed-files src/api/users.py src/models/user.py

# Auto-detect from git diff against base branch
python change_impact_skill.py --from-git --base-branch main

# Custom repo path and output directory
python change_impact_skill.py --repo-path /path/to/repo --from-git --output /tmp/impact
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from engine.graph_builder import DependencyGraphBuilder
from engine.impact_analyzer import ImpactAnalyzer
from engine.risk_scorer import RiskScorer
from engine.contract_validator import ContractValidator
from engine.ownership_parser import OwnershipParser
from engine.report_generator import ReportGenerator

_DIVIDER = "=" * 64


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Change Impact Analysis Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--repo-path", default=".",
        help="Root of the repository to analyse (default: current directory)",
    )
    p.add_argument(
        "--changed-files", nargs="+", metavar="FILE",
        help="Explicit list of changed file paths",
    )
    p.add_argument(
        "--from-git", action="store_true",
        help="Auto-detect changed files from `git diff --name-only <base>`",
    )
    p.add_argument(
        "--base-branch", default="main",
        help="Base branch for git diff (default: main)",
    )
    p.add_argument(
        "--since-minutes", type=int, default=1440,
        help=(
            "Fallback window (in minutes) used to detect changed files by file "
            "modification time when this is not a Git repository, Git is not "
            "installed, or `git diff` produces no result (default: 1440 = 24h)"
        ),
    )
    p.add_argument(
        "--output", default=None,
        help="Output directory (default: <repo-root>/change-impact-output/)",
    )
    p.add_argument(
        "--format", choices=["markdown", "json", "both"], default="both",
        help="Output format(s) to generate (default: both)",
    )
    p.add_argument(
        "--json-only", action="store_true",
        help="Emit the JSON result to stdout and exit (no files written)",
    )
    return p.parse_args()


def is_git_repo(repo_path: Path) -> bool:
    """Return True only if `git` is installed AND repo_path is inside a git work tree."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=repo_path, check=False,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def get_changed_files_from_git(repo_path: Path, base_branch: str) -> list:
    """
    Try, in order:
      1. `git diff --name-only <base>...HEAD`   (PR-style diff against base branch)
      2. `git diff --name-only HEAD`            (uncommitted / staged working-tree changes)
      3. `git diff --name-only HEAD~1 HEAD`     (most recent commit, if there is one)

    Returns an empty list if none of the above produce any files (e.g. a brand
    new repo with a single commit and a clean working tree, or `base_branch`
    does not exist).
    """
    # Tier 1: diff against base branch
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_branch}...HEAD"],
        capture_output=True, text=True, cwd=repo_path, check=False,
    )
    if result.returncode == 0:
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        if files:
            return files
    else:
        print(
            f"  [warn] git diff against '{base_branch}...HEAD' failed "
            f"(branch may not exist): {result.stderr.strip()}",
            file=sys.stderr,
        )

    # Tier 2: uncommitted / staged working-tree changes, plus new (untracked,
    # not-yet-`git add`ed) files — `git diff` alone never reports untracked
    # files, which would otherwise make brand-new files invisible to local
    # "what did I just change" runs.
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True, text=True, cwd=repo_path, check=False,
    )
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True, text=True, cwd=repo_path, check=False,
    )
    files += [f.strip() for f in untracked.stdout.splitlines() if f.strip()]

    if files:
        return sorted(set(files))

    # Tier 3: most recent commit (handles "I just committed, what changed?")
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True, cwd=repo_path, check=False,
    )
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    return files


def get_changed_files_by_mtime(repo_path: Path, since_minutes: int) -> list:
    """
    Filesystem-based fallback for repos with no usable git history.

    Returns every source file modified within the last `since_minutes`
    minutes. This is a heuristic (not deterministic across machines/clocks)
    and is only used when `git diff` cannot produce a result.
    """
    cutoff = time.time() - (since_minutes * 60)
    changed = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in DependencyGraphBuilder.IGNORE_DIRS and not d.startswith(".")]
        for name in files:
            full = Path(root) / name
            try:
                if full.stat().st_mtime >= cutoff:
                    changed.append(str(full.relative_to(repo_path)).replace("\\", "/"))
            except OSError:
                continue
    return sorted(changed)


def main() -> int:
    args = parse_args()
    repo_path = Path(args.repo_path).resolve()

    if not repo_path.exists():
        print(f"[error] Repository path not found: {repo_path}", file=sys.stderr)
        return 1

    # Resolve changed files
    detection_method = "explicit"
    if args.from_git:
        if is_git_repo(repo_path):
            changed_files = get_changed_files_from_git(repo_path, args.base_branch)
            detection_method = "git"
            if not changed_files:
                print(
                    "[info] git diff produced no changes (clean working tree, no "
                    f"commits ahead of '{args.base_branch}', and no prior commit "
                    "to diff)."
                )
                print(
                    f"[info] Falling back to filesystem scan: files modified in "
                    f"the last {args.since_minutes} minute(s) "
                    f"(adjust with --since-minutes)."
                )
                changed_files = get_changed_files_by_mtime(repo_path, args.since_minutes)
                detection_method = "mtime"
        else:
            print(
                f"[warn] 'git diff' is not available for '{repo_path}' - this is "
                "not a Git repository (no .git directory found) or Git is not "
                "installed."
            )
            print(
                f"[info] Falling back to filesystem scan: files modified in the "
                f"last {args.since_minutes} minute(s) "
                f"(adjust with --since-minutes)."
            )
            changed_files = get_changed_files_by_mtime(repo_path, args.since_minutes)
            detection_method = "mtime"

        if not changed_files:
            print(
                "[warn] No changed files could be detected automatically "
                "(git diff and filesystem scan both returned nothing)."
            )
            print(
                "[info] Re-run with an explicit file list instead, e.g.:\n"
                "       python change_impact_skill.py --changed-files "
                "path/to/file1.py path/to/file2.py"
            )
            return 0
    elif args.changed_files:
        changed_files = args.changed_files
    else:
        print("[error] Provide --changed-files <files...> or --from-git", file=sys.stderr)
        return 1

    output_dir = Path(args.output) if args.output else repo_path / "change-impact-output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.json_only:
        print(f"\n{_DIVIDER}")
        print("  CHANGE IMPACT ANALYSIS SKILL  v1.0.0")
        print(_DIVIDER)
        print(f"  Repository : {repo_path}")
        print(f"  Changed    : {len(changed_files)} file(s)  (detected via: {detection_method})")
        print(f"  Base branch: {args.base_branch}")
        print(f"  Output     : {output_dir}")
        print(_DIVIDER)

    # ── Phase 1: Build dependency graph ───────────────────────────────
    _step(1, 5, "Building dependency graph", args.json_only)
    graph_builder = DependencyGraphBuilder(repo_path)
    dep_graph = graph_builder.build()
    _log(f"Nodes: {len(dep_graph.nodes)}, Edges: {sum(len(v) for v in dep_graph.edges.values())}", args.json_only)

    # ── Phase 2: Parse ownership metadata ────────────────────────────
    _step(2, 5, "Parsing ownership metadata", args.json_only)
    ownership_parser = OwnershipParser(repo_path)
    ownership_map = ownership_parser.parse()

    # ── Phase 3: Validate API contracts ──────────────────────────────
    _step(3, 5, "Validating API contracts", args.json_only)
    contract_validator = ContractValidator(repo_path, args.base_branch)
    contract_violations = contract_validator.validate()
    _log(f"Violations found: {len(contract_violations)}", args.json_only)

    # ── Phase 4: Analyze change impact ───────────────────────────────
    _step(4, 5, "Analysing change impact", args.json_only)
    impact_analyzer = ImpactAnalyzer(dep_graph, ownership_map, repo_path)
    impact = impact_analyzer.analyze(changed_files)
    _log(
        f"Direct: {impact['direct_impact_count']}, Transitive: {impact['transitive_impact_count']}",
        args.json_only,
    )

    # ── Phase 5: Calculate risk score ────────────────────────────────
    _step(5, 5, "Calculating deployment risk score", args.json_only)
    risk_scorer = RiskScorer()
    risk_result = risk_scorer.score(impact, contract_violations)

    # ── Assemble result ───────────────────────────────────────────────
    result = {
        "repo_path": str(repo_path),
        "base_branch": args.base_branch,
        "change_detection_method": detection_method,
        "impact": impact,
        "contract_violations": contract_violations,
        "risk": risk_result,
    }

    # ── JSON-only mode ────────────────────────────────────────────────
    if args.json_only:
        print(json.dumps(result, indent=2, default=str))
        return 0

    # ── Write output files ────────────────────────────────────────────
    print("\n  Generating reports...")
    report_gen = ReportGenerator(output_dir)

    paths = {}
    if args.format in ("markdown", "both"):
        paths["report"] = report_gen.generate_markdown(result)
        print(f"  [ok] Impact Report   : {paths['report']}")

    if args.format in ("json", "both"):
        paths["json"] = report_gen.generate_json(result)
        print(f"  [ok] Analysis JSON   : {paths['json']}")

    paths["checklist"] = report_gen.generate_checklist(result)
    print(f"  [ok] Deploy Checklist: {paths['checklist']}")

    # ── Summary ───────────────────────────────────────────────────────
    score = risk_result["score"]
    level = risk_result["level"]
    bar = _risk_bar(score)

    print(f"\n{_DIVIDER}")
    print(f"  RISK SCORE  {score:3d}/100  {bar}  {level}")
    print(f"  Action      {risk_result['action']}")
    print(f"  APIs        {len(impact['impacted_apis'])} endpoint(s) affected")
    print(f"  Modules     {impact['direct_impact_count']} direct | {impact['transitive_impact_count']} transitive")
    print(f"  Consumers   {len(impact['consumer_apps'])} application(s)")
    print(f"  Contracts   {len(contract_violations)} violation(s)")
    print(_DIVIDER + "\n")

    return 0


def _step(n: int, total: int, label: str, silent: bool) -> None:
    if not silent:
        print(f"[{n}/{total}] {label}...")


def _log(msg: str, silent: bool) -> None:
    if not silent:
        print(f"      {msg}")


def _risk_bar(score: int) -> str:
    filled = score // 10
    return "[" + "#" * filled + "." * (10 - filled) + "]"


if __name__ == "__main__":
    sys.exit(main())
