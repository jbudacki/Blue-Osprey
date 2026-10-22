# Evidence-map validation automation

The bundled validator checks the canonical Markdown table without executing
repository code or contacting external systems.

## Basic validation

```bash
python3 scripts/validate_evidence_map.py <evidence-map.md>
```

It fails when the map has:

- a missing canonical column;
- no data rows;
- missing or duplicate row IDs;
- an empty action, evidence reference, evidence statement, source-to-sink or
  impact statement, SOC collection request, or status;
- a status outside the controlled status model;
- a source-confirmed status without a recognizable report, finding, artifact,
  or repository reference;
- a SOC-corroborated status without an operational-evidence reference; or
- a malformed `file:line` or reversed line-range reference.

The validator accepts the controlled status followed by a semicolon and a short
qualification. It does not accept a free-form replacement status.

## Verify local references

```bash
python3 scripts/validate_evidence_map.py <evidence-map.md> \
  --repo-root <repository> \
  --strict-local-references
```

With `--repo-root`, relative local file references are resolved from that
directory. Existing absolute references are also checked. Missing files and
out-of-range lines are warnings by default; `--strict-local-references` makes
them errors suitable for CI or release gates.

References attributed to a report but unavailable locally should remain clearly
attributed in the map. Do not create fake local files or weaken a status merely
to satisfy strict validation.

## Machine-readable output

```bash
python3 scripts/validate_evidence_map.py <evidence-map.md> --json
```

Exit codes are:

- `0`: no validation errors;
- `1`: the map was read but failed validation; and
- `2`: command usage or file-reading failure.

Warnings do not change the exit code unless strict local-reference checking
promotes them to errors.

## Validation boundary

The validator checks structure and mechanically detectable evidence hygiene. It
cannot determine whether cited evidence is genuine, whether a source-to-sink
path is semantically correct, whether a recommendation is sufficient, or
whether operational activity actually occurred. Those remain evidence-review
decisions.
