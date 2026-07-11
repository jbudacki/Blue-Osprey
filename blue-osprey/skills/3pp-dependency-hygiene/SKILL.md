---
name: 3pp-dependency-hygiene
description: "Detect risky third-party dependency changes including unpinned versions, known-dangerous packages, typosquatting indicators, missing lockfile updates, non-standard registry sources, and Go version drift. Use when Codex reviews dependency manifest diffs or supply-chain risk in package.json, requirements.txt, pyproject.toml, pom.xml, go.mod, Gemfile, Dockerfiles, or lockfiles."
---

# 3PP Dependency Hygiene

Detect risky third-party dependency changes and supply chain risks detectable from dependency manifest diffs.

## Overview

This skill identifies dependency changes that introduce supply chain risk through:
- Unpinned or loosely-pinned version specifiers.
- Packages with well-known security "footguns" or dangerous defaults.
- Possible typosquatting (misspelled names of popular packages).
- Manifest changes without corresponding lockfile updates.
- Packages sourced from non-standard or untrusted registries.

---

## Mandatory Self-Check Gates

Pass all gates before emitting a finding:

1. **Gate 0: Rationale check.** Discard if rationale contains "cannot verify from diff alone", "assumed", or if it flags pre-existing patterns.
2. **Gate 1: Diff-surface verification.** Every finding must cite specific `+` lines in the diff.
3. **Gate 2: Curated-list match.** Typosquat claims must match the curated list below.
4. **Gate 3: Dual-surface check.** For lockfile claims, verify the manifest changed AND the lockfile path is NOT in the diff.

---

## What to Check

### 1. Unpinned or Loosely-Pinned Versions
Dependencies MUST be pinned to exact versions in production manifests.

- **Incorrect**: `requests`, `flask>=2.0`, `"express": "*"`, `"axios": "^1.0.0"`.
- **Correct**: `requests==2.31.0`, `"express": "4.18.2"`, `implementation 'com.google.guava:guava:32.1.3-jre'`.

*Note: SNAPSHOT versions on the project's own artifact are acceptable; flag them only on external dependencies.*

### 2. Known-Dangerous Packages (Blocklist)

| Ecosystem | Package | Risk |
| :--- | :--- | :--- |
| **Python** | `pickle`/`cPickle` | Arbitrary code execution on deserialization. |
| | `pyyaml` (unsafe) | Must use `yaml.safe_load()`. |
| | `jellyfIsh` (cap I) | Malicious typosquat of `jellyfish`. |
| **JS/Node** | `event-stream` (3.3.4-3.3.6) | Malicious targeting of Bitcoin wallets. |
| | `colors` (>1.4.0) | Maintainer intentionally corrupted (infinite loop). |
| | `node-ipc` (10.1.1-10.1.3) | Maintainer added destructive code. |
| **Java** | `log4j-core` (<2.17.1) | Log4Shell RCE. |

### 3. Typosquatting Indicators
Flag new dependencies suspiciously close to popular packages.

| Legitimate | Known Typosquats |
| :--- | :--- |
| `jellyfish` | `jellyfIsh` (capital I) |
| `python-dateutil` | `python3-dateutil`, `python-dateutl` |
| `cross-env` | `crossenv`, `cross-env.js` |
| `requests` | `requestes`, `request` (singular on npm) |
| `urllib3` | `urlib3`, `urllib` |

### 4. Missing Lockfile Updates
When a manifest changes, the lockfile must also be updated.

- **package.json** → `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **requirements.txt** → `requirements.lock`, `poetry.lock`, `Pipfile.lock`, `uv.lock`
- **Gemfile** → `Gemfile.lock`
- **go.mod** → `go.sum`

### 5. Non-Default Registry Sources
Flag dependencies pulled over HTTP or from unknown external registries.
- **Incorrect**: `--index-url http://...`, `--extra-index-url http://...`

### 6. Go Module Version Drift
When `go.mod` updates the Go version, any builder image in a `Dockerfile` must match.

---

## Severity Decision Tree

1. **WARNING**: Completely unpinned (`*`, `latest`), confirmed blocklist match, or HTTP registry.
2. **SUGGESTION**: Loose version range (`^`, `~`, `>=`), missing lockfile update, or suspected (unconfirmed) typosquat.

---

## Do NOT Flag

- **Removals**: Deleting dependencies reduces attack surface.
- **Pre-existing patterns**: Only flag weakening introduced in the current diff.
- **Dev/Test dependencies**: Apply lighter scrutiny to `devDependencies` or test scope.
- **Self-SNAPSHOTS**: Project's own `-SNAPSHOT` versioning in Maven.
- **Example/Template directories**: `example/`, `sample/`, etc.
