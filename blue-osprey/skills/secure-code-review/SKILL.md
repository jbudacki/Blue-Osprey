---
name: secure-code-review
description: "Perform evidence-based security code reviews of pull requests, diffs, commits, files, or repositories after scope is established. Use when Codex needs code-level source-to-sink analysis, review of authentication or authorization logic, input validation, error and cleanup paths, concurrency, security-control regressions, tests, or an overall review disposition. Use as the code-review specialist behind $security-review; route secrets, IAM, LLM, crypto, network, dependency, and model-specific surfaces through the matching Blue-Osprey skills."
---

# Secure Code Review

Act as the code-level specialist for `$security-review`. Review changed behavior,
its surrounding execution paths, and the controls that protect affected assets.
Keep the review direct, respectful, and proportional to demonstrated risk.

## Establish the review boundary

1. Read applicable repository instructions and identify the requested review
   target, comparison base, and relevant environment.
2. Confirm authorization before validating a live, third-party, production, or
   customer-facing target. Treat local read-only inspection as the default.
3. Identify affected entry points, callers, callees, assets, identities, trust
   boundaries, external systems, and security controls.
4. Inspect the surrounding code, configuration, and tests needed to understand
   changed behavior. Do not review a diff in isolation when its call path is
   available.
5. Use `$codebase-discovery` first when the repository is unfamiliar enough
   that architecture or review scope cannot be established safely.

Do not edit code, create commits, call external services, or validate against a
live system unless the user authorizes that action.

## Apply the review principles

Read [references/review-principles.md](references/review-principles.md) before
performing the review. Apply the principles as engineering criteria, not as a
persona. Do not imitate a named individual, repeat insults, or use theatrical
language in review feedback.

## Review method

Evaluate the target in this order:

1. **Architecture and trust boundaries.** Determine what changed, who can reach
   it, which privileges are involved, and which assets could be affected.
2. **Correctness.** Verify control flow, state transitions, assumptions, error
   propagation, cleanup, compatibility, and behavior at boundary conditions.
3. **Security.** Trace attacker-controlled or lower-trust data through parsing,
   validation, authorization, transformation, storage, logging, and sensitive
   sinks. Check for security-control regressions as well as new vulnerabilities.
4. **Tests.** Confirm that changed success paths, failure paths, authorization
   boundaries, and platform-specific behavior have meaningful coverage.
5. **Maintainability.** Flag complexity, duplication, hidden state, or unclear
   contracts only when they materially increase correctness or security risk.
6. **Performance.** Challenge security-relevant availability risks and
   performance claims only when the code path and evidence support them.

For each suspected issue:

1. Identify the entry point and attacker-controlled or lower-trust source.
2. Trace the source to a reachable sink or failed control.
3. State the required role, state, configuration, and environmental
   preconditions.
4. Verify the impact without relying on an unsupported worst case.
5. Check nearby guards, framework behavior, deployment constraints, and tests
   that could make the concern a false positive.
6. Prefer a safe proof or focused test. Do not provide harmful exploit steps for
   systems outside authorized scope.
7. Recommend the smallest change that removes the demonstrated path and name a
   verification step.

Use the routing table in `$security-review` when the target contains a specialist
surface such as secrets, IAM, LLMs, cryptography, network exposure, dependencies,
or model deployment. Keep this skill focused on the cross-cutting code path and
do not duplicate a specialist's findings.

## Finding gate

Report a security finding only when the available evidence establishes a
plausible source-to-sink or control-failure path. Do not:

- convert scanner output directly into a finding;
- infer exploitability from a dangerous function name alone;
- assume an input is attacker-controlled without identifying the boundary;
- assign severity from reviewer preference, code style, or tone;
- force a fixed number of findings; or
- claim a test or validation passed unless it was run.

Label an unconfirmed concern as a hypothesis and state the missing evidence.
When no confirmed findings remain, say so and disclose validation limits and
residual risks.

## Severity and disposition

Use `Critical`, `High`, `Medium`, `Low`, or `Info` for technical security
severity. Base severity on reachable impact, required privileges, exposure,
scope, and practical constraints.

Keep the overall review disposition separate:

- **Block:** A confirmed Critical or High risk, or a direct bypass of a required
  security control, makes the change unsafe to merge.
- **Request changes:** A confirmed issue or missing required verification must
  be resolved before merge.
- **Discuss:** Material intent, architecture, or reachability remains unclear.
- **Non-blocking:** Only Low, Info, or narrowly scoped hardening remains.
- **Approve:** No blocking findings remain and verification is proportionate to
  the change.

Do not inflate a vulnerability's severity to justify a merge disposition.

## Output

Lead with confirmed findings ordered by severity. Use this format, matching
`$security-review`:

```text
Finding: <name>
Severity: <Critical|High|Medium|Low|Info>
Confidence: <High|Medium|Low>
Evidence:
- <file:line> <relevant code or behavior>
Entry point: <where attacker/user input enters>
Source-to-sink path: <path summary>
Trust boundary: <boundary crossed>
Preconditions: <required state/role/config>
Impact: <what can happen>
Exploitability notes: <constraints without unsafe detail>
False-positive considerations: <why this might not be exploitable>
Recommended fix: <specific change>
Verification: <test/manual check/tool command>
Open questions: <unknowns>
```

After the findings, provide the overall disposition, verification performed,
and remaining unknowns. Put material non-security observations in a separate
section and do not present them as vulnerabilities.

When the user requests an evidence map, remediation handoff, SOC collection
plan, or the review concerns active threat activity, route the completed
findings through `$security-evidence-map`. Keep the original review authoritative
and distinguish source-confirmed conditions from operational corroboration.
