# Synthetic security review

Finding: Missing server-side document authorization  
ID: SR-04  
Severity: High  
Confidence: High  
Evidence: `src/routes/documents.ts:42` calls the document controller without
authentication middleware. `tests/documents-auth.test.ts` contains no negative
authorization case.  
Entry point: External HTTP request containing a document identifier.  
Source-to-sink path: Anonymous request → document controller → document store.  
Preconditions: The route must be externally reachable.  
Impact: Unauthorized document access or modification.  
Recommended fix: Enforce server-side authentication and object authorization;
add negative tests and detection coverage.  
Verification: Confirm anonymous and cross-user requests are rejected and logged.  
Open questions: Whether production telemetry contains successful anonymous or
identity-mismatched requests.

Disposition: Block

No production systems were queried and no operational logs were supplied.
