# Evidence map schema

Use one row per actionable unit. A finding may produce several rows when the
actions have different evidence, owners, or closure criteria. A cross-cutting
action may point to several findings.

## Canonical table

| ID | Action | Where to point | Evidence shown | Source → sink / impact | SOC evidence to collect | Status |
|---|---|---|---|---|---|---|

### ID

Retain an existing finding or action ID when one exists. When several actions
derive from one finding, use a stable suffix such as `BO-03-A` and `BO-03-B`.
For inputs without IDs, assign local identifiers such as `EM-001` and explain
that they are evidence-map IDs rather than newly discovered findings.

### Action

State a concrete remediation, containment, validation, or investigation action.
Use an imperative phrase and name the affected control or asset. Do not use the
vulnerability title alone as the action.

### Where to point

Prefer references in this order:

1. Existing Blue Osprey finding ID and stable report section or line.
2. Repository, configuration, or test evidence using `path:line`.
3. A named inventory, export, dashboard, ticket, or operational artifact.

Use multiple references when no single artifact supports the row. Distinguish a
reference verified during the current task from one merely attributed to an
input report. Do not invent line numbers, anchors, dashboard names, or queries.

### Evidence shown

Explain what the cited artifact proves in factual language. Include the relevant
control failure, behavior, configuration, or documented evidence gap. Keep the
statement narrower than the impact when the evidence establishes only a
precondition.

Examples of useful distinctions:

- `The route has no server-side authentication middleware` is source evidence.
- `Threat actors exploited the route` requires operational corroboration.
- `Authentication should be added` is a recommendation, not evidence.

### Source → sink / impact

For technical findings, summarize:

```text
lower-trust source or failed control → relevant processing or boundary →
sensitive sink or security consequence

Preconditions: <material role, reachability, configuration, or identifier need>
Impact: <bounded consequence supported by the evidence>
```

For governance, inventory, or lifecycle actions without a meaningful data or
control path, use `Not applicable` and describe the decision or assurance gap
and resulting risk.

### SOC evidence to collect

Describe missing operational evidence as a collection request. When applicable,
identify:

- telemetry source, such as API gateway, WAF, identity provider, application,
  database, cloud audit, CI runner, provider usage, or host metrics;
- relevant event or behavior;
- fields needed for correlation, such as timestamp, principal, source address,
  route, object ID, response status, request ID, or provider operation;
- useful time window or triggering event; and
- the observation that would support or weaken the hypothesis.

Do not require a vendor-specific query unless the user supplies the relevant
platform and requests one. Do not include secret values or unnecessary personal
or regulated data.

### Status

Use exactly one controlled status from
[status-model.md](status-model.md). Add a short qualification after the status
only when needed to identify a specific missing artifact or validation step.

## Optional columns

Add columns only when the user or workflow needs them:

- Severity
- Confidence
- Owner
- Target date
- Verification method
- Last updated

Do not overload `Status` with owner or due-date information.

## Supporting sections

After the table, include only the sections supported by the input:

1. **Disposition** — carry forward the source review's disposition verbatim or
   clearly label a later approved change.
2. **SOC triage priorities** — order urgent collection without implying that
   lower-priority evidence is unnecessary.
3. **Evidence gaps and open questions** — list missing artifacts that could
   change reachability, impact, or closure.
4. **Validation boundary** — state which artifacts were inspected and which
   live or operational checks were not performed.
