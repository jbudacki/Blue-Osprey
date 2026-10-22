#!/usr/bin/env node
const fs = require("node:fs");

const requiredFindingFields = [
  "name", "severity", "confidence", "evidence", "entryPoint",
  "sourceToSink", "trustBoundary", "preconditions", "impact",
  "exploitabilityNotes", "falsePositiveConsiderations", "recommendedFix",
  "verification", "openQuestions"
];
const validSeverities = new Set(["Critical", "High", "Medium", "Low", "Info"]);
const validDispositions = new Set(["Block", "Request changes", "Discuss", "Non-blocking", "Approve"]);

function fail(message) {
  console.error(`contract failure: ${message}`);
  process.exitCode = 1;
}

if (!process.argv[2]) {
  fail("usage: node validate-review.cjs <expected.json>");
} else {
  const expected = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  for (const [caseName, oracle] of Object.entries(expected)) {
    if (!validDispositions.has(oracle.disposition)) fail(`${caseName}: invalid disposition`);
    if (!Number.isInteger(oracle.findingCount) || oracle.findingCount < 0) fail(`${caseName}: invalid findingCount`);
    if (oracle.severity && !validSeverities.has(oracle.severity)) fail(`${caseName}: invalid severity`);
    if (oracle.confidence && !["High", "Medium", "Low"].includes(oracle.confidence)) fail(`${caseName}: invalid confidence`);
    if (!Array.isArray(oracle.requiredEvidence || [])) fail(`${caseName}: requiredEvidence must be an array`);
  }
  if (!process.exitCode) console.log(`validated ${Object.keys(expected).length} contract cases`);
}
