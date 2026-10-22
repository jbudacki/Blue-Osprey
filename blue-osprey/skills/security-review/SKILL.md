---
name: security-review
description: "Route and structure security reviews. Use for application security review, AI security review, vulnerability triage, secure code review, authn/authz review, prompt-injection review, MCP/tool boundary review, dependency risk review, or when asked whether code is exploitable. Activates specialized Blue-Osprey skills when needed, including MCP assessment and evidence-map workflows."
---

# Security review router

Use this skill as the front door for security work. It provides scope control, evidence requirements, and a routing table for the specialized skills installed with this pack.

## Inputs to establish

- Authorized scope and target environment.
- Files, diff, branch, commit, issue, architecture, model, or finding being reviewed.
- Relevant data classes, trust boundaries, identities, roles, external systems, and MCP/tool permissions.
- Whether validation may run commands, start services, make network calls, or call external APIs.

## Routing

| Need | Skill |
| --- | --- |
| Understand an unfamiliar repo before choosing review depth | `$codebase-discovery` |
| Cross-cutting secure code review of pull requests, diffs, commits, files, or repositories | `$secure-code-review` |
| Hardcoded credentials, tokens, private keys, config leakage | `$secrets-analysis` |
| LLM apps, RAG, prompt injection, tools, agents, model output authority | `$llm-security` |
| AI/ML model deployment, model cards, serving, model supply chain | `$model-security-review` |
| AWS IAM, trust policies, wildcard permissions, role escalation | `$iam-security` |
| Public network exposure, security groups, public databases, VPC boundaries | `$network-exposure` |
| Crypto implementations, hashing, signing, certificates, key management | `$crypto-analysis` |
| Dependency manifest or lockfile supply-chain risk | `$3pp-dependency-hygiene` |
| MCP connection classification, checklist, evidence gaps, or security decision | `$mcp-security-review` |
| Formal general-system threat model | `$threat-model-generator-stride` |
| Formal agentic-AI/RAG/MCP threat model | `$threat-model-generator-maestro` |
| Security decision memo or accepted-risk retrospective | `$risk-retrospective` |
| Org/process/security strategy principle review | `$security-principles-review` |
| Generated-code risk in Python | `$vibe-code-detection` |
| Convert completed findings or remediation actions into an engineering and SOC evidence handoff | `$security-evidence-map` |

Use only the skills needed for the task. Do not load multiple deep skills just because they exist.

## Method

1. Define scope. If the target is live, third-party, production, customer-facing, or outside the repo, confirm authorization before validation.
2. Map entry points, trust boundaries, assets, identities, and sinks.
3. Route code-level reviews through `$secure-code-review`. Add other specialists
   only when the evidence surface matches their trigger; use them to supplement,
   not duplicate, the cross-cutting review.
4. Route package-specific MCP connection assessments through
   `$mcp-security-review`. Use `$threat-model-generator-maestro` instead
   when the requested deliverable is a formal agentic-AI or MCP threat model.
5. Trace source-to-sink paths. Do not report a finding without a plausible path and preconditions.
6. Prefer safe proof over exploit detail. Do not provide offensive steps for systems outside authorized scope.
7. Recommend the smallest fix that removes the path, then name verification steps.
8. When the user requests an evidence map, remediation or SOC handoff, or the
   review concerns active threat activity, route stabilized findings and actions
   through `$security-evidence-map`. The map supplements the review and must not
   silently change its findings, severity, confidence, or disposition.

## Finding format

```text
Finding: <name>
Severity: <Critical|High|Medium|Low|Info>
Confidence: <High|Medium|Low>
Evidence:
- <file:line> <relevant code or behavior>
Entry point: <where attacker/user input enters>
Source-to-sink path: <path summary>
Trust boundary: <boundary crossed>
Preconditions: <required state/role/config>
Impact: <what can happen>
Exploitability notes: <constraints without unsafe detail>
False-positive considerations: <why this might not be exploitable>
Recommended fix: <specific change>
Verification: <test/manual check/tool command>
Open questions: <unknowns>
```

For unconfirmed concerns, label them as hypotheses and state what evidence is missing.
