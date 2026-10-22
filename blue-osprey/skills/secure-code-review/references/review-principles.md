# Secure Code Review Principles

Use these principles to make security reviews rigorous without turning them
into personality-driven commentary. Apply only the criteria relevant to the
target and repository.

## Core principles

1. **Require evidence before judgment.** Identify the changed behavior, the
   reachable path, and the security consequence. Ask for missing context instead
   of guessing.
2. **Protect existing contracts and controls.** Treat public APIs, authorization
   rules, validation behavior, audit events, data classifications, and documented
   guarantees as contracts. Flag an incompatible change only after identifying
   an affected consumer or control.
3. **Prefer the simplest secure design.** Challenge new flags, variants, states,
   branches, configuration, and abstractions that lack a concrete need. Do not
   reject necessary complexity merely because it is unfamiliar.
4. **Establish correctness before exploitability.** Confirm actual program
   behavior, framework semantics, and deployment assumptions before describing
   an attack path.
5. **Review failure paths as carefully as success paths.** Check partial state,
   rollback, resource cleanup, retry behavior, transaction boundaries, and
   whether errors fail open or fail closed.
6. **Keep privilege transitions explicit.** Verify authentication,
   authorization, tenant separation, service identities, impersonation, and
   administrative paths at the point the privileged action occurs.
7. **Keep input and output authority explicit.** Identify where lower-trust data
   enters, how it is parsed and normalized, and whether output can become code,
   commands, queries, paths, policy, markup, or instructions.
8. **Treat concurrency and lifetime as security properties.** Check lock scope,
   atomicity, ordering, stale state, double use, cleanup races, and object
   lifetime when the language or runtime makes them relevant.
9. **Demand tests that prove changed behavior.** Prefer focused tests for the
   new path, relevant error cases, authorization boundaries, and supported
   platforms. Test intent must be clear from setup and assertions.
10. **Require realistic evidence for availability and performance claims.** Use
    representative workloads, bounded-resource analysis, or profiling. Do not
    treat a micro-benchmark as proof of production behavior.
11. **Make documentation agree with code.** Do not accept a stale comment,
    design document, or API description as evidence that contradicts observable
    behavior.
12. **Separate engineering preference from risk.** Style, naming, or elegance
    can inform maintainability feedback, but they do not establish a
    vulnerability or its severity.

## Decision checkpoints

Work through these questions in order when they apply:

1. Does the change weaken or bypass an existing security contract?
2. Can an attacker-controlled or lower-trust source reach the suspected sink?
3. Is an authentication, authorization, or tenant boundary crossed incorrectly?
4. Can an error or interruption leave sensitive state, privileges, or resources
   in an unsafe condition?
5. Does concurrency, retry, caching, or object lifetime make the check stale or
   bypassable?
6. Does the change create unnecessary public surface or rarely tested code
   paths that materially increase risk?
7. Do tests exercise the security-relevant behavior and its failure cases?
8. Do comments, documentation, configuration, and implementation agree?
9. Is the claimed impact supported by the deployment and threat model?
10. Is the proposed remediation the smallest change that removes the path?

## Review anti-patterns

- Do not imitate a celebrity reviewer or use humiliation, insults, profanity, or
  invented quotations.
- Do not confuse a forceful writing style with strong technical evidence.
- Do not convert a checklist miss, scanner match, or dangerous API into a
  vulnerability without reachability and preconditions.
- Do not inspect only changed lines when the affected caller, sink, or guard is
  available nearby.
- Do not use security severity as a substitute for an overall merge decision.
- Do not request broad refactoring when a focused fix removes the risk.
- Do not create noise from harmless formatting, naming, or documentation
  preferences.
- Do not approve solely because the code is concise, tested, or familiar; verify
  the relevant security properties.
