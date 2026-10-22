#!/usr/bin/env node
const fs = require("node:fs");

const VALID_MODES = new Set(["finding-first", "action-first"]);
const VALID_REFERENCE_TYPES = new Set([
  "review", "repo", "test", "artifact", "operational"
]);
const VALID_STATUSES = new Set([
  "Confirmed in source — operationally unverified — open",
  "Confirmed in source — SOC corroborated — open",
  "Conditionally reachable — evidence needed",
  "Evidence gap confirmed — action open",
  "Hypothesis — insufficient source evidence",
  "Remediated — verification pending",
  "Closed — verified",
  "Accepted risk — approval reference required"
]);

function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function nonEmptyStringArray(value) {
  return Array.isArray(value) && value.length > 0 && value.every(nonEmptyString);
}

function validateEvidenceMap(document) {
  const errors = [];

  if (!document || typeof document !== "object" || Array.isArray(document)) {
    return ["document must be an object"];
  }
  if (!VALID_MODES.has(document.mode)) errors.push("mode must be finding-first or action-first");
  if (!nonEmptyString(document.sourceTitle)) errors.push("sourceTitle must be a non-empty string");
  if (!nonEmptyString(document.validationBoundary)) {
    errors.push("validationBoundary must state what the map did and did not establish");
  }
  if (!Array.isArray(document.rows) || document.rows.length === 0) {
    errors.push("rows must be a non-empty array");
    return errors;
  }

  const ids = new Set();
  for (const [index, row] of document.rows.entries()) {
    const at = `rows[${index}]`;
    if (!row || typeof row !== "object" || Array.isArray(row)) {
      errors.push(`${at} must be an object`);
      continue;
    }

    if (!nonEmptyString(row.id)) {
      errors.push(`${at}.id must be a non-empty string`);
    } else if (ids.has(row.id)) {
      errors.push(`${at}.id duplicates ${row.id}`);
    } else {
      ids.add(row.id);
    }

    if (!nonEmptyStringArray(row.sourceIds)) {
      errors.push(`${at}.sourceIds must contain at least one source finding or action ID`);
    }
    if (!nonEmptyString(row.action)) errors.push(`${at}.action must be a non-empty string`);
    if (!nonEmptyString(row.evidenceShown)) {
      errors.push(`${at}.evidenceShown must be a non-empty string`);
    }
    if (!VALID_STATUSES.has(row.status)) errors.push(`${at}.status is not controlled`);

    if (!Array.isArray(row.whereToPoint) || row.whereToPoint.length === 0) {
      errors.push(`${at}.whereToPoint must contain at least one evidence reference`);
    } else {
      for (const [referenceIndex, reference] of row.whereToPoint.entries()) {
        const refAt = `${at}.whereToPoint[${referenceIndex}]`;
        if (!reference || typeof reference !== "object" || Array.isArray(reference)) {
          errors.push(`${refAt} must be an object`);
          continue;
        }
        if (!VALID_REFERENCE_TYPES.has(reference.type)) {
          errors.push(`${refAt}.type is invalid`);
        }
        if (!nonEmptyString(reference.ref)) errors.push(`${refAt}.ref must be non-empty`);
      }
      if (nonEmptyStringArray(row.sourceIds)) {
        const citedReferences = row.whereToPoint
          .map((reference) => reference?.ref || "")
          .join(" ")
          .toLowerCase();
        for (const sourceId of row.sourceIds) {
          if (!citedReferences.includes(sourceId.toLowerCase())) {
            errors.push(`${at}.sourceIds value ${sourceId} is not present in whereToPoint`);
          }
        }
      }
    }

    const path = row.sourceToSinkImpact;
    if (!path || typeof path !== "object" || Array.isArray(path)) {
      errors.push(`${at}.sourceToSinkImpact must be an object`);
    } else if (path.kind === "technical") {
      if (!nonEmptyString(path.source)) errors.push(`${at}.sourceToSinkImpact.source is required`);
      if (!nonEmptyString(path.sink)) errors.push(`${at}.sourceToSinkImpact.sink is required`);
      if (!nonEmptyString(path.impact)) errors.push(`${at}.sourceToSinkImpact.impact is required`);
      if (!nonEmptyStringArray(path.preconditions)) {
        errors.push(`${at}.sourceToSinkImpact.preconditions must be non-empty`);
      }
    } else if (path.kind === "governance") {
      if (path.applicability !== "not-applicable") {
        errors.push(`${at}.sourceToSinkImpact.applicability must be not-applicable for governance rows`);
      }
      if (!nonEmptyString(path.assuranceGap)) {
        errors.push(`${at}.sourceToSinkImpact.assuranceGap is required`);
      }
      if (!nonEmptyString(path.impact)) errors.push(`${at}.sourceToSinkImpact.impact is required`);
    } else {
      errors.push(`${at}.sourceToSinkImpact.kind must be technical or governance`);
    }

    const collection = row.socEvidenceToCollect;
    if (!collection || typeof collection !== "object" || Array.isArray(collection)) {
      errors.push(`${at}.socEvidenceToCollect must be an object`);
    } else {
      if (!nonEmptyStringArray(collection.telemetrySources)) {
        errors.push(`${at}.socEvidenceToCollect.telemetrySources must be non-empty`);
      }
      if (!nonEmptyStringArray(collection.events)) {
        errors.push(`${at}.socEvidenceToCollect.events must be non-empty`);
      }
      if (!nonEmptyStringArray(collection.correlationFields)) {
        errors.push(`${at}.socEvidenceToCollect.correlationFields must be non-empty`);
      }
      if (!nonEmptyString(collection.confirmationCriteria)) {
        errors.push(`${at}.socEvidenceToCollect.confirmationCriteria must be non-empty`);
      }
      if (nonEmptyString(row.evidenceShown) && row.evidenceShown === collection.confirmationCriteria) {
        errors.push(`${at} must distinguish evidence shown from evidence still to collect`);
      }
    }

    if (row.operationalEvidence !== undefined
        && (!Array.isArray(row.operationalEvidence)
          || !row.operationalEvidence.every(nonEmptyString))) {
      errors.push(`${at}.operationalEvidence must contain only non-empty strings when present`);
    }
    const operationalEvidence = Array.isArray(row.operationalEvidence)
      ? row.operationalEvidence
      : [];
    if (row.status === "Confirmed in source — SOC corroborated — open") {
      const hasOperationalReference = Array.isArray(row.whereToPoint)
        && row.whereToPoint.some((reference) => reference?.type === "operational");
      if (!hasOperationalReference || !nonEmptyStringArray(operationalEvidence)) {
        errors.push(`${at} claims SOC corroboration without operational evidence and a reference`);
      }
    }

    if (row.status === "Closed — verified" && !nonEmptyStringArray(row.verificationEvidence)) {
      errors.push(`${at} claims verified closure without verificationEvidence`);
    }

    if (document.mode === "finding-first" && nonEmptyString(row.id)
        && nonEmptyStringArray(row.sourceIds)) {
      const retainsSourceId = row.sourceIds.some(
        (sourceId) => row.id === sourceId || row.id.startsWith(`${sourceId}-`)
      );
      if (!retainsSourceId) errors.push(`${at}.id must retain a source finding ID`);
    }
  }

  return errors;
}

function readDocument(path) {
  return JSON.parse(fs.readFileSync(path, "utf8"));
}

if (require.main === module) {
  if (!process.argv[2]) {
    console.error("usage: node validate-evidence-map.cjs <normalized-map.json>");
    process.exit(2);
  }
  let document;
  try {
    document = readDocument(process.argv[2]);
  } catch (error) {
    console.error(`contract failure: unable to read JSON: ${error.message}`);
    process.exit(1);
  }
  const errors = validateEvidenceMap(document);
  if (errors.length > 0) {
    for (const error of errors) console.error(`contract failure: ${error}`);
    process.exit(1);
  }
  console.log(`validated ${document.rows.length} evidence-map rows`);
}

module.exports = { validateEvidenceMap, VALID_STATUSES };
