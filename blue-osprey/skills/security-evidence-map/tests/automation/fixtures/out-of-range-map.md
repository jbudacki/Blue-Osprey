# Out-of-range synthetic evidence map

| ID | Action | Where to point | Evidence shown | Source → sink / impact | SOC evidence to collect | Status |
|---|---|---|---|---|---|---|
| SR-04-A | Enforce document authorization. | [SR-04](review.md#sr-04); [`documents.ts:99`](src/routes/documents.ts:99) | The route lacks an authorization check. | Anonymous request → document store. Impact: unauthorized access. | Collect gateway and application events. | Confirmed in source — operationally unverified — open |
