---
name: threat-model
description: "Route threat modeling work. Use when asked to threat model a feature, architecture, PRD, design doc, AI agent workflow, MCP integration, data flow, auth flow, or deployment. Chooses STRIDE for general systems and MAESTRO for agentic AI/RAG/tool systems."
---

# Threat model router

Use this skill to choose the right threat-modeling workflow before loading a deeper framework skill.

## Choose the framework

- Use `$threat-model-generator-stride` for traditional applications, APIs, services, infrastructure, auth flows, deployment designs, and most system designs.
- Use `$threat-model-generator-maestro` for agentic AI systems, RAG, LLM tools, MCP servers, autonomous workflows, model orchestration, multi-agent systems, AI memory, and AI control-plane/data-plane analysis.
- If the system has both a conventional application layer and an agentic AI layer, produce a short split model: STRIDE for the application/control surfaces and MAESTRO for the AI/agent ecosystem.

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

For formal reports, switch to `$threat-model-generator-stride` or `$threat-model-generator-maestro`.
