# [Risk: Brief descriptive title]

Use this template to structure every risk retrospective. Fill in all sections. Replace placeholder text in [brackets] with actual content. Remove the bracketed instructions after filling in. The H1 heading above serves as the document title - do not repeat it in the header table.

| Field | Value |
| :--- | :--- |
| Date | [YYYY-MM-DD] |
| Author | [Name, Role] |
| Overall Severity | [Low / Medium / High / Critical] |
| Status | [Draft / In Review / Final / Superseded] |
| Tracking | [work item (W-XXXXXX) or other case/ticket IDs] |
| Decision Deadline | [YYYY-MM-DD - when a decision must be made] |

## Executive Summary
[3-5 sentences. What is the risk? What's the business context? What do you recommend? What happens if we do nothing? This section must stand alone - a VP reading only this paragraph should understand the situation and the ask.]

## Background and Business Context
[1 paragraph, 3-5 sentences. What feature, project, or customer need created this situation? Why does the business care? Include revenue impact, customer commitments, or compliance requirements if relevant.]

## Risk Assessment

| Dimension | Rating | Rationale |
| :--- | :--- | :--- |
| Likelihood | [Low/Medium/High/Critical] | [1 sentence explaining why] |
| Technical Impact | [Low/Medium/High/Critical] | [1 sentence explaining why] |
| Business Impact | [Low/Medium/High/Critical] | [1 sentence explaining why] |
| Overall Severity | [Low/Medium/High/Critical] | [1 sentence explaining derivation] |

### Existing Mitigating Controls:
* [Control 1 - what it does and how effective it is]
* [Control 2]
* [Control 3 - if applicable]

## Security Implications
[Numbered list of 3-5 specific risks. Each item: 2-3 sentences describing the risk and the attack vector or failure mode. Be specific - "attacker could X via Y" not "there are security concerns."]

1. [Risk Name] - [Description of the specific risk, how it could be exploited or triggered, and what the impact would be.]
2. [Risk Name] - [Description.]
3. [Risk Name] - [Description.]

## Timeline
[Only critical milestones: risk discovery/raised, case/ticket creation or status changes, escalations, incidents, key decisions. 5-8 bullets max. Do NOT include minor artifact updates, comment edits, or incremental document revisions. Every entry must have a date.]

* YYYY-MM-DD - [Risk discovered or raised]
* YYYY-MM-DD - [Case/ticket created or escalated]
* YYYY-MM-DD - [Key decision or incident]
* YYYY-MM-DD - [Upcoming deadline or decision point]

## Options and Recommendations

| Aspect | Option 1: [Name] | Option 2: [Name] | Option 3: Accept the Risk |
| :--- | :--- | :--- | :--- |
| **Description** | [What this option entails] | [What this option entails] | Proceed without changes; document accepted risk |
| **Pros** | [Key advantages] | [Key advantages] | No engineering cost; no timeline impact |
| **Cons** | [Key disadvantages] | [Key disadvantages] | [Residual risk remains unmitigated] |
| **Effort** | [T-shirt size or sprint estimate] | [Estimate] | None |
| **Residual Risk** | [What risk remains after this option] | [Residual risk] | [Full current risk] |

## Security Directive
[3-5 sentences. State what the security team believes is the right path and why, based on the evidence above. Name the recommended option and explain why it best balances security risk against business needs. This is the one place where opinions are allowed - be direct and decisive.]

## Decision Log
[Leave empty. This section gets filled in after stakeholders read the document and make decisions.]

## References and Artifacts
* W-XXXXXXXX - ticket title
* [Internal doc title and link]
* [Slack Channel and link]
* [OWASP reference, e.g., OWASP Top 10 A01:2021 Broken Access Control]
* [NIST reference, e.g., NIST SP 800-53 AC-6]
* [CWE reference, e.g., CWE-285: Improper Authorization]
