---
name: llm-security
description: "Detect LLM-specific security vulnerabilities using OWASP Top 10 for LLM Applications concepts, including prompt injection, hardcoded API keys, improper output handling, excessive agency, insecure RAG, and weak model configuration. Use when Codex reviews codebases integrating OpenAI, Anthropic, LangChain, vector databases, agents, tools, or other LLM frameworks."
---

# LLM Security Analysis

## Script path rule

When running helper scripts, resolve `SKILL_DIR` to this skill directory and run scripts by absolute path from the target repository root. Do not assume `./scripts` exists in the target repo.

```bash
SKILL_DIR="/absolute/path/to/llm-security"
python3 "$SKILL_DIR/scripts/llm_scan.py" --help
```

Heuristic reconnaissance for codebases integrating Large Language Models. It
identifies candidate review surfaces for prompt injection, improper output
handling, excessive agency, secrets, and configuration risk. A match is not a
confirmed vulnerability.

## Quick Start

Run LLM security analysis on a codebase to identify OWASP-aligned review
surfaces.

> Warning: The helper prints matching source lines. Run it only in an approved
> local environment and do not share raw logs without reviewing them. Use
> `$secrets-analysis` when you need fingerprinted credential evidence.

Generated, vendored, cache, and `.agents` directories are skipped by default.
Use `--include-agent-skills` or `--exclude-dir <name>` to adjust scope.

**Prerequisites:**
- [ ] Python 3.8+ available
- [ ] Target codebase accessible
- [ ] Write access for report output

Resolve `scripts/llm_scan.py` relative to this skill directory. Use `--path`
to point at the target repo.

---

## Workflow

### Phase 1: Discovery

Identify LLM integration points and understand the application architecture.

- [ ] Run LLM discovery scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --discover
  ```

- [ ] Verify LLM library imports (manual check)
  ```bash
  rg -n "import.*openai|import.*anthropic|import.*langchain" -g "*.py" -g "*.js" -g "*.ts" . | head -15
  ```

- [ ] Check configuration for LLM settings
  ```bash
  rg -n "OPENAI|ANTHROPIC|LLM|GPT|CLAUDE" -g "*.env*" -g "*.yaml" -g "*.json" . | head -10
  ```

---

### Phase 2: Secrets & API Keys (LLM02)

Detect hardcoded API keys and insecure credential management.

- [ ] Run secrets scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --secrets
  ```

---

### Phase 3: Prompt Injection (LLM01)

Identify prompt injection attack vectors - the #1 vulnerability for LLM applications.

- [ ] Run prompt injection scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --injection
  ```

- [ ] Check for direct input concatenation
  ```bash
  rg -n "prompt.*=.*input|prompt.*+.*input|f['\"].*{.*input" -g "*.py" -g "*.js" . | head -15
  ```

---

### Phase 4: Output & Agency (LLM05/LLM06)

Detect improper output handling and excessive LLM permissions.

- [ ] Run output handling scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --output
  ```

- [ ] Run agency scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --agency
  ```

---

### Phase 5: Configuration & Resources (LLM09/LLM10)

Review LLM configuration and resource management.

- [ ] Run configuration scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --config
  ```

---

### Phase 6: RAG & Supply Chain (LLM08/LLM04)

Assess RAG implementations and model provenance.

- [ ] Identify RAG/vector database usage
  ```bash
  rg -n "vector|embedding|rag|chroma|pinecone|weaviate|faiss" -g "*.py" -g "*.js" . | head -15
  ```

---

## Full Scan

Run all heuristic categories:

```bash
python3 "$SKILL_DIR/scripts/llm_scan.py" --all
```

For JSON output (integration with other tools):

```bash
python3 "$SKILL_DIR/scripts/llm_scan.py" --all --json > llm-security-report.json
```

---

## Output

Generate an LLM security report following the template in [references/reference.md](references/reference.md).

Save to: `reports/llm-security-[date].md`

---

## Quick Reference

See [references/reference.md](references/reference.md) for:
- OWASP Top 10 for LLM Applications (2025) mapping
- Severity classification criteria
- Detailed red flags by category
- Remediation recommendations
