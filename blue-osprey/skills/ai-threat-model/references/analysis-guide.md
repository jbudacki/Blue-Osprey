# AI threat modeling analysis guide

Read this reference when mapping an AI architecture or preparing a review discussion. Select prompts that fit the system; an absent component does not need a threat entry. Record each answer as observed, stated but unverified, absent, or unknown.

## 1. Bound the system

- What is the intended decision or action, who uses it, and who can be harmed by a wrong or unauthorized outcome?
- Which lifecycle stages are in scope: data selection, training/tuning, evaluation, deployment, inference, monitoring, retirement?
- Which facts came from code, configuration, diagrams, interviews, or external material? Which controls are only proposed?
- What is explicitly out of scope? Which missing facts would change the top risks?

## 2. Map components and flows

Inventory relevant users, administrators, providers and models, application and orchestration code, system/developer prompts, training data, retrieval corpus/index/vector store, connectors, short- and long-term memory, tools and APIs, runtime identities, policy decision/enforcement points, approval UI, logging/evaluation, and external vendors.

For each flow, capture `source → destination`, data type, owner, trust level, transformation, persistence, and whether the flow can change an instruction, policy, decision, or action. Draw separate data-plane and control-plane flows. The control plane includes prompt templates, model/version selection, connector and tool scopes, memory-write rules, approvals, policies, deployment, and evaluation settings.

Pay particular attention to these boundary crossings:

- External data or a lower-trust user message enters model context or a training set.
- Retrieved text, image, audio, tool response, or peer-agent message is promoted from **data** into an **instruction**.
- Model output becomes code, a query, a file, a tool argument, a policy/configuration update, or a persistent memory entry.
- A model-selected action reaches a tool or API holding a more privileged credential.
- One tenant's content, embeddings, memory, or credentials become visible to another.
- An evaluation result or safety signal changes a deployment or approval decision.

For each candidate scenario, write a concrete path: `actor/control of source → entry point → trust boundary → system behavior → enforcement point → action or decision → asset/person/outcome`. State the preconditions and a plausible benign explanation. A technique name without this path is an investigation prompt, not a finding.

## 3. Choose analysis lenses

| System | Apply |
| --- | --- |
| Conventional app that calls an AI API | STRIDE on app/provider boundaries; targeted AI input, output, and data-sharing questions. |
| Predictive ML or custom training/tuning | STRIDE on pipeline/deployment; data/model provenance, integrity, privacy, evaluation, and relevant PLOT4AI prompts. |
| RAG or read-only copilot | Relevant MAESTRO model/data/framework layers; STRIDE on retrieval authorization, tenant separation, and host app. Do not invent tools or agent actions. |
| Tool-using or autonomous agent | Applicable MAESTRO layers and cross-layer interactions; STRIDE on tool hosts and IAM; action-authority ledger below. |
| Multi-agent workflow | Above plus peer identity, message integrity, transitive delegation, cascading effects, and recovery. |

The seven MAESTRO layers are foundation models, data operations, agent frameworks, deployment and infrastructure, evaluation and observability, security and compliance, and agent ecosystem. Assess applicability, including cross-layer interactions, without demanding a threat per layer. See [CSA MAESTRO](https://labs.cloudsecurityalliance.org/maestro/) and the [CSA layer description](https://labs.cloudsecurityalliance.org/agentic/agentic-secure-development-lifecycle-v1/). For STRIDE, use the existing generator's six categories and its evidence rule. For a mixed system, use one scenario per consequence with multiple framework tags rather than duplicate findings.

## 4. Record action authority

Create one row per tool/action class with side effects, even when its use is only proposed. Capture:

| Question | Evidence to seek |
| --- | --- |
| Who makes the call? | Verifiable runtime/workload identity, peer authentication, and impersonation resistance. |
| On whose behalf? | Authenticated human or service principal and actual delegation mechanism; prompt text alone is not delegation. |
| What is allowed? | Actions, resources, tenants, destinations, data classes, and downstream delegation scope. |
| How long? | Credential issuance, storage, expiry, rotation, and run/session binding. |
| Where is it enforced? | Tool/API or gateway policy decision on each action, independent of model output. |
| Who approves? | Which high-impact actions require approval and whether approval binds exact parameters and destination. |
| How does it stop? | Revocation behavior during a run, including queued and in-flight actions; emergency stop where applicable. |
| What remains observable? | Attribution, audit, alerting, and recovery without unnecessary secret or sensitive-prompt logging. |

Do not credit a named identity/delegation product as a working control without deployment evidence and an enforcement test. A signed identity does not constrain a tool that accepts broader credentials. [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).

## 5. Broader AI impacts

Use selected [PLOT4AI](https://plot4.ai/how-does-it-work) questions to check data quality/governance, privacy, bias and disparate outcomes, safety and environmental effects, ethics and rights, transparency/accessibility, and accountability/oversight. Name affected people, the decision owner, and what evidence could establish the impact. Keep these items distinct from adversarial security findings. Do not infer a legal violation from a category label. Link and attribute PLOT4AI rather than copying its CC BY-SA card library into this skill.

## 6. Research to test, not research to finding

When an AI-specific mechanism or defense needs support, search the [Promptfoo LM Security Database](https://www.promptfoo.dev/lm-security-db/) by the mapped architecture and boundary. Use its filters for attack type, context (such as RAG, agents, or MCP), component, surface, impact, publication date, and evidence status. Open the linked **primary paper**. Record attacker access, tested models/versions, setup, outcome measure, limitations, and whether the proposed defense was tested. Compare these to the system under review, then define a narrow synthetic or staging test. Never transfer a paper's success rate or affected-product claim to another deployment. If the primary paper is unavailable, label the entry an unreviewed research lead.

Use [MITRE ATLAS](https://atlas.mitre.org/) to check adversary behavior and technique links for an already supported path. Verify current identifiers before citing them. ATLAS and the research database are discovery sources; neither establishes that the reviewed system has a vulnerability.

## 7. Stop conditions and confidence

Do not validate vulnerabilities against live, production, or third-party systems without explicit authorization and scope. When a path depends on unknown corpus ownership, permissions, tool reachability, or enforcement, mark it a hypothesis and ask for that evidence. State confidence separately from impact and likelihood. Recommend a falsifiable check for each material gap.
