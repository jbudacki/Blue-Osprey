---
name: threat-model
description: "Route threat modeling work for features, architectures, PRDs, data flows, deployments, and AI systems. Chooses STRIDE for conventional systems and ai-threat-model for AI/ML, RAG, tools, and agents."
---

# Threat model router

Use this skill to choose the right threat-modeling workflow before loading a deeper framework skill.

## Choose the framework

- Use `$threat-model-generator-stride` for traditional applications, APIs, services, infrastructure, auth flows, deployment designs, and most system designs.
- Use `$ai-threat-model` for AI/ML systems, RAG, LLM tools, MCP integrations, autonomous workflows, model orchestration, multi-agent systems, and AI memory. It selects relevant STRIDE and MAESTRO analysis and adds influence-to-action and authority review.
- If the system has both conventional and AI layers, use `$ai-threat-model` to coordinate a single model: STRIDE for application/control surfaces and MAESTRO for applicable AI/agent layers.

Framework completeness means assessing every applicable category or layer, not forcing a fixed number of findings. Formal reports must include only evidence-supported threats and may explicitly state that none were identified for a category or layer.

## Minimum pre-work

1. Define scope, assumptions, explicit out-of-scope areas, and security goals.
2. Identify assets, identities, components, external systems, and trust boundaries.
3. Separate data plane from control plane.
4. Identify where untrusted data can become instructions, code, queries, files, tool calls, policy, or configuration.
5. Prioritize risks by impact, likelihood, detection, and fix cost.

## Output for lightweight models

```text
Scope:
Assets:
Actors:
Trust boundaries:
Data flows:
Top risks:
1. <risk> - impact, likelihood, current controls, gaps, mitigation, verification
2. <risk> - impact, likelihood, current controls, gaps, mitigation, verification
Assumptions:
Open questions:
Recommended next tests:
```

For formal conventional reports, switch to `$threat-model-generator-stride`. For formal AI reports, use `$ai-threat-model`, which calls the relevant generator skills and deduplicates their risks.
