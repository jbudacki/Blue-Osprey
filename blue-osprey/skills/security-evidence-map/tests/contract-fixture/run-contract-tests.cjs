#!/usr/bin/env node
const fs = require("node:fs");
const path = require("node:path");
const { validateEvidenceMap } = require("./validate-evidence-map.cjs");

const fixtureRoot = __dirname;
const manifest = JSON.parse(
  fs.readFileSync(path.join(fixtureRoot, "cases.json"), "utf8")
);
let failures = 0;

function fail(message) {
  failures += 1;
  console.error(`contract failure: ${message}`);
}

for (const testCase of manifest.cases) {
  const document = JSON.parse(
    fs.readFileSync(path.join(fixtureRoot, testCase.map), "utf8")
  );
  const errors = validateEvidenceMap(document);
  const isValid = errors.length === 0;

  if (isValid !== testCase.valid) {
    fail(`${testCase.name}: expected valid=${testCase.valid}, got errors: ${errors.join("; ") || "none"}`);
    continue;
  }
  if (!testCase.valid) continue;

  if (document.rows.length < testCase.minRows) {
    fail(`${testCase.name}: expected at least ${testCase.minRows} rows`);
  }
  for (const status of testCase.requiredStatuses || []) {
    if (!document.rows.some((row) => row.status === status)) {
      fail(`${testCase.name}: missing required status ${status}`);
    }
  }
  if (testCase.requiresSplitSourceId) {
    const counts = new Map();
    for (const row of document.rows) {
      for (const sourceId of row.sourceIds) {
        counts.set(sourceId, (counts.get(sourceId) || 0) + 1);
      }
    }
    if (![...counts.values()].some((count) => count > 1)) {
      fail(`${testCase.name}: expected one source finding to produce multiple actions`);
    }
  }
  if (testCase.requiresCrossCuttingRow
      && !document.rows.some((row) => row.sourceIds.length > 1)) {
    fail(`${testCase.name}: expected an action linked to multiple findings or artifacts`);
  }
}

if (failures > 0) process.exit(1);
console.log(`passed ${manifest.cases.length} evidence-map contract cases`);
