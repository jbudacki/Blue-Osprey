# Codebase Discovery Reference

## Scoring Methodology

The discovery score (1-10) helps prioritize the depth of subsequent security analysis.

### Base Score: 1

### Scoring Modifiers
| Finding | Points | Rationale |
|---------|--------|-----------|
| 🔴 Critical Flag | +3 | Immediate security risks significantly increase analysis complexity. |
| 🟡 Warning Flag | +2 | Complexity or potential risks require targeted investigation. |
| 🟢 Info Flag | +1 | Standard architectural patterns to be noted. |
| Tech Stack (>4 languages) | +2 | Cross-language boundaries are common places for bugs/vulnerabilities. |
| Integrations (>4 types) | +2 | Increased attack surface due to external dependencies. |

*Total score is capped at **10**.*

## Score Interpretation

| Score | Level | Analysis Recommendation |
|-------|-------|-------------------------|
| **1-3** | Simple | Basic security audit; focus on dependency updates and common best practices. |
| **4-6** | Moderate | Targeted analysis; run specific skills (e.g., `secrets-analysis`) based on findings. |
| **7-10** | Complex | Comprehensive analysis; requires deep dive into architecture, crypto, and cross-service logic. |

## Severity Definitions

- **🔴 Critical**: Immediate remediation or deep investigation required (e.g., hardcoded secrets, RCE patterns).
- **🟡 Warning**: Potential risk or complexity that needs verification (e.g., mixed tech stack, high commit velocity).
- **🟢 Info**: Noteworthy architectural detail with no immediate risk (e.g., web framework detected, database usage).

## Exclusion Patterns

Analysis should generally ignore:
- `node_modules/`, `vendor/`, `site-packages/` (Vendored dependencies)
- `.git/`, `.svn/` (Version control metadata)
- `tests/`, `spec/`, `docs/` (Non-production code)
- Generated code (e.g., `dist/`, `build/`, `*.pb.go`)
