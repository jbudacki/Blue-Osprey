# Evidence map status model

Status communicates three things compactly: what the available evidence
establishes, whether operational activity is corroborated, and whether the
action is closed. Choose the most specific supported value.

| Status | Use when |
|---|---|
| `Confirmed in source — operationally unverified — open` | Code, configuration, or another authoritative artifact confirms the condition, but operational evidence has not established attempted or successful exploitation. |
| `Confirmed in source — SOC corroborated — open` | The source condition is confirmed and supplied operational evidence corroborates relevant attempted or successful activity. State which evidence supports the correlation. |
| `Conditionally reachable — evidence needed` | The condition exists, but exploitability depends on unverified deployment, identity, network, identifier, or configuration preconditions. |
| `Evidence gap confirmed — action open` | The demonstrated problem is missing ownership, approval, inventory, provenance, retention, monitoring, or other assurance evidence rather than a technical source-to-sink path. |
| `Hypothesis — insufficient source evidence` | The available artifacts suggest a concern but do not establish the condition or a plausible control-failure path. Name the evidence needed. |
| `Remediated — verification pending` | A change or control implementation is evidenced, but the required closure test or independent validation has not been completed. |
| `Closed — verified` | The remediation is evidenced and the specified verification has passed. Identify the verification artifact or result. |
| `Accepted risk — approval reference required` | An authorized risk owner accepted the condition. Cite the approval, scope, expiration or review date, and compensating controls when supplied. |

## Selection rules

- Do not use `SOC corroborated` solely because the user says the environment is
  being scanned. Corroboration requires relevant supplied telemetry or an
  authoritative incident record tied to the condition.
- Do not use `Remediated` from an implementation plan, ticket state, or verbal
  assurance alone. Require evidence of the changed control.
- Do not use `Closed` until the stated verification has been performed and its
  result is available.
- Do not use `Accepted risk` without an identifiable approving authority and
  scope. If the approval artifact is missing, keep the action open.
- Preserve the source review's confidence separately when present. Status does
  not replace confidence or technical severity.
- If evidence supports different statuses for separate actions under one
  finding, create separate rows.
