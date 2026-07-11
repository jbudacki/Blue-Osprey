---
name: codebase-discovery
description: "Perform deep reconnaissance of an unfamiliar codebase to map structure, technologies, dependencies, integrations, git signals, and security concerns. Use when Codex needs to understand a project before implementation, audit planning, security review, or choosing which other analysis skills to run."
---

# Codebase Discovery

## Script path rule

When running helper scripts, resolve `SKILL_DIR` to this skill directory and run scripts by absolute path from the target repository root. Do not assume `./scripts` exists in the target repo.

```bash
SKILL_DIR="/absolute/path/to/codebase-discovery"
python3 "$SKILL_DIR/scripts/discover.py" --help
```

Analyze a target codebase to map its structure, identify technologies, detect security patterns, and generate prioritized recommendations for further analysis.

The helper emits reconnaissance signals and unverified security candidates. Do
not convert a match into a finding until you have traced the relevant
source-to-sink path and checked preconditions. Generated, vendored, cache, and
`.agents` directories are skipped by default. Use `--include-agent-skills`
or `--exclude-dir <name>` to adjust scope.

## Quick Start

Resolve `scripts/discover.py` relative to this skill directory. To scan a target
repo, run the script by absolute path with the target repo as the working
directory.

Run a full discovery analysis:
```bash
python3 /path/to/codebase-discovery/scripts/discover.py full-report
```

Or execute individual checks during the workflow below.

---

## Prerequisites

- [ ] Confirm target directory is accessible
  ```bash
  ls -la
  ```

- [ ] Verify Python 3 is available
  ```bash
  python3 --version
  ```

---

## Workflow

### Phase 1: Structure Reconnaissance

Map project layout, identify file types, and locate entry points.

- [ ] Analyze project structure
  ```bash
  python3 "$SKILL_DIR/scripts/discover.py" structure
  ```

- [ ] Review file type distribution
  
  Check the output for primary languages and file counts.

**Assessment:**

| Finding | Level | Action |
|---------|-------|--------|
| Mixed technology stack (>3 languages) | Medium | Plan multi-language analysis |
| Large config file count (>20) | Low | Review configuration complexity |
| No entry points found | Medium | Investigate build system |

---

### Phase 2: Technology Stack Identification

Identify frameworks, dependencies, and databases in use.

- [ ] Detect tech stack
  ```bash
  python3 "$SKILL_DIR/scripts/discover.py" tech-stack
  ```

- [ ] Review dependency manifests
  
  Check for `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`.

- [ ] Note detected frameworks
  
  Web frameworks trigger security audit recommendations.

**Assessment:**

| Finding | Level | Action |
|---------|-------|--------|
| Large dependency count (>100) | Medium | Review for outdated/vulnerable deps |
| Web framework detected | Low | Queue web security audit |
| Database usage detected | Low | Queue SQL injection analysis |

---

### Phase 3: Git Repository Analysis

Understand project history and development patterns.

> Warning: **Skip if no `.git` directory**

- [ ] Analyze git history
  ```bash
  python3 "$SKILL_DIR/scripts/discover.py" git-analysis
  ```

- [ ] Check for secret exposure
  
  Review `potential_secret_commits` if flagged.

- [ ] Assess development velocity
  
  Low author count or high commit velocity may indicate vibe-coded project.

**Assessment:**

| Finding | Level | Action |
|---------|-------|--------|
| Potential secrets in commits | High | Run hardcoded secrets analysis immediately |
| Few unique authors (<3) | Medium | Consider vibe-code detection |
| No git repo | Low | Note for recommendations |

---

### Phase 4: External Integrations

Find APIs, services, and external connections.

- [ ] Scan for integrations
  ```bash
  python3 "$SKILL_DIR/scripts/discover.py" integrations
  ```

- [ ] Review environment variable usage
  
  Check for sensitive config patterns.

- [ ] Check container/deployment files
  
  Note infrastructure complexity.

**Assessment:**

| Finding | Level | Action |
|---------|-------|--------|
| Multiple external integrations (>5) | Medium | Expand attack surface review |
| Hardcoded URLs in config | Medium | Verify no credentials in URLs |
| AWS/GCP/Azure detected | Low | Review cloud security config |

---

### Phase 5: Security Pattern Detection

Identify immediate security concerns.

- [ ] Run security scan
  ```bash
  python3 "$SKILL_DIR/scripts/discover.py" security
  ```

- [ ] Review high-priority candidates
  
  Validate High candidates before reporting or remediation.

- [ ] Note crypto usage
  
  Cryptographic code requires specialized review.

**Assessment:**

| Finding | Level | Action |
|---------|-------|--------|
| Hardcoded secrets | High | Immediate remediation required |
| SQL injection patterns | High | Queue injection analysis |
| Dangerous eval/exec | High | Review for RCE vulnerabilities |
| Shell execution | Medium | Review command injection risk |
| Crypto usage | Low | Queue crypto-analysis skill |
| MCP server detected | Low | Review MCP security patterns |

---

## Scoring

Calculate discovery score based on findings (see [references/reference.md](references/reference.md) for details).

| Score | Interpretation |
|-------|---------------|
| 1-3 | Simple project -- basic security audit recommended |
| 4-6 | Moderate complexity -- targeted analysis needed |
| 7-10 | Complex system -- comprehensive analysis required |

---

## Output

Generate a summary report:

```markdown
# Codebase Discovery: [Project Name]

**Score:** X/10 ([Interpretation])
**Date:** [YYYY-MM-DD]

## Project Overview

| Attribute | Value |
|-----------|-------|
| Primary Language(s) | ... |
| Framework(s) | ... |
| Database(s) | ... |
| Total Files | ... |

## Key Findings

| Category | Finding | Level |
|----------|---------|-------|
| ... | ... | ... |

## Recommended Next Steps

### High Priority
- [ ] [Skill/Action to run]

### Medium Priority  
- [ ] [Skill/Action to run]

### Low Priority
- [ ] [Skill/Action to run]

## Technology-Specific Notes

- [Framework]: [Specific considerations]
- [Language]: [Analysis recommendations]
```

---

## Triage Notes

**Downgrade severity when:**
- Large file count is due to generated code (marked appropriately)
- Multiple languages are test/build tooling only
- Integration patterns are in documentation/comments only

**Ignore findings in:**
- `tests/` directories (for secrets scanning)
- Generated code directories
- Vendored dependencies (`vendor/`, `node_modules/`)
- Example/sample directories

---

## Related Skills

Based on discovery findings, consider running:

| Condition | Recommended Skill |
|-----------|------------------|
| Python detected | `vibe-code-detection` |
| Crypto usage found | `crypto-analysis` |
| Web framework detected | Web security audit |
| MCP server found | MCP security review |
