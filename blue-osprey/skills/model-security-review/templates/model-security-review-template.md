# Model Security Review - {{MODEL_NAME}}

## Security Review Metadata

- **Organization:** {{ORGANIZATION_OR_AMC_CORP}}
- **Authors:** {{REVIEWER_NAMES}}
- **Assessment Timeframe:** {{TIMEFRAME}}
- **Work Item:** {{WORK_ITEM}}
- **Decision Owner:** {{DECISION_OWNER}}
- **Approval or Decision Record:** {{APPROVAL_RECORD}}
- **Engineering Contacts:** {{ENGINEERING_CONTACTS}}
- **Review Scope:** {{REVIEW_SCOPE}}
- **Resources:**
  - Code: {{CODE_REPOSITORY_OR_PATH}}
  - Model card or registry record: {{MODEL_RECORD}}
  - Paper or technical report: {{PAPER_OR_REPORT}}
  - Rollout or deployment document: {{ROLLOUT_DOCUMENT}}
  - Related decision or collaboration record: {{COLLABORATION_RECORD}}

### Revision History

| Date | Version | Author(s) | Summary |
|---|---|---|---|
| {{DATE}} | 1.0 | {{REVIEWER_NAMES}} | Initial delivery |

## Executive Assessment

- **Decision supported:** {{DECISION_SUPPORTED}}
- **Overall risk:** {{OVERALL_RISK}}
- **Recommendation:** {{OVERALL_RECOMMENDATION}}
- **Residual risk:** {{RESIDUAL_RISK}}
- **Material unknowns:** {{MATERIAL_UNKNOWNS}}

## Security Recommendations

### {{FINDING_1_TITLE}}

{{FINDING_1_SUMMARY}}

- **Severity:** {{FINDING_1_SEVERITY}}
- **Confidence:** {{FINDING_1_CONFIDENCE}}
- **Gap:** {{FINDING_1_GAP}}
- **Evidence:** {{FINDING_1_EVIDENCE}}
- **Question:** {{FINDING_1_QUESTION}}
- **Recommendation:** {{FINDING_1_RECOMMENDATION}}
- **Owner:** {{FINDING_1_OWNER}}
- **Verification:** {{FINDING_1_VERIFICATION}}

## Overview

### Capabilities

{{KEY_CAPABILITIES}}

### Intended Use Cases

{{INTENDED_USE_CASES}}

### Out-of-Scope or Prohibited Uses

{{OUT_OF_SCOPE_USES}}

## Scope

- **Model Name and Version:** {{MODEL_NAME}}
- **Base Model or Predecessor:** {{BASE_MODEL}}
- **Architecture:** {{ARCHITECTURE}}
- **Input Modality:** {{INPUT_MODALITY}}
- **Output Modality:** {{OUTPUT_MODALITY}}
- **Primary Adopters:** {{PRIMARY_ADOPTERS}}
- **Access Model:** {{ACCESS_MODEL}}
- **Deployment Regions:** {{REGIONS}}
- **Owning Team:** {{OWNING_TEAM}}

### Interfaces and Integrations

- **Interfaces:** {{INTERFACES}}
- **Upstream Dependencies:** {{UPSTREAM_DEPENDENCIES}}
- **Downstream Consumers:** {{DOWNSTREAM_CONSUMERS}}
- **Trust Boundaries:** {{TRUST_BOUNDARIES}}

## Model Development and Training

### Data Sources and Provenance

- **Public or Licensed Data:** {{PUBLIC_OR_LICENSED_DATA}}
- **Synthetic Data:** {{SYNTHETIC_DATA}}
- **Proprietary or Internal Data:** {{INTERNAL_DATA}}
- **Regulated or Personal Data:** {{REGULATED_DATA}}
- **Provenance and Consent:** {{DATA_PROVENANCE}}
- **Retention and Deletion:** {{DATA_RETENTION}}

### Training and Fine-Tuning

- **Method:** {{TRAINING_METHOD}}
- **Volume:** {{TRAINING_VOLUME}}
- **Compute and Location:** {{TRAINING_COMPUTE}}
- **Fine-Tuning or Adaptation:** {{FINE_TUNING}}
- **Data Filtering and Deduplication:** {{DATA_FILTERING}}

## Model Artifact Integrity

- **Artifact Source:** {{ARTIFACT_SOURCE}}
- **Digest Algorithm:** {{DIGEST_ALGORITHM}}
- **Expected Digest:** {{MODEL_DIGEST}}
- **Verification Point:** {{DIGEST_VERIFICATION_POINT}}
- **Signing or Attestation:** {{SIGNING_OR_ATTESTATION}}

Document how the deployment pipeline verifies the artifact before loading it. A published digest is not an attestation unless its origin and verification path are trusted.

## Model Behavior and Limits

### Operational Limits

- **Maximum Input:** {{MAXIMUM_INPUT}}
- **Maximum Output:** {{MAXIMUM_OUTPUT}}
- **Batch and Concurrency Limits:** {{BATCH_AND_CONCURRENCY_LIMITS}}
- **Timeouts:** {{TIMEOUTS}}
- **Parameter Validation:** {{PARAMETER_VALIDATION}}
- **Failure Behavior:** {{FAILURE_BEHAVIOR}}

### Performance and Quality

- **Latency:** {{LATENCY_DETAILS}}
- **Quality or Accuracy:** {{QUALITY_DETAILS}}
- **Evaluation Coverage:** {{EVALUATION_COVERAGE}}
- **Known Limitations:** {{LIMITATIONS}}

## Infrastructure and Deployment

### Training and Evaluation Environment

- **Provider or Location:** {{TRAINING_LOCATION}}
- **Hardware:** {{TRAINING_HARDWARE}}
- **Software:** {{TRAINING_SOFTWARE}}
- **Security Controls:** {{TRAINING_SECURITY_CONTROLS}}

### Inference Environment

- **Provider or Location:** {{INFERENCE_LOCATION}}
- **Hardware:** {{INFERENCE_HARDWARE}}
- **Software Dependencies:** {{DEPENDENCIES}}
- **Endpoint or Interface:** {{ENDPOINT_CONVENTION}}
- **Authentication and Authorization:** {{AUTH_CONTROLS}}
- **Encryption:** {{ENCRYPTION_CONTROLS}}
- **Tenant Isolation:** {{TENANT_ISOLATION}}
- **Network Exposure and Egress:** {{NETWORK_CONTROLS}}
- **Monitoring and Logging:** {{MONITORING_AND_LOGGING}}
- **Rollout, Rollback, and Kill Switches:** {{ROLLOUT_SAFEGUARDS}}

## Security Testing

- **Threat Model:** {{THREAT_MODEL}}
- **Abuse and Misuse Testing:** {{ABUSE_TESTING}}
- **Adversarial Robustness Testing:** {{ADVERSARIAL_TESTING}}
- **Privacy Testing:** {{PRIVACY_TESTING}}
- **Prompt Injection and Tool-Use Testing:** {{AGENTIC_TESTING}}
- **Safety Evaluations:** {{SAFETY_EVALUATIONS}}
- **Dynamic or Fuzz Testing:** {{DYNAMIC_TESTING}}
- **Known Gaps:** {{TESTING_GAPS}}

## Questions and Unknowns

### Documentation and Use Cases

- **Q:** {{QUESTION_DOCUMENTATION_1}}
- **A or Status:** {{ANSWER_DOCUMENTATION_1}}

### Product and Model Specifications

- **Q:** {{QUESTION_PRODUCT_1}}
- **A or Status:** {{ANSWER_PRODUCT_1}}

### Performance and Evaluation

- **Q:** {{QUESTION_PERFORMANCE_1}}
- **A or Status:** {{ANSWER_PERFORMANCE_1}}

### Infrastructure and Deployment

- **Q:** {{QUESTION_INFRASTRUCTURE_1}}
- **A or Status:** {{ANSWER_INFRASTRUCTURE_1}}

## Accepted Risks and Decision

- **Decision:** {{DECISION}}
- **Decision Owner:** {{DECISION_OWNER}}
- **Accepted Risks:** {{ACCEPTED_RISKS}}
- **Conditions or Expiration:** {{ACCEPTANCE_CONDITIONS}}
- **Follow-up Owners and Dates:** {{FOLLOW_UPS}}

## Code Review

**Date:** {{REVIEW_DATE}}  
**Reviewer:** {{REVIEWER_NAMES}}  
**Scope:** {{CODE_SCOPE}}

### Advisory 1 - {{ADVISORY_1_TITLE}}

- **Severity:** {{ADVISORY_1_SEVERITY}}
- **Confidence:** {{ADVISORY_1_CONFIDENCE}}
- **Status:** {{ADVISORY_1_STATUS}}
- **Owner:** {{ADVISORY_1_OWNER}}

#### Impact

{{ADVISORY_1_IMPACT}}

#### Attack Preconditions and Trust Boundary

- {{ADVISORY_1_PRECONDITION_1}}
- {{ADVISORY_1_PRECONDITION_2}}

#### Evidence and Data Flow

- {{ADVISORY_1_EVIDENCE_1}}
- {{ADVISORY_1_EVIDENCE_2}}

#### Exploitability and False-Positive Considerations

{{ADVISORY_1_EXPLOITABILITY}}

#### Recommended Remediation

1. {{ADVISORY_1_REMEDIATION_1}}
2. {{ADVISORY_1_REMEDIATION_2}}

#### Verification

- {{ADVISORY_1_VERIFICATION_1}}
- {{ADVISORY_1_VERIFICATION_2}}

#### Open Questions

- {{ADVISORY_1_OPEN_QUESTION_1}}
