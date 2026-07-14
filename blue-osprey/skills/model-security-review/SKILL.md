---
name: model-security-review
description: "Conduct structured security reviews of AI or ML models before deployment, adoption, or a security approval decision. Use when reviewing a model card, research paper, rollout document, serving code, third-party model, open-source model, or production AI/ML deployment for security risk."
---

# Model Security Review

## Purpose

Conduct a structured security assessment of an AI/ML model and produce a standardized Model Security Review document suitable for an engineering hand-off and an authorized deployment or adoption decision.

Use the AMC Corp name only as a replaceable organization placeholder when a template requires one. Do not assume any specific review program, approval process, tool, model registry, cloud, collaboration platform, or agent harness.

## Inputs to Gather

Extract facts from provided materials before asking for missing information. Ask in small batches and collect only fields relevant to the review.

### Identity and Ownership

- Model name and version
- Base model or predecessor
- Architecture type
- Owning team and engineering contacts
- Reviewer name
- Work item and approval or decision record, if applicable

### Resources

- Model card or registry record
- Research paper or technical report
- Source repository or local code path
- Rollout or deployment document
- Relevant decision or collaboration record

### Use Case and Scope

- Intended use cases and primary adopters
- Access model: public, customer-facing, partner, or internal
- Deployment regions and regulatory constraints
- Input and output modalities
- Interface types, such as library, API, batch job, or embedded component

### Training and Data

- Public, licensed, synthetic, proprietary, or regulated datasets used
- Data provenance, consent, retention, and deletion constraints
- Training corpus size and method
- Training compute and location when relevant
- Model artifact digest and verification process

### Infrastructure

- Training and inference environments
- Endpoint and service topology
- Authentication, authorization, encryption, and tenant isolation
- Rollout safeguards, monitoring, rollback, and kill switches

### Performance and Limits

- Latency and quality benchmarks
- Input, output, batch, token, row, and payload limits
- Timeouts, quotas, and concurrency controls
- Parameter and schema validation behavior

### Security Testing

- Applicable adversarial, abuse, privacy, and safety testing
- Evaluation datasets and coverage
- Known vulnerabilities and limitations
- Results and unresolved gaps

### Code to Review

- Inference and serving code
- Tool, sandbox, or agent execution code when applicable
- Build, container, infrastructure, and deployment configuration

## Workflow

Follow these phases in order. Tailor the depth to the model type, deployment context, data sensitivity, and requested scope.

### Phase 1 - Intake and Scoping

1. Identify the canonical model, architecture, deployment, and code references.
2. Confirm the decision being supported, the authorized reviewer or risk owner, and any governing criteria.
3. Confirm whether code review, architecture review, dynamic testing, or documentation review is in scope.
4. Classify the data before using external tools or connectors. Do not send confidential or regulated material to an external service without authorization.
5. Read any prior review only for relevant context, accepted risks, and local document conventions.

### Phase 2 - Information Extraction

1. Use available, approved tools to inspect public references and extract architecture, parameter count, training data claims, license, stated limitations, and artifact digests.
2. Access authenticated internal material only through an approved connector or user-provided local copy. Do not assume an authentication failure or prescribe a particular document platform.
3. For code repositories, inspect locally when possible and identify:
   - inference and serving entry points
   - authentication and authorization boundaries
   - input and output validation
   - sandbox or workload isolation
   - quotas, timeouts, and payload limits
   - model loading and artifact verification
4. Record sources, unsupported claims, conflicts, and open questions as the review proceeds.

### Phase 3 - Threat Analysis

Read `references/threat-categories.md`. Mark each relevant category as applicable, not applicable, or needs more information, and document the evidence supporting that status.

At minimum consider:

- resource exhaustion and cost abuse
- model and software supply chain
- tenant and data isolation
- input and output validation
- infrastructure trust boundaries
- adversarial robustness appropriate to the modality
- privacy, extraction, inversion, and memorization
- prompt injection, unsafe tool authority, and retrieval poisoning for agentic or generative systems

### Phase 4 - Code Review Findings

When code is in scope, read `references/code-review-checklist.md`. Report a finding only when there is a demonstrated source-to-sink or control-failure path. Include:

- severity and confidence
- affected component and owner
- impact and blast radius
- attack preconditions and trust boundary
- file-and-line evidence
- exploitability and false-positive considerations
- recommended remediation
- verification steps
- open questions

Do not elevate a generic checklist signal into a vulnerability without deployment context and a demonstrated path.

### Phase 5 - Document Generation

1. Read `templates/model-security-review-template.md`.
2. Retain applicable sections and remove inapplicable placeholders; do not force every review into the same shape.
3. Place Security Recommendations near the top and order them by risk and decision relevance.
4. Put unresolved facts in Questions or Unknowns rather than guessing.
5. Distinguish findings, observations, accepted risks, and recommendations.
6. Record the authorized decision owner and approval record only when they exist.
7. Save to the user's chosen location. Default to `Model Security Review - <ModelName>.md` in the current working directory.

## Output Conventions

- Top-level heading: `# Model Security Review - <ModelName>`
- Use absolute dates where ambiguity matters.
- Cite public claims with normal links and code findings with file paths and line numbers.
- Label unsupported statements as claims or open questions.
- Do not include internal extraction markers, citation IDs, or citation-processing artifacts.
- Do not expose secrets, credentials, personal data, or confidential material in the report.

## Example Invocations

- "Review Forecast-Small-v2 for a proposed internal batch deployment. I have a model card, architecture note, and local serving repository."
- "Assess whether we should adopt this third-party image model and produce a decision-ready security review."
- "Update the existing model security review with verified findings from the serving-code changes."

## Do Not

- Do not invent findings, vulnerabilities, metrics, sources, or remediations.
- Do not assume a specific approval framework or that security owns the launch decision.
- Do not access protected systems or validate vulnerabilities against live services without explicit authorization.
- Do not publish or commit the review without explicit instruction.
