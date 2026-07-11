---
name: crypto-analysis
description: "Analyze cryptographic implementations for security vulnerabilities, including weak algorithms, unsafe modes, key management problems, nonce or IV misuse, timing attacks, encoding misuse, and protocol design issues. Use when Codex reviews encryption, hashing, signing, certificates, key storage, or cryptographic protocols in codebases."
---

# Cryptographic Security Analysis

## Script path rule

When running helper scripts, resolve `SKILL_DIR` to this skill directory and run scripts by absolute path from the target repository root. Do not assume `./scripts` exists in the target repo.

```bash
SKILL_DIR="/absolute/path/to/crypto-analysis"
python3 "$SKILL_DIR/scripts/crypto_scan.py" --help
```

Comprehensive methodology for analyzing cryptographic implementations, detecting vulnerabilities, and assessing cryptographic security posture.

The helper reports context-sensitive candidates rather than confirmed
vulnerabilities. Severity describes the potential impact if the matched
primitive protects a security property; confidence describes how strongly the
syntax implies actual cryptographic use. Generated, vendored, cache, and
`.agents` directories are skipped by default.

## Quick Start

Run cryptographic security analysis on any codebase to identify weak algorithms, key management issues, implementation anti-patterns, and post-quantum readiness.

**Prerequisites:**
- [ ] Python 3.8+ available
- [ ] Target codebase accessible

Resolve `scripts/crypto_scan.py` relative to this skill directory. Use `--path`
to point at the target repo.

**Quick Scan:**
```bash
python3 /path/to/crypto-analysis/scripts/crypto_scan.py --path .
```

---

## Workflow

### Phase 1: Discovery & Inventory

Identify cryptographic usage scope and catalog all cryptographic functions.

- [ ] Detect cryptographic library imports
  ```bash
  rg -n "import.*crypto|from.*crypto|require.*crypto|Bouncy.*Castle|PyCryptodome|OpenSSL|jose|node-forge" -g "*.py" -g "*.js" -g "*.ts" -g "*.go" -g "*.java" . | head -20
  ```

---

### Phase 2: Implementation Analysis

Analyze algorithm choices, key lengths, modes, and configurations.

- [ ] Assess algorithm and mode configuration
  ```bash
  rg -n -i -C 5 "AES|RSA|ECDSA|SHA-256|GCM|CBC|ECB" -g "*.py" -g "*.js" -g "*.ts" -g "*.go" -g "*.java" . | head -50
  ```

- [ ] Check key length and strength
  ```bash
  rg -n -i "128|256|1024|2048|4096.*bit|key.*size|key.*length" -g "*.py" -g "*.js" -g "*.ts" -g "*.go" -g "*.java" . | head -20
  ```

---

### Phase 3: Key & Lifecycle Management

Map key generation, storage, and IV/nonce handling.

- [ ] Find certificate and key files
  ```bash
  rg --files -g '*.pem' -g '*.crt' -g '*.key' -g '*.p12' -g '*.pfx' | head -10
  ```

- [ ] Check for hardcoded keys or secrets
  ```bash
  rg -n "-----BEGIN.*PRIVATE KEY-----|-----BEGIN.*CERTIFICATE-----" -g "*.py" -g "*.js" -g "*.ts" -g "*.go" . | head -10
  ```

---

### Phase 4: Automated Vulnerability Scan

Run comprehensive vulnerability analysis using the analysis script.

- [ ] Run full cryptographic analysis
  ```bash
  python3 "$SKILL_DIR/scripts/crypto_scan.py" --all
  ```

- [ ] Detect timing attack vulnerabilities
  ```bash
  rg -n -i "==.*password|==.*secret|==.*token|==.*hash" -g "*.py" -g "*.js" -g "*.ts" -g "*.go" -g "*.java" . | head -15
  ```

---

## Output

Generate a cryptographic security report using the template in [references/reference.md](references/reference.md).

Save to: `reports/crypto-analysis-[date].md`

---

## Quick Reference

See [references/reference.md](references/reference.md) for:
- Algorithm security status (Secure vs. Broken)
- Common vulnerability patterns
- Post-Quantum readiness (PQC)
- Mitigation recommendations
