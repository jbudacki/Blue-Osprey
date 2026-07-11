---
name: secrets-analysis
description: "Detect hardcoded secrets, API keys, tokens, passwords, private keys, credentials, and sensitive configuration, with optional active validation when explicitly authorized. Use when Codex scans codebases for exposed credentials, secret leakage, credential hygiene, or remediation prioritization."
---

# Hardcoded Secrets Analysis

## Script path rule

When running helper scripts, resolve `SKILL_DIR` to this skill directory and run scripts by absolute path from the target repository root. Do not assume `./scripts` exists in the target repo.

```bash
SKILL_DIR="/absolute/path/to/secrets-analysis"
python3 "$SKILL_DIR/scripts/secrets_scan.py" --help
```

Comprehensive detection of hardcoded secrets, API keys, credentials, and sensitive data exposure in source code. Optionally validates discovered secrets to determine if they are still active.

## Quick Start

Run a secrets scan on any codebase to identify exposed credentials.

**Prerequisites:**
- [ ] Python 3.8+ available
- [ ] Target codebase accessible

Resolve `scripts/secrets_scan.py` relative to this skill directory. Use `--path`
to point at the target repo.

Generated, vendored, cache, and `.agents` directories are skipped by default.
Use `--include-agent-skills` or `--exclude-dir <name>` to adjust scope. Matches
are candidates until manually verified.

**Quick Scan:**
```bash
python3 /path/to/secrets-analysis/scripts/secrets_scan.py --path .
```

---

## Workflow

### Phase 1: Secret Discovery

Scan the codebase for hardcoded secrets across all categories.

- [ ] Run comprehensive secrets scan
  ```bash
  python3 "$SKILL_DIR/scripts/secrets_scan.py" --path .
  ```

- [ ] Review findings by severity (CRITICAL → HIGH → MEDIUM → LOW)

- [ ] Filter by category if needed
  ```bash
  # Available categories: api_keys, cloud, database, crypto, services
  python3 "$SKILL_DIR/scripts/secrets_scan.py" --category api_keys --category cloud
  ```

---

### Phase 2: Active Validation

Active credential validation is not implemented by this helper. The
`--validate` flag fails closed without making a network request. Validate a
credential only through a separately authorized, provider-specific procedure.

---

### Phase 3: Risk Assessment

Interpret findings and prioritize remediation.

- [ ] Count findings by severity
- [ ] Calculate risk score based on [references/reference.md](references/reference.md).

---

### Phase 4: Manual Pattern Search (Optional)

For custom patterns or additional verification, use targeted rg commands.

- [ ] Search for generic secret assignments
  ```bash
  rg -n "api.*key.*=|secret.*=|password.*=" -g "*.py" -g "*.js" -g "*.json" -g "*.yaml" . | rg -v "None|null|''|\"\"" | head -20
  ```

---

## Output

Generate a secrets analysis report using the reference in [references/reference.md](references/reference.md).

Save to: `reports/secrets-analysis-[date].md`

---

## Quick Reference

See [references/reference.md](references/reference.md) for:
- Complete pattern reference by category
- Risk classification matrix
- Mitigation recommendations
- Secret management best practices
