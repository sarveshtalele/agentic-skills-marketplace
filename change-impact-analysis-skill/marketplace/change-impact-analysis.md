# Scorecard: `change-impact-analysis`

**Overall Quality Score**: `95.8/100`  
**Evaluation Status**: **✅ PASS**  
**Evaluation Mode**: `⚡ Static Heuristic (Fast CI)`  

## Dimension Breakdown

| Quality Dimension | Weight | Score | Status |
| :--- | :---: | :---: | :---: |
| **Specification Compliance** | 10% | `100.0` | ✅ |
| **Content & Progressive Disclosure** | 15% | `90.0` | ✅ |
| **Functional Correctness** | 25% | `100.0` | ✅ |
| **Skill Lift vs Baseline** | 15% | `100.0` | ✅ |
| **Trigger Quality (F1)** | 10% | `85.7` | ✅ |
| **Reliability** | 5% | `90.0` | ✅ |
| **Token & Time Efficiency** | 5% | `85.0` | ✅ |
| **Security (SkillSpector)** | 15% | `100.0` | ✅ |
| **Total Composite Score** | **100%** | **`95.8`** | **✅ PASS** |

## Benchmark Summary
- **Test Cases**: `2/2 passed`
- **Skill Lift**: `100.0% with skill` vs `25.0% without skill` (Delta: `+75.0pp`)
- **Resource Footprint**: `~0.0s execution`, `~0 tokens`

## Security Profile (NVIDIA SkillSpector)
- **Confirmed Critical**: `0`
- **Confirmed High**: `0`
- **Medium / Low**: `0 Medium`, `0 Low`
- **Suppressed False Positives**: `5`

### Security Findings Details

| Severity | Category | File:Line | Finding Description / Evidence |
| :--- | :--- | :--- | :--- |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `change_impact_skill.py:84` | Subprocess Invocation via subprocess.run - `  81 \| def is_git_repo(repo_path: Path) -> bool:   82 \|     """Return True onl` |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `change_impact_skill.py:105` | Subprocess Invocation via subprocess.run - ` 102 \|     does not exist).  103 \|     """  104 \|     # Tier 1: diff against ` |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `change_impact_skill.py:124` | Subprocess Invocation via subprocess.run - ` 121 \|     # not-yet-`git add`ed) files — `git diff` alone never reports untrac` |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `change_impact_skill.py:130` | Subprocess Invocation via subprocess.run - ` 127 \|     )  128 \|     files = [f.strip() for f in result.stdout.splitlines()` |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `change_impact_skill.py:140` | Subprocess Invocation via subprocess.run - ` 137 \|         return sorted(set(files))  138 \|   139 \|     # Tier 3: most re` |

## Regression Analysis
- **Overall Delta**: `+0.0 points`
- **Functional Delta**: `+0.0 points`
- **Security Delta**: `+0.0 points`
- **Verdict**: ✅ No regressions.
