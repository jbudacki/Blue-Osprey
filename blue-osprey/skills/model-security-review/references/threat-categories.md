# Threat Categories by Model Type

Use this checklist during Phase 3 (Threat Analysis). For each category, decide: applicable / not applicable / needs more info, and if applicable, identify the gap.

## Universal (all model types)

### Resource Exhaustion / Denial of Wallet
- Per-tenant rate limits on inference invocations (not just per-request size)
- gRPC connection pool exhaustion via repeat callers
- Expensive hyperparameter combinations that bypass row/token limits
- Timeout enforcement on both client (DB/gateway) and server (inference) side
- Graceful failure when inference service is overloaded - does the caller crash or return a clean error?

### Supply Chain
- Model weight integrity: published SHA-256 hash in model card
- Hash verification in download/deployment pipeline
- License compatibility (Apache 2.0 vs research-only vs commercial restrictions)
- Dependency vulnerabilities (pyproject.toml, requirements.txt) run audit
- Pinned versions vs floating tags

### Tenant Isolation (multi-tenant deployments)
- Inference cache keyed by tenant
- No cross-tenant data leakage in batched inference
- Tenant ID propagated through entire request path (gateway → inference metadata service)

### Input Validation
- Fail-early on type mismatch (e.g., JSON parsing in DB layer)
- Hyperparameter bounds enforced at inference engine
- Max payload / max rows / max tokens enforced before model invocation
- Structured schema validation (not just type checks)

### Infrastructure
- mTLS or signed tokens between services
- Endpoint exposure (localhost-only vs network-reachable)
- Secrets management (no hardcoded keys, use of vault/parameter store)
- Audit logging on inference calls (who, what, when, tenant)

---

## Numerical / Time-Series Models

### Adversarial Robustness
- White-box attacks (PGD, FGSM): tested? results?
- Grey-box attacks (frequency-domain, transfer attacks): tested?
- Black-box attacks (query-based): tested?
- Data poisoning: stealthy perturbations within L-infinity bounds
- Mitigation: input anomaly detection, ensemble forecasting, monitoring forecast deviation

### Output Bounds
- Forecast value clamping / sanity checks
- Detection of "flat-line" or "crash" outputs
- Confidence interval validation

---

## LLM / Generative Text Models

### Prompt Injection
- Direct injection in user input
- Indirect injection via retrieved documents (RAG)
- Tool-use injection (instructions embedded in tool output)
- Mitigation: prompt structure, instruction hierarchy, output filtering

### Jailbreaking
- Resistance to known jailbreak templates
- Refusal training evaluation
- Multi-turn conversation degradation

### Data Leakage / Memorization
- Training data extraction via targeted prompts
- PII memorization
- Mitigation: deduplication, training data filtering, output filtering

### Harmful Content
- CSAM, weapons, malware, bioweapons evaluation
- AMC Corp-specific: customer data leakage, internal system info disclosure

### Tool Use / Agent Risks
- Authentication on tool endpoints
- Tool output validation before re-prompting
- Sandbox isolation for code-execution tools
- Permission scoping per tool

---

## Multimodal Models

### Image Input Risks
- Adversarial perturbations on images
- Image-based prompt injection (text rendered in image)
- NSFW input detection

### Audio Input Risks
- Adversarial audio (inaudible commands)
- Voice cloning resistance

---

## Agent Models / Tool-Calling Systems

### Sandbox Isolation
- Container privileges (USER directive, root vs non-root)
- Capability dropping (--cap-drop=ALL)
- Read-only filesystem (--read-only)
- Network isolation (--network=none or strict allowlist)
- Resource limits (--memory, --cpus, --pids-limit)
- Seccomp/AppArmor profiles
- No-new-privileges flag

### Tool Endpoint Security
- Authentication on all tool endpoints (bearer token, mTLS)
- Localhost binding by default
- Schema validation on tool calls
- Payload size and timeout caps
- Audit logging on all executions

### Privilege Escalation
- File system writes outside scratch dir
- Network egress to internal services
- Access to host metadata services (IMDS)
- Container escape via shared kernel features

---

## Red-Flag Patterns to Always Flag
- Action: "*" and Resource: "*" in IAM policies
- 0.0.0.0/0 ingress on management ports (SSH, RDP)
- USER root in production Dockerfiles
- HTTP endpoints on 0.0.0.0 instead of 127.0.0.1 for sandbox services
- eval(), exec(), pickle.load() on network input
- No timeout / no max payload on /execute endpoints
- Hardcoded secrets in code or config
- Cross-account trust without aws:PrincipalOrgID or sts:ExternalId conditions
