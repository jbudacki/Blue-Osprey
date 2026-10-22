# Evidence map examples

These examples illustrate structure only. Replace every identifier, reference,
and evidence statement with verified material from the current task.

## Finding-first example

A completed review contains a finding that an externally reachable API route
lacks server-side authorization. The evidence map derives an action and keeps
source confirmation separate from operational confirmation.

| ID | Action | Where to point | Evidence shown | Source → sink / impact | SOC evidence to collect | Status |
|---|---|---|---|---|---|---|
| SR-04 | Enforce server-side authentication and object authorization on the document route; add negative authorization tests. | `security-review.md`, finding SR-04; `src/routes/documents.ts:42`; `tests/documents-auth.test.ts` | The route invokes the document controller without authentication middleware, and no negative authorization test covers the route. | Anonymous request → document controller → document store. Preconditions: route is externally reachable. Impact: unauthorized document access or modification. | API gateway and application events for the route, including timestamp, principal, source address, object ID, response status, and request ID. Correlate anonymous or mismatched identities with successful responses. | `Confirmed in source — operationally unverified — open` |

## Action-first example

A posture review identifies that several inventory sources have not been joined
into an ownership and approval register. There is no meaningful technical
source-to-sink path, so the map states the assurance gap instead.

| ID | Action | Where to point | Evidence shown | Source → sink / impact | SOC evidence to collect | Status |
|---|---|---|---|---|---|---|
| EM-001 | Reconcile cloud inventory, software inventory, source repositories, and the CMDB into an owner-approved register. | `posture-review.md`, Inventory section; named cloud and CMDB exports | Separate inventories identify assets and components, but the supplied artifacts contain no joined owner, purpose, environment, approval, and retirement record. | Not applicable. Assurance gap: security and lifecycle decisions cannot be reliably assigned or evidenced for all assets. | Obtain current inventory exports and authoritative ownership records; compare stable asset identifiers and identify orphaned or conflicting records. | `Evidence gap confirmed — action open` |

## What not to do

Do not convert this:

```text
Collect WAF logs for suspicious requests.
```

into this unsupported status:

```text
Confirmed exploited.
```

The collection request identifies evidence that is still needed. Until relevant
telemetry is supplied and correlated, use a source-confirmed, conditional, or
hypothesis status as appropriate.
