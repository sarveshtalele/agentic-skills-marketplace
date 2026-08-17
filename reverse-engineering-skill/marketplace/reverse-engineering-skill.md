# Scorecard: `reverse-engineering-skill`

**Overall Quality Score**: `96.1/100`  
**Evaluation Status**: **✅ PASS**  
**Evaluation Mode**: `⚡ Static Heuristic (Fast CI)`  

## Dimension Breakdown

| Quality Dimension | Weight | Score | Status |
| :--- | :---: | :---: | :---: |
| **Specification Compliance** | 10% | `100.0` | ✅ |
| **Content & Progressive Disclosure** | 15% | `90.0` | ✅ |
| **Functional Correctness** | 25% | `100.0` | ✅ |
| **Skill Lift vs Baseline** | 15% | `100.0` | ✅ |
| **Trigger Quality (F1)** | 10% | `88.9` | ✅ |
| **Reliability** | 5% | `90.0` | ✅ |
| **Token & Time Efficiency** | 5% | `85.0` | ✅ |
| **Security (SkillSpector)** | 15% | `100.0` | ✅ |
| **Total Composite Score** | **100%** | **`96.1`** | **✅ PASS** |

## Benchmark Summary
- **Test Cases**: `1/1 passed`
- **Skill Lift**: `100.0% with skill` vs `0.0% without skill` (Delta: `+100.0pp`)
- **Resource Footprint**: `~0.0s execution`, `~0 tokens`

## Security Profile (NVIDIA SkillSpector)
- **Confirmed Critical**: `0`
- **Confirmed High**: `0`
- **Medium / Low**: `0 Medium`, `0 Low`
- **Suppressed False Positives**: `35`

### Security Findings Details

| Severity | Category | File:Line | Finding Description / Evidence |
| :--- | :--- | :--- | :--- |
| 🟡 `MEDIUM` | `Dangerous Code AST` | `pipeline.py:83` | Subprocess Invocation via subprocess.run - `  80 \|             the stderr output included in the exception message.   81 \|` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1612` | Unsafe Output Handling / DOM Injection - `1609 \|     {{ label: 'API Endpoints',       value: DATA.metrics.endpoints, sub:` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1635` | Unsafe Output Handling / DOM Injection - `1632 \|   const el = document.getElementById('lang-hbar'); 1633 \|   const langs` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1660` | Unsafe Output Handling / DOM Injection - `1657 \|   document.getElementById('arch-pattern-text').textContent = DATA.archPa` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1670` | Unsafe Output Handling / DOM Injection - `1667 \| // ---------------------------------------------------------------- 1668` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1681` | Unsafe Output Handling / DOM Injection - `1678 \| function buildModuleBars() {{ 1679 \|   const el = document.getElementBy` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1685` | Unsafe Output Handling / DOM Injection - `1682 \|     return; 1683 \|   }} 1684 \|   const max = DATA.topModules[0].connec` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1703` | Unsafe Output Handling / DOM Injection - `1700 \|   const wrap = document.getElementById('endpoints-table-wrap'); 1701 \| ` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1717` | Unsafe Output Handling / DOM Injection - `1714 \|       <td><span class="code-mono">${{ep.file}}</span></td> 1715 \|     <` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1742` | Unsafe Output Handling / DOM Injection - `1739 \| function buildDeadCode() {{ 1740 \|   const fl = document.getElementById` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1747` | Unsafe Output Handling / DOM Injection - `1744 \|         `<li class="dead-item"><span class="dead-dot" style="background:` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1763` | Unsafe Output Handling / DOM Injection - `1760 \|   const el = document.getElementById('layers-list'); 1761 \|   const ds ` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1767` | Unsafe Output Handling / DOM Injection - `1764 \|     ? DATA.layers.map(l => `<span class="layer-chip">${{l}}</span>`).joi` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1792` | Unsafe Output Handling / DOM Injection - `1789 \|   const whatEl = document.getElementById('hiw-what'); 1790 \|   if (what` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1800` | Unsafe Output Handling / DOM Injection - `1797 \|   if (wfEl) {{ 1798 \|     const workflows = bl.core_workflows \|\| []; ` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1812` | Unsafe Output Handling / DOM Injection - `1809 \|           </div>`; 1810 \|       }}).join(''); 1811 \|     }} else {{ 18` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1820` | Unsafe Output Handling / DOM Injection - `1817 \|   const rolesEl = document.getElementById('hiw-roles'); 1818 \|   if (ro` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1829` | Unsafe Output Handling / DOM Injection - `1826 \|   const rulesEl = document.getElementById('hiw-rules'); 1827 \|   if (ru` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1839` | Unsafe Output Handling / DOM Injection - `1836 \|   if (entEl) {{ 1837 \|     const ents = bl.data_entities_explained \|\|` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1858` | Unsafe Output Handling / DOM Injection - `1855 \|           </tbody> 1856 \|         </table>`; 1857 \|     }} else {{ 185` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1866` | Unsafe Output Handling / DOM Injection - `1863 \|   const intEl = document.getElementById('hiw-integrations'); 1864 \|   i` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1880` | Unsafe Output Handling / DOM Injection - `1877 \|    1878 \|   const data = DATA.blockDiagram; 1879 \|   if (!data \|\| !d` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1921` | Unsafe Output Handling / DOM Injection - `1918 \|   }}); 1919 \|    1920 \|   html += '</div>'; 1921 >   container.innerHT` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:1997` | Unsafe Output Handling / DOM Injection - `1994 \|       {{ label: 'Relationships',      value: schema.relationship_count \` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2015` | Unsafe Output Handling / DOM Injection - `2012 \|   // Legend inside the entity diagram card 2013 \|   const legendEl = do` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2024` | Unsafe Output Handling / DOM Injection - `2021 \|   const bgEl = document.getElementById('boundary-grid'); 2022 \|   if (b` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2026` | Unsafe Output Handling / DOM Injection - `2023 \|     if (!boundaries.length) {{ 2024 \|       bgEl.innerHTML = '<p style=` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2051` | Unsafe Output Handling / DOM Injection - `2048 \|   if (etEl) {{ 2049 \|     const ents = schema.entities \|\| []; 2050 \|` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2072` | Unsafe Output Handling / DOM Injection - `2069 \|           <td><span class="code-mono">${{e.file}}</span></td> 2070 \|   ` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2098` | Unsafe Output Handling / DOM Injection - `2095 \|  2096 \|   if (!entities.length) {{ 2097 \|     if (wrap) wrap.style.hei` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2177` | Unsafe Output Handling / DOM Injection - `2174 \|       entityNetInited = true; 2175 \|     }} catch (err) {{ 2176 \|     ` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2191` | Unsafe Output Handling / DOM Injection - `2188 \|   // Domain badge 2189 \|   const domainEl = document.getElementById('bl` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2204` | Unsafe Output Handling / DOM Injection - `2201 \|   // User roles 2202 \|   const rolesEl = document.getElementById('bl-ro` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2212` | Unsafe Output Handling / DOM Injection - `2209 \|   // Integrations 2210 \|   const intEl = document.getElementById('bl-in` |
| 🔴 `HIGH` | `Output Handling` | `dashboard.py:2221` | Unsafe Output Handling / DOM Injection - `2218 \|   const rulesEl = document.getElementById('bl-rules'); 2219 \|   if (rul` |

## Regression Analysis
- **Overall Delta**: `+15.0 points`
- **Functional Delta**: `+0.0 points`
- **Security Delta**: `+100.0 points`
- **Verdict**: ✅ No regressions.
