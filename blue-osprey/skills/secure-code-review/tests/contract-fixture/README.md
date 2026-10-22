# Secure Code Review Contract Fixture

This fixture provides deterministic cases for validating that a secure code
review follows the Blue-Osprey `secure-code-review` contract. The code is
synthetic and safe to inspect; it must not be executed with untrusted input.

## Cases

- `cases/confirmed-command-injection/` — confirmed source-to-sink finding.
- `cases/no-finding/` — benign input handling; should produce no finding.
- `cases/unconfirmed-scanner-hit/` — suspicious API name without a reachable
  attacker-controlled path; should be reported as a hypothesis or observation,
  not a confirmed vulnerability.
- `cases/missing-context/` — security-relevant behavior whose reachability is
  unknown; should produce open questions and a `Discuss` disposition.

## Expected contract

`expected.json` defines the expected finding class, severity range, disposition,
and required evidence concepts for each case. A review runner can have the
review skill produce its normal Markdown report, then map it to the small JSON
shape accepted by `validate-review.cjs`:

```json
{
  "findings": [
    {
      "name": "...",
      "severity": "High",
      "confidence": "High",
      "evidence": ["file.js:4"],
      "entryPoint": "...",
      "sourceToSink": "...",
      "trustBoundary": "...",
      "preconditions": "...",
      "impact": "...",
      "exploitabilityNotes": "...",
      "falsePositiveConsiderations": "...",
      "recommendedFix": "...",
      "verification": "...",
      "openQuestions": "..."
    }
  ],
  "disposition": "Block",
  "verificationPerformed": "...",
  "remainingUnknowns": "..."
}
```

Run the structural contract check with:

```bash
node validate-review.cjs expected.json
```

This validates the fixture’s expected oracle and the required review fields; it
does not execute application code or claim that a model review is correct.

