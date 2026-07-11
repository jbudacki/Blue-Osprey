# Vibe-Code Detection Reference

## Scoring Methodology

The vibe-score (1-10) indicates the likelihood that a Python project is primarily LLM-generated or "vibe-coded".

### Base Score: 1

### Scoring Modifiers
| Finding | Points | Rationale |
|---------|--------|-----------|
| 🔴 Critical Flag | +3 | Strong indicator of AI-assisted patterns (e.g., progress files, 100% consistency). |
| 🟡 Warning Flag | +2 | Common AI patterns that require further context (e.g., high class/file ratio). |
| 🟢 Info Flag | +1 | Minor indicators or standard AI preferences (e.g., AI-IDE usage, click+rich). |
| Perfectionist Bonus | +2 | Multiple patterns showing unnatural consistency (e.g., >95% type hints AND docstrings). |
| Total Consistency | +3 | 100% consistency in multiple categories is almost never human-driven. |

*Total score is capped at **10**.*

## Score Interpretation

| Score | Level | Interpretation |
|-------|-------|----------------|
| **1-3** | Unlikely | Human-driven development with standard inconsistencies. |
| **4-5** | Possible | Likely some AI assistance or very disciplined human development. |
| **6-7** | Likely | Strong evidence of significant LLM generation or "vibe-coding". |
| **8-10** | Certain | Almost certainly an LLM-generated repository with minimal human structural oversight. |

## Patterns of "Perfection"

Humans naturally deviate in naming, spacing, and documentation frequency. AI models tend toward:
- **100% Type Hinting**: Every function parameter and return value typed perfectly.
- **Consistent Docstrings**: Identical format (Google, NumPy, ReST) across 100% of methods.
- **Generic Modularization**: Creating `utils.py`, `core.py`, and `helpers.py` even for small scripts.
- **Over-documentation**: High volume of `.md` files in root explaining implementation details.
