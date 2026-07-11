# model-security-review

A Gemini CLI skill that conducts structured security assessments of AI/ML models prior to production deployment, producing a standardized Model Security Review markdown document suitable for PLR (Production Launch Review) sign-off and engineering hand-off.

## Overview

`model-security-review` is invoked when you ask the agent to review an AI/ML model's security posture — for example before adopting a third-party / open-source model, before signing off on internal PLR for a new model deployment, or when you provide a HuggingFace model card, an arXiv paper, or an internal rollout doc and ask "is this safe to ship?"

The skill walks through a five-phase workflow that mirrors how a security engineer would actually do the assessment: scope the work, extract facts from public references and code, run the threats through a checklist by model type, write up code-review findings if a repo is in scope, and produce a single PLR-ready markdown document.

The output is a single file named `Model Security Review - <ModelName>.md` that follows the internal AMC Corp Model Security Review format. It leads with an executive summary of security recommendations (so PLR readers see findings first), then provides full context - model identity, scope, training data, infrastructure, security testing, open questions, and code-review advisories — using the exact heading hierarchy PLR reviewers expect.

## When the skill triggers

The skill fires automatically on phrases like:
* "security review for model X"
* "model security review"
* "review this model"
* "model security assessment"

Or when you give a Hugging Face URL, arXiv paper, or model repo and ask for a security read.

## What it produces

A single markdown file with this top-level structure:

# Model Security Review - <ModelName>

| Section | Description |
| :--- | :--- |
| **Review Metadata** | (authors, work item, PLR ID, links) |
| **Revision History** | (table) |
| **Security Recommendations** | (executive summary at the top) |
| **Overview** | (capabilities + intended use cases) |
| **Scope** | (model name, base, architecture, adopters) |
| **Product Usage** | (who consumes it, regions, API) |
| **Model Development & Training** | (datasets, synthetic data, compute) |
| **Model Attestation** | (SHA-256 of weights) |
| **Infrastructure** | (training and inference environments) |
| **Security Controls** | (safety datasets, adversarial testing) |
| **Questions** | (open questions back to engineering) |
| **Code Review** | (per-finding Advisory blocks) |

The Security Recommendations section is deliberately placed at the top — before the Overview — so engineering and PLR readers see findings first without scrolling. Findings are ordered by severity and each contains a Gap / Question / Recommendation triplet.

## The five-phase workflow

### Phase 1 - Intake & Scoping (5-10 min)
Collects the canonical references:
* Model card / Hugging Face URL or paper
* Internal rollout doc
* Code repo
* Work item + PLR ID

If a prior Model Security Review exists for a related model, the skill reads it first to pick up house style and prior context. It also confirms scope: code-review-included or doc-review-only.

### Phase 2 - Information Extraction (15-30 min)
In parallel, fetches and extracts:
* **arXiv / Hugging Face / public GitHub** via WebFetch - architecture, parameter count, training corpus, license, stated limitations, model attestation hashes.
* **Internal docs** (Google Docs, Confluence, GUS) - WebFetch will 401 on these; the skill instead asks the user to paste excerpts or download as markdown.
* **Code repos** - clones or reads locally to identify inference/serving entrypoints, authentication on endpoints, input validation, sandbox isolation (Dockerfile, container flags), and resource limits.

It tracks every gap as it goes — these become the "Questions" section in the final document.

### Phase 3 - Threat Analysis (20-40 min)
Walks a checklist of threat categories scoped to the model type. The skill ships with `references/threat-categories.md` which covers:

**Universal (every model):**
* Resource exhaustion / denial of wallet
* Supply chain (weight integrity, dependency CVEs, license compatibility)
* Tenant isolation
* Input validation (fail-early, hyperparameter bounds, payload caps)
* Infrastructure (mTLS, secrets management, audit logging)

**Numerical/time-series models:**
* Adversarial robustness (PGD, FGSM, frequency-domain, transfer, poisoning)
* Output bounds (forecast clamping, flat-line detection)

**LLM/generative text:**
* Prompt injection (direct, indirect via RAG, tool-output)
* Jailbreak resistance, refusal training
* Data leakage / memorization, PII
* Harmful content (CSAM, weapons, malware, bioweapons)
* Tool use / agent risks

**Multimodal:**
* Adversarial perturbations on images, image-based prompt injection
* Adversarial audio, voice cloning

**Agent/tool-calling systems:**
* Sandbox isolation (USER directive, capabilities, network, resource limits, seccomp)
* Tool endpoint security (auth, schema validation, audit logs)
* Privilege escalation paths

**Red-flag patterns to always flag:**
* `Action: "*"`/`Resource: "*"` IAM
* `0.0.0.0/0` ingress on management ports
* `USER root` in production Dockerfiles
* HTTP services on `0.0.0.0` instead of `127.0.0.1`
* `eval()`, `exec()`, `pickle.load()` on network input
* No timeouts/no payload caps on `/execute`-style endpoints
* Hardcoded secrets

For each category the skill marks: applicable / not applicable / needs more info, and identifies the gap.

### Phase 4 - Code Review Findings (optional, 30-60 min)
Triggered only when code is in scope. The skill ships with `references/code-review-checklist.md` covering:
* **Inference / serving endpoints** - auth, network binding (127.0.0.1 default), input validation, rate limiting, timeouts, audit logging.
* **Sandbox / code execution services** - endpoint auth, Dockerfile hygiene (USER directive, minimal base, multi-stage builds), runtime flags (`--read-only`, `--cap-drop=ALL`, `--security-opt no-new-privileges`, `-pids-limit`, `--memory`, `-cpus`, `--network=none`, seccomp), code-execution safety (no eval/exec/pickle.load on untrusted input).
* **Configuration & secrets** - no hardcoded keys, vault/parameter store usage, `.env` in `.gitignore`.
* **Dependencies** - pinned versions, CVE audit, license audit, no deprecated crypto.
* **Model loading** - trusted source, hash verification, no `weights_only=False` on untrusted checkpoints.

Each finding becomes an Advisory block:
```markdown
## Advisory N <title>
Severity: Critical | High | Medium | Low
Status: Open
Owner: <team>

### Impact
<what the attacker gains, blast radius>

### Attack Preconditions
- <conditions>

### Evidence
- <file/line>

### Recommended Remediation
1. <step>
2. <step>

### Verification
<how to test>
```
The skill ships two pre-written Advisory templates for the most common findings: "Unauthenticated execution endpoint" and "Weak container isolation."

### Phase 5 - Document Generation
Reads `templates/model-security-review-template.md` (a full skeleton with placeholders for every section), fills in every field from the gathered data, and saves the document.

**Conventions enforced at this phase:**
* Filename: `Model Security Review - <ModelName>.md`
* Top heading: `# **Model Security Review \- <ModelName>**` (escaped hyphen matches Google Docs export)
* Major sections use `### Section`
* Code Review advisories separated by `---`
* Evidence cited with file paths and line numbers
* Relative dates converted to absolute (e.g., "next quarter" → "Q3 2026")
* Unknown fields go into the Questions section, not invented

## Required inputs

The skill prompts in batches (not all at once) for these. If you provide docs/links, it extracts from them first and only asks about what's missing.

### Identity & Ownership
* Internal model name (e.g., Moirai-2.0-R-Small)
* Base model / predecessor
* Architecture type (decoder-only transformer, diffusion, etc.)
* Feature-owning team
* Engineering Slack handles
* Reviewer name(s)
* Work item ID, PLR ID

### Resources
* Paper URL (arXiv)
* Blog post URL
* Model URL (Hugging Face, internal registry)
* Code repo URL or local path
* Internal rollout doc URL
* Slack thread URL

### Use Case & Scope
* Intended use cases
* Primary adopters (data scientists, end users, agents)
* External access plans (open-source, customer-facing, internal-only)
* Regions (Global / US-only / regulated)
* API compatibility (Python, REST, gRPC)
* Input/output modality

### Training & Data
* Public datasets used
* Synthetic data generation method (KernelSynth, mixup, etc.)
* Internal/proprietary data used
* Training corpus size, training method
* Training compute (GPUs, hours, region)
* Model attestation (SHA-256 hash from model card)

### Infrastructure
* Training and inference environments (hardware, cloud, region, precision)
* Endpoint convention (gRPC UDF, REST, internal service mesh)
* Security context (auth, mTLS, IAM, tenant isolation)
* Rollout safeguards (feature flags, dialect allowlists, kill switches)

### Performance & Limits
* Latency SLAs and benchmarks
* Accuracy/quality benchmarks (MASE, CRPS, MMLU, etc.)
* Hardcoded input/output limits
* Timeouts, hyperparameter validation behavior

### Security Testing
* Adversarial testing performed (PGD, frequency-domain, jailbreaks, prompt injection)
* Safety/red-team datasets
* Known vulnerabilities and limitations
* Results (effective / partially effective / ineffective)

### Code to Review (if in scope)
* Path to inference/serving code
* Path to sandbox / agent execution code
* Dockerfile / deployment config paths

## Files in the skill

```text
model-security-review/
  SKILL.md # The skill definition + workflow
  templates/
    model-security-review-template.md # Full document skeleton with placeholders
  references/
    threat-categories.md # Phase 3 checklist by model type
    code-review-checklist.md # Phase 4 checklist + Advisory templates
    README.md # This documentation file
```

## Guardrails - what the skill will NOT do

* **No invented findings.** Every claim must be grounded in the provided materials or actual code inspection. The skill explicitly refuses to fabricate vulnerabilities, remediations, or attack chains.
* **No invented metrics.** Latency, accuracy, parameter counts, training compute - if it's not in the source materials, it goes into the Questions section, not the body.
* **No skipping the Questions section.** Open questions back to engineering are a deliverable, not a failure. A review with documented unknowns is more useful than a review with confidently wrong assumptions.
* **No silent commits.** The skill will not push the review to a public repo without explicit instruction.

## Example invocations

**Full review with all materials:**
> "Do a model security review for Moirai-2.0-R-Small. Paper: arxiv.org/abs/2511.11698, model: huggingface.co/amccorp/moirai-2.0-R-small, code: github.com/AMC-Corp-Research/uni2ts, work item W-21354707, PLR-008318."

**Doc-only review:**
> "I have the rollout doc for AgentCore-LLM-v2. Can you draft the security review document? I'll paste the doc contents."

**Update existing review:**
> "Update the Moirai security review with new findings from the code review of project/moirai-agent."

## Typical output footprint

For a full review with code, expect:
* ~700-1500 lines of markdown
* 5-10 Security Recommendations (executive summary)
* 4-8 Code Review Advisories (each with Impact / Preconditions / Evidence / Remediation / Verification)
* 8-15 open Questions back to engineering
* Filled-in metadata table, scope, data lineage, infrastructure, attestation status

A doc-only review (no code in scope) typically lands at half that length, with the Code Review section reduced to a single line noting it was out of scope.

## How it integrates with the rest of the harness

* Uses `WebFetch` for public references (arXiv, HuggingFace, public GitHub).
* Uses `Read` / `Bash` (grep, find) for local code inspection.
* Uses `TaskCreate` / `TaskUpdate` to track each phase as a discrete task.
* Uses `AskUserQuestion` for batched scoping questions when context is missing.
* Writes the final document with `Write`.

## When NOT to use it

* **Generic security questions about a model that isn't being deployed** ("is GPT-4 safe?") - that's a research question, not a PLR review.
* **Code reviews that aren't model-related** - use the regular code-review skill instead.
* **Threat-modeling exercises for systems where the model is incidental** - use the security-review skill on the change set instead.
* **Production incident response** - this skill is pre-deployment.

## Limitations

* The skill does not run dynamic analysis (no live exploitation attempts, no fuzzing).
* It does not run dependency CVE scanners (pip-audit, osv-scanner) or static analyzers (semgrep, bandit) automatically - those need to be invoked separately.
* Internal authenticated URLs (Google Docs, Confluence, GUS) require the user to paste excerpts; WebFetch will return 401.
* For very large repos, the skill scopes the code review to security-sensitive paths (inference, serving, sandbox, agent execution) rather than enumerating every file. Anything skipped is noted as residual risk.
