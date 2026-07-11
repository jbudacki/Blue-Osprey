---
name: vibe-code-detection
description: "Detect LLM-generated or vibe-coded patterns in Python projects, including AI-IDE artifacts, excessive generic naming, monolithic files, placeholder classes, high type-hint uniformity, identical docstring style, and unusual git velocity. Use when Codex analyzes Python repositories for AI-assisted code indicators or generated-code risk."
---

# Vibe-Code Detection for Python

## Script path rule

When running helper scripts, resolve `SKILL_DIR` to this skill directory and run scripts by absolute path from the target repository root. Do not assume `./scripts` exists in the target repo.

```bash
SKILL_DIR="/absolute/path/to/vibe-code-detection"
python3 "$SKILL_DIR/scripts/analyze.py" --help
```

Identify Python repositories that "feel" auto-generated or LLM-assisted through pattern analysis.

## Quick Start

Resolve `scripts/analyze.py` relative to this skill directory. To scan a target
repo, run the script by absolute path with the target repo as the working
directory.

Run a full analysis:
```bash
python3 /path/to/vibe-code-detection/scripts/analyze.py full-report
```

Or execute individual checks during the workflow below.

---

## Prerequisites

- [ ] Verify this is a Python project
  ```bash
  rg --files -g '*.py' -g '!**/__pycache__/**' | wc -l
  ```
  Abort: **Abort if count < 1** -- not a Python project

---

## Workflow

### Phase 1: Reconnaissance

Baseline layout and AI artifact detection.

- [ ] Check for AI-IDE directories
  ```bash
  ls -d .windsurf .cursor .aider .claude 2>/dev/null || echo "None found"
  ```

- [ ] Count markdown files in root (AI over-documents)
  ```bash
  rg --files -g '*.md' | rg -v '/' | wc -l
  ```

- [ ] Analyze generic naming patterns
  ```bash
  python3 "$SKILL_DIR/scripts/analyze.py" generic-names
  ```

**Assessment:**

| Finding | Level | Threshold |
|---------|-------|-----------|
| AI-IDE directory present | Low | Any |
| Markdown files in root | Low | >4, Medium >6 |
| Generic names (utils, core, helpers) | Low ≥3, Medium ≥6, High ≥10 |

---

### Phase 2: Code Structure

Detect over-engineering and monolithic patterns.

- [ ] Analyze class-to-file ratio
  ```bash
  python3 "$SKILL_DIR/scripts/analyze.py" class-ratio
  ```

- [ ] Find large files (>500 lines)
  ```bash
  # Manual check or use script
  rg --files -0 -g '*.py' -g '!**/__pycache__/**' | xargs -0 wc -l | sort -nr | head -10
  ```

- [ ] Count placeholder classes (class with only `pass`)
  ```bash
  rg -n "^class " -g "*.py" . | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    linenum=$(echo "$line" | cut -d: -f2)
    next=$(sed -n "$((linenum+1))p" "$file" | tr -d ' ')
    [ "$next" = "pass" ] && echo "$line"
  done | wc -l
  ```

---

### Phase 3: Code Quality Patterns

Detect perfectionist LLM patterns--humans are inconsistent.

- [ ] Analyze type hint coverage
  ```bash
  python3 "$SKILL_DIR/scripts/analyze.py" type-hints
  ```

- [ ] Analyze docstring consistency
  ```bash
  python3 "$SKILL_DIR/scripts/analyze.py" docstrings
  ```

---

### Phase 4: Git History

> Warning: **Skip if no `.git` directory**

- [ ] Check commit velocity
  ```bash
  git log --since="2 weeks ago" --oneline 2>/dev/null | wc -l
  ```

---

## Scoring

Calculate final vibe-score based on findings (see [references/reference.md](references/reference.md) for methodology).

| Score | Interpretation |
|-------|---------------|
| 1-3 | Unlikely vibe-coded |
| 4-5 | Possibly vibe-coded |
| 6-7 | Likely vibe-coded |
| 8-10 | Almost certainly vibe-coded |

---

## Output

Generate a summary report as specified in the reference.

---

## Related Skills

Consider running:
- `codebase-discovery`: For general mapping.
- `llm-security`: If AI-generated code handles sensitive data.
