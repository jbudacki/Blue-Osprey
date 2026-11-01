# AI threat model report schema

Use this reference for a formal or exportable report. A short review can keep the same evidence fields in prose. Do not fill blank rows merely to make a table look complete.

## Report outline

1. **Scope and basis:** Intended use, system boundary, reviewed artifacts with dates/versions, assumptions, exclusions, confidence, and consequential unknowns.
2. **System model:** Assets and affected people; actors and identities; components; data- and control-plane flows; trust boundaries; lifecycle stages; applicable STRIDE categories and MAESTRO layers.
3. **Action authority ledger:** For side-effecting agent actions, record principal, delegated principal, scope, expiry, enforcement, approval, revocation, attribution, and recovery. Mark each control implemented, proposed, absent, or unknown.
4. **Risk register:** One entry per distinct scenario and consequence. Security threats and broader AI impacts may share a document but must have a clear type and owner.
5. **Coverage and decisions:** Applicable categories/layers assessed, those with no identified path, treatment priorities, accepted residual risk only when an authorized owner has actually accepted it, and open questions.
6. **Verification plan:** Safe tests or evidence requests linked to risk IDs. Distinguish performed checks from proposed checks.

If the user requests a full STRIDE or MAESTRO report, preserve the existing generator's required sections and matrices. Add the deduplicated register as a synthesis or crosswalk; do not replace required framework sections or repeat the same scenario as independent findings.

## Risk-register fields

| Field | Record |
| --- | --- |
| ID, type, title | Stable ID; `security threat` or `broader AI impact`; plain-language failure mode. |
| Evidence/status | Exact artifact, code path/line, diagram element, or statement; `observed`, `plausible from architecture`, or `hypothesis`. A research paper alone is a lead. |
| Actor and entry point | Who can influence the source; how it reaches the system. |
| Source-to-sink path | Every material trust crossing, model/agent behavior, enforcement point, and final action or decision. |
| Asset/outcome | Affected data, system, person, or business process; harm and blast radius. |
| Preconditions/false positives | What must be true, contrary evidence, and key unknowns. |
| Current controls/gap | Verified implementation and its limit; distinguish proposed controls. |
| Impact/likelihood/confidence | Separate qualitative judgments with explicit reasoning; use organization scoring if supplied. Unknown is not low. |
| Treatment/owner | Prevent, limit, detect, or recover; accountable owner; residual risk and tradeoffs. |
| Verification | Specific synthetic, mock, staging, or evidence check; performed result or `proposed`. |
| Cross-references | Applicable STRIDE category, MAESTRO layer(s), verified ATLAS link, relevant PLOT4AI domain, and optional primary research link. |

Prioritize by credible impact, reachable attack surface, attacker prerequisites, implemented controls, detectability, and uncertainty. Avoid numeric precision when no organizational rubric exists. A high-impact but unverified path can be a high-priority investigation without being a confirmed vulnerability.

## Worked synthetic example

**Scenario TM-AI-01 — Retrieved document influences an outbound tool.** This example is a hypothesis about a made-up agent, not a finding about a real deployment.

| Field | Example entry |
| --- | --- |
| Type/status | Security threat; hypothesis pending permissions and retrieval evidence. |
| Actor/entry | External collaborator can edit a document in a corpus available to the agent. |
| Path | Corpus write → retrieval → model context → model-generated tool arguments → outbound tool → external endpoint. The document-to-context and context-to-tool boundaries are separate. |
| Preconditions | The document is retrievable; the agent can read confidential content; the outbound tool can reach the endpoint; independent policy or approval does not deny the action. None is assumed proven. |
| Outcome | Unauthorized disclosure of content available to the agent. |
| Current control/gap | Unknown until corpus ACLs, tenant filtering, tool policy, token scope, and approval behavior are inspected. |
| Treatment | Restrict corpus writes, preserve provenance and tenant boundaries, enforce destination and data-class policy at the tool, scope credentials, and require exact-action approval for high-impact export. |
| Verification | In a mock or staging system, insert a synthetic document, use fake confidential content and a mocked destination, and check that the call is denied and attributed. |
| Cross-references | STRIDE Tampering/Information Disclosure; MAESTRO Data Operations/Agent Frameworks/Security and Compliance. Add an ATLAS technique only after checking a specific current entry. |

Do not turn this example into a default finding in every RAG review. If the agent has no outbound tool, the described sink does not exist; model any remaining output-manipulation risk separately.
