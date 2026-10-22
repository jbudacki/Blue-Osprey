# Security Evidence Map contract fixture

This fixture tests the observable contract of the Blue Osprey
`security-evidence-map` skill without requiring exact prose. The source reports
are synthetic, sanitized examples based on the two supported orientations:

- `cases/finding-first-source.md` starts with a vulnerability and produces more
  than one action while retaining the source finding ID.
- `cases/action-first-source.md` starts with a cross-cutting remediation action
  and points to several findings and artifacts.

The corresponding JSON files are normalized representations of acceptable
Markdown evidence maps. A review runner can give a source file to the skill,
normalize the resulting map to the same JSON shape, and validate it with
`validate-evidence-map.cjs`.

Run all positive and negative contract cases with:

```bash
node run-contract-tests.cjs
```

Validate one normalized map with:

```bash
node validate-evidence-map.cjs cases/finding-first-map.json
```

The checks cover meaningful invariants: traceability, controlled status,
finding-ID retention, source-to-sink structure, separation of source evidence
from SOC collection requests, operational corroboration requirements, and
cross-cutting actions. They do not grade wording or claim that a model-derived
map is factually correct.
