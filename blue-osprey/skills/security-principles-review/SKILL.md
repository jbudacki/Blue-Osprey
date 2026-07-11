---
name: security-principles-review
description: "Evaluate security decisions, proposals, architecture designs, processes, and security team operating models against the Security Core Principles rubric. Use when Codex reviews org designs, engagement models, security charters, decision docs, security strategies, or team workflows for principle alignment and anti-patterns."
---

# Security Principles Review

## Why This Approach

Security organizations fail in predictable ways: rubber-stamping reviews, blocking without alternatives, and spreading thin across low-risk work. This skill uses a dual-axis rubric--separate principle alignment from anti-pattern detection--to catch these failure modes early.

## Before You Begin

Familiarize yourself with the scoring criteria:

- [references/principles.md](references/principles.md) -- Detailed definitions of the 7 Core Principles and 6 Anti-Patterns.

## Identify the Subject

Determine the type of subject being reviewed:
- **Decision**: A specific security choice (e.g., "require MFA for admin access").
- **Design**: Architecture or technical proposal (e.g., threat model, RFC).
- **Process**: Operating model or workflow (e.g., triage process).
- **Operating Model**: How a security org structures its engagement with engineering.

If a document is provided, read it thoroughly. If described conversationally, summarize your understanding back to the user before proceeding with the review.

## Evaluation Workflow

### 1. Core Principles Alignment (7)
For each principle in `references/principles.md`, assign a rating:
- **Strong Alignment**: Clearly embodies the principle with concrete evidence.
- **Partial Alignment**: Some elements present, but gaps exist.
- **Not Demonstrated**: Neither supports nor conflicts.
- **Conflict**: Actively works against the principle.

### 2. Anti-Pattern Detection (6)
For each anti-pattern in `references/principles.md`, assign a flag:
- **Clear**: No indication observed.
- **At Risk**: Elements suggest it could emerge.
- **Present**: Actively exhibited.

## Producing the Verdict

Use the following template for your output:

```markdown
# Security Principles Review

## Subject
[Description and type: decision / design / process / operating model]

## Overall Verdict
[**Aligned** / **Partially Aligned** / **Misaligned**]
[1-2 sentence summary reasoning.]

## Principle Scorecard

| Principle | Rating | Justification |
|-----------|--------|---------------|
| Secure by Default | [rating] | [evidence] |
| Constructive Friction | [rating] | [evidence] |
| Shift Left & Shield Right | [rating] | [evidence] |
| Risk-Based Pragmatism | [rating] | [evidence] |
| Intelligence Feedback Loop | [rating] | [evidence] |
| Partnership over Policing | [rating] | [evidence] |
| Transparent Criteria | [rating] | [evidence] |

## Anti-Pattern Check

| Anti-Pattern | Flag | Evidence |
|--------------|------|----------|
| Compliance Theater | [flag] | [evidence or "None observed"] |
| Manual Stop-Gap | [flag] | [evidence or "None observed"] |
| Proxy for Product Context | [flag] | [evidence or "None observed"] |
| Department of No | [flag] | [evidence or "None observed"] |
| One-Size-Fits-All Bureaucracy | [flag] | [evidence or "None observed"] |
| Throw It Over the Wall | [flag] | [evidence or "None observed"] |

## Strengths
- [Specific strengths tied to principles]

## Recommendations
- [Actionable changes referencing principles or anti-patterns addressed]
```
