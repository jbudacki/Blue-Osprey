# OWASP Top 10 for LLM Applications (2026)

This reference aligns the skill to the supplied document
`OWASP-GenAI-LLM-Top-10-2026-v1.0 (2).pdf`. The PDF identifies itself as
“Version 2026,” dated August 4, 2026, and says the publication date is still to
be set. Confirm official publication status before representing this mapping as
an adopted external standard.

## Categories

1. **LLM01:2026 Prompt Injection** — Untrusted direct input, retrieved content,
   tool output, multimodal content, intermediate reasoning, or persistent
   memory alters model behavior in unintended ways.
2. **LLM02:2026 Sensitive Information Disclosure** — Confidential, regulated,
   privileged, or proprietary information is exposed through answers, tool
   arguments, context, reasoning traces, logs, telemetry, embeddings, or
   observable inference properties.
3. **LLM03:2026 Excessive Agency** — Unexpected, ambiguous, hallucinated, or
   manipulated model output can trigger damaging actions because functionality,
   permissions, or autonomy are excessive.
4. **LLM04:2026 Supply Chain** — Third-party models, adapters, datasets,
   packages, serialization formats, conversion pipelines, or deployment
   platforms compromise integrity, safety, or availability.
5. **LLM05:2026 Data and Model Poisoning** — Pre-training, fine-tuning,
   embedding, RAG, continuous-learning, or model-distribution data and
   artifacts are manipulated to embed harmful behavior, bias, or weaknesses.
6. **LLM06:2026 Unbounded Consumption** — Uncontrolled inference, token,
   context, reasoning, tool-loop, or other resource consumption causes service
   disruption, unsustainable cost, or model-cloning exposure.
7. **LLM07:2026 Misinformation** — Incorrect, incomplete, unsupported, or
   misleading output appears credible enough to influence a person, workflow,
   or agent action.
8. **LLM08:2026 Hidden Context Exposure** — System prompts, hidden instructions,
   tool schemas, behavioral control logic, permissions, roles, or output rules
   are disclosed through context or model output.
9. **LLM09:2026 Vector and Embedding Weaknesses** — Embedding inversion,
   retrieval-time poisoning, retrieval jamming, membership inference,
   semantic-cache abuse, or multimodal embedding weaknesses expose or distort
   retrieval behavior.
10. **LLM10:2026 Improper Output Handling** — Model output is insufficiently
    validated, sanitized, encoded, or mediated before reaching shells, queries,
    paths, browsers, terminals, logs, tools, or other downstream systems.

## Review distinctions

- Prompt Injection is the input-side boundary problem; unsafe downstream use of
  model output belongs to Improper Output Handling.
- Sensitive Information Disclosure concerns what is exposed; Hidden Context
  Exposure focuses on protected instructions, schemas, roles, and control logic.
- Excessive Agency concerns functionality, permissions, and autonomy; it is not
  interchangeable with output sanitization.
- Data and Model Poisoning covers durable corruption of data or model behavior;
  inference-time malicious instructions in retrieved content remain Prompt
  Injection, and embedding-geometry attacks remain Vector and Embedding
  Weaknesses.
- Misinformation covers the harmful failure mode of false or misleading output.
  Root causes such as injection, poisoning, or supply-chain compromise should
  also be identified when supported by evidence.

## Review prompts

For each applicable category, identify the entry point, lower-trust source,
reachable sink or failed control, trust boundary, preconditions, impact,
false-positive considerations, and verification. Do not promote a heuristic
match to a finding without a demonstrated path.

### Prompt Injection (LLM01)

- Direct user input, retrieved documents, web pages, email, tool output,
  database rows, images, audio, video, memory, and inter-agent content
- Context pooling, cross-session persistence, multimodal or invisible encoding,
  and chained tool execution
- Provenance labeling, capability restriction, deterministic mediation, and
  human approval for privileged or irreversible actions

### Sensitive Information Disclosure (LLM02)

- PII, PHI, financial data, credentials, API keys, trade secrets, model weights,
  privileged communications, embeddings, logs, and telemetry
- Training, inference, pipeline, and observation-time disclosure surfaces
- Data minimization, authorization-aware retrieval, redaction, output controls,
  and protection of derived artifacts

### Excessive Agency (LLM03)

- Excessive functionality, permissions, or autonomy
- Tool calls, shell access, database writes, external communication, and
  irreversible state changes
- Least privilege, deterministic policy mediation, capability budgets, and
  explicit human confirmation

### Supply Chain (LLM04)

- Third-party models, datasets, adapters, packages, model registries, model
  cards, conversion/merge workflows, and serialization formats
- Provenance, integrity checks, signed artifacts, dependency hygiene, isolated
  loading, and license controls

### Data and Model Poisoning (LLM05)

- Pre-training, fine-tuning, embedding creation, RAG corpora, feedback loops,
  continuous learning, tokenizer/configuration files, and adapters
- Source validation, anomaly detection, staged promotion, reproducibility, and
  rollback or replacement paths

### Unbounded Consumption (LLM06)

- Input/output tokens, context accumulation, reasoning budgets, multimodal
  inputs, concurrency, agent loops, and downstream tool amplification
- Rate and token limits, spending caps, timeouts, circuit breakers, and cost
  attribution monitoring

### Misinformation (LLM07)

- Unsupported decisions, incorrect state inference, fabricated code or
  dependencies, misleading summaries, and forged evidence
- Grounding, source attribution, independent validation, human review, and
  fail-safe handling when confidence or evidence is insufficient

### Hidden Context Exposure (LLM08)

- System prompts, hidden context, tool/function schemas, permissions, roles,
  refusal logic, behavioral controls, and output-format constraints
- Keep secrets and security-critical configuration out of model-visible context
  and assume hidden context may be disclosed

### Vector and Embedding Weaknesses (LLM09)

- Embedding inversion, retrieval poisoning, retrieval jamming, membership
  inference, semantic-cache poisoning, and multimodal embedding attacks
- Treat exposed embeddings and backups as sensitive data; validate corpus writes,
  protect similarity metadata, and monitor retrieval integrity

### Improper Output Handling (LLM10)

- Shell, `eval`, SQL, file paths, HTML/JavaScript, Markdown, email templates,
  terminal/log output, external-resource fetches, and tool arguments
- Apply context-specific encoding, structural validation, deterministic policy
  checks, safe parsers, bounded output, and monitoring before downstream use

## Scope boundary

The 2026 document states that this list covers the LLM as an application
component. When the model is an autonomous actor with tools, persistent memory,
or multi-step consequences, pair this reference with the OWASP Top 10 for
Agentic Applications and any applicable Blue-Osprey agentic security skill.
