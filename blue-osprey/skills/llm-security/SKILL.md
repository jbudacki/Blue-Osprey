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
identifies candidate review surfaces aligned to the OWASP Top 10 for LLM
Applications 2026 taxonomy. A match is not a confirmed vulnerability.

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

### Phase 2: Sensitive Information Disclosure (LLM02:2026)

Review whether confidential, regulated, privileged, or proprietary data can be
exposed through answers, tool arguments, retrieved chunks, reasoning traces,
logs, telemetry, embeddings, or observable inference properties. Use the
secrets specialist for credential-specific detection.

- [ ] Run secrets scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --secrets
  ```

---

### Phase 3: Prompt Injection (LLM01:2026)

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

### Phase 4: Excessive Agency & Improper Output Handling (LLM03:2026 / LLM10:2026)

Review excessive functionality, permissions, and autonomy separately from
unsafe model-output handling. Trace model output to tools, shells, APIs,
queries, paths, markup, and other downstream sinks.

- [ ] Run output handling scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --output
  ```

- [ ] Run agency scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --agency
  ```

---

### Phase 5: Unbounded Consumption (LLM06:2026)

Review token, context, reasoning, request-rate, concurrency, tool-loop, and
cost controls, including spending caps and circuit breakers.

- [ ] Run configuration scan
  ```bash
  python3 "$SKILL_DIR/scripts/llm_scan.py" --config
  ```

---

### Phase 6: Supply Chain, Poisoning, and Retrieval (LLM04:2026 / LLM05:2026 / LLM09:2026)

Assess third-party model, adapter, dataset, package, serialization, conversion,
and deployment provenance; poisoning of training, fine-tuning, embedding, or
RAG data; and vector/embedding risks such as inversion, retrieval poisoning,
jamming, membership inference, and semantic-cache abuse.

- [ ] Identify RAG/vector database usage
  ```bash
  rg -n "vector|embedding|rag|chroma|pinecone|weaviate|faiss" -g "*.py" -g "*.js" . | head -15
  ```

### Phase 7: Misinformation & Hidden Context Exposure (LLM07:2026 / LLM08:2026)

Review whether incorrect, incomplete, unsupported, or misleading output can
drive human decisions, automated workflows, or agent actions. Also review
exposure of system prompts, tool schemas, behavioral control logic, permissions,
roles, and output-format rules through hidden context.

### Taxonomy boundary

This skill uses the 2026 list for the LLM-as-application-component boundary.
When the model acts as an autonomous actor with tools, memory, multi-step
execution, or persistent state, pair this review with the OWASP Top 10 for
Agentic Applications and the appropriate Blue-Osprey agentic review workflow.

The attached source used for this update is `OWASP-GenAI-LLM-Top-10-2026-v1.0
(2).pdf`, labeled “Version 2026” and dated August 4, 2026; its cover states
that the publication date is still to be set. Treat the taxonomy as a supplied
reference until its official publication status is confirmed.

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
- OWASP Top 10 for LLM Applications (2026) mapping
- Severity classification criteria
- Detailed red flags by category
- Remediation recommendations
