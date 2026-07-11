# Secrets analysis — 2026-07-10

## Scope

The complete staged Codex and Blue Osprey export was scanned after portable
settings were separated from machine-local configuration.

## Result

- Candidates detected: 0
- Active credential validation: not performed; no candidates were present and
  no network validation was authorized.
- Confidence: high that common hardcoded credential formats are absent.

## Additional exclusions

Authentication state, conversations, logs, caches, telemetry routing,
notification commands, trusted-project paths, marketplace cache metadata, and
runtime-managed MCP environment values were excluded before scanning.

## Limitation

Pattern-based scanning cannot prove that a package contains no sensitive data.
The archive should still be reviewed before sharing outside its intended scope.
