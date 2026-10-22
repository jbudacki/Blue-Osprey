# Synthetic evidence map

| ID | Action | Where to point | Evidence shown | Source → sink / impact | SOC evidence to collect | Status |
|---|---|---|---|---|---|---|
| SR-04-A | Enforce document authorization. | [SR-04](review.md#sr-04); [`documents.ts:2`](src/routes/documents.ts:2) | The route lacks an authorization check. | Anonymous request → document store. Impact: unauthorized access. | Collect gateway and application events with principal, object ID, status, and request ID. | Confirmed in source — operationally unverified — open |
| EM-001 | Reconcile inventory ownership. | `POSTURE-02`; named inventory export attributed by the posture review | Separate inventories have no joined owner record. | Not applicable. Assurance gap: ownership decisions cannot be traced. | Collect current inventory and ownership exports keyed by stable asset ID. | Evidence gap confirmed — action open; owner assignment pending |

## Validation boundary

Only the synthetic source artifacts were inspected. No operational systems were queried.
