---
name: model-security-review
description: "Conduct structured security reviews of AI or ML models before deployment, adoption, or PLR-style sign-off. Use when Codex reviews a model card, Hugging Face model, arXiv paper, rollout document, serving code, third-party model, open-source model, or production AI/ML deployment for security risk."
---

# Model Security Review

## Purpose
Guide the user through a structured security assessment of an AI/ML model and produce a standardized Model Security Review markdown document suitable for PLR sign-off and engineering hand-off.

The output document follows the internal AMC Corp Model Security Review format.

## When to Invoke
* User asks for a "security review", "model security review", "model assessment" of a specific model.
* User provides a model name, HuggingFace URL, arXiv paper, internal rollout doc, or PLR ID and asks for security analysis.
* User is preparing PLR sign-off for an AI model deployment.
* User wants to evaluate adopting a third-party / open-source model.

## Inputs to Gather
Before drafting, collect the following from the user (ask in batches, not all at once - see Workflow). If the user provides docs/links, extract from them first and only ask about what's missing.

### Identity & Ownership
* Internal model name (e.g., Moirai-2.0-R-Small)
* Base model / predecessor
* Architecture type (decoder-only transformer, diffusion, etc.)
* Feature-owning team
* Engineering contacts (Slack handles)
* Reviewer name(s)
* Work item ID (e.g., W-21354707)
* PLR ID (e.g., PLR-008318)

### Resources
* Paper URL (arXiv)
* Blog post URL
* Model URL (Hugging Face, internal registry)
* Code repo URL (GitHub)
* Internal rollout doc URL
* Slack thread URL

### Use Case & Scope
* Intended use cases (e.g., demand forecasting, text generation)
* Primary adopters (data scientists, end users, agents)
* External access plans (open-source, customer-facing, internal only)
* Regions (Global / US-only / regulated regions)
* API compatibility (Python, REST, gRPC)
* Input modality (text, time-series numbers, images, multimodal)
* Output modality

### Training & Data
* Public datasets used
* Synthetic data generation method (e.g., KernelSynth, mixup)
* Internal/proprietary data used
* Training corpus size (samples, tokens, observations)
* Training method (pre-training loss, fine-tuning approach)
* Training compute (GPUs, hours, region)
* Model attestation (SHA-256 hash from model card)

### Infrastructure
* Training environment (hardware, cloud, region, precision)
* Inference hosting environment (CPU/GPU, provider)
* Endpoint convention (gRPC UDF, REST, internal service mesh)
* Security context (auth, mTLS, IAM, tenant isolation)
* Rollout safeguards (feature flags, dialect allowlists, kill switches)

### Performance & Limits
* Latency SLAs and benchmarks
* Accuracy/quality benchmarks (MASE, CRPS, MMLU, etc.)
* Hardcoded input/output limits (max rows, max tokens, max payload)
* Timeouts
* Hyperparameter validation behavior

### Security Testing
* Adversarial testing performed (PGD, frequency-domain attacks, jailbreaks, prompt injection)
* Safety/red-team datasets
* Known vulnerabilities and limitations
* Results summary (effective / partially effective / ineffective)

### Code to Review
* Path to inference/serving code
* Path to sandbox / agent execution code (if applicable)
* Dockerfile / deployment config paths

---

## Workflow
Follow these phases in order.

### Phase 1 - Intake & Scoping (5-10 min)
1.  Ask the user to share the canonical references:
    * Model card / Hugging Face URL or paper
    * Internal rollout doc
    * Code repo
    * Work item + PLR ID
2.  If a prior Model Security Review document exists for a related model, read it first to understand prior context and house style.
3.  Confirm scope: is this code-review-included, or doc-review-only?

### Phase 2 - Information Extraction (15-30 min)
1.  `web or browser tools` the public references (arXiv, Hugging Face, public GitHub) to extract:
    * Architecture, parameter count, training corpus
    * License
    * Stated limitations
    * Model attestation hash
2.  For internal docs (Google Docs, Confluence, GUS): `web or browser tools` will fail with 401. Ask the user to paste relevant excerpts or download as markdown.
3.  For code repos: clone or read locally. Identify:
    * Inference/serving entrypoints
    * Authentication on endpoints
    * Input validation
    * Sandbox isolation (Dockerfile, container flags)
    * Resource limits (timeouts, payload caps)
4.  Track gaps – questions the engineering team needs to answer.

### Phase 3 - Threat Analysis (20-40 min)
For each of the categories below, identify whether the model/system has a credible risk and what gap exists:
* **Resource exhaustion / Denial of Wallet:** tenant rate limits, batch size limits, gRPC/connection pool exhaustion, expensive hyperparameter combinations
* **Unauthenticated execution surfaces:** sandbox endpoints, agent tool execution, internal service-to-service calls without mTLS
* **Container / sandbox isolation:** root user, capabilities, network access, filesystem writes, resource cgroups
* **Adversarial robustness:** data poisoning, evasion attacks, prompt injection, jailbreaking (depending on modality)
* **Data exfiltration / model inversion:** training data memorization, embedding leakage
* **Supply chain:** model weight integrity (attestation hash verification), dependency vulnerabilities, license compatibility
* **Tenant isolation:** multi-tenant data leakage, cross-tenant inference cache pollution
* **Input validation:** type confusion, schema fail-early behavior, hyperparameter bounds

*Note: For LLM-style models, add: prompt injection, jailbreak resistance, PII leakage, harmful content generation.*

### Phase 4 - Code Review Findings (optional, 30-60 min)
If code is in scope, produce one Advisory per finding using this format:

```markdown
## Advisory N: <short title>
Severity: Critical | High | Medium | Low
Status: Open
Owner: <team>

### Impact
<what the attacker gains, blast radius>

### Attack Preconditions
- <bullet list of conditions required>

### Evidence
- <file path:line>
- <file path:line>

### Recommended Remediation
1. <numbered actionable step>
2. <numbered actionable step>

### Verification
<how to confirm the fix works>
```

Common findings to look for:
* HTTP/gRPC endpoints without auth
* USER root in Dockerfiles
* Missing --cap-drop ALL, --read-only, --network=none, --security-opt no-new-privileges
* eval(), exec(), pickle.load() on untrusted input
* No payload size or timeout caps on /execute-style endpoints
* Hardcoded credentials, API keys, or service tokens

### Phase 5 - Document Generation
1.  Fill in every section using gathered data.
2.  Place Security Recommendations at the top (before Overview) - this is the executive summary section that engineering and PLR readers see first. Order findings by severity.
3.  Use the exact heading hierarchy from templates.
4.  For unknown fields, write the question into the Questions section rather than guessing.
5.  Save the document to the user's chosen location (default: ./Model Security Review <ModelName>.md in the current working directory).

## Output Conventions
* File name: Model Security Review <ModelName>.md
* Top-level heading: # Model Security Review \- <ModelName>
* Each Security Recommendation contains: The Gap, Question, Recommendation
* Cite evidence with file paths (and line numbers when possible)
* Convert relative dates to absolute (e.g., "next quarter" → "Q3 2026")

## Example Invocations
* Full review with all materials: "Do a model security review for Moirai-2.0-R-Small. Paper: arxiv.org/abs/2511.11698, model: huggingface.co/amccorp/moirai-2.0-R-small, code: github.com/AMC-Corp-Research/uni2ts, work item W-21354707, PLR-008318."
* Doc-only review: "I have the rollout doc for AgentCore-LLM-v2. Can you draft the security review document? I'll paste the doc contents."

## Do Not
* Do not invent findings, vulnerabilities, or remediations.
* Do not generate metrics (latency, accuracy, parameter counts) that aren't in the source materials.
* Do not skip the Questions section.
* Do not commit the review to a public repo without the user's explicit instruction.
