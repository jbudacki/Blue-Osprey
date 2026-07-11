---
name: iam-security
description: "Detect overly permissive IAM policies, wildcard permissions, public principals, unguarded cross-account trust, and privilege escalation paths in Terraform, CloudFormation, CDK, Pulumi, raw IAM JSON/YAML, and related infrastructure code. Use when Codex reviews AWS IAM, least privilege, service roles, trust policies, or cloud authorization changes."
---

# IAM Security Rule: Overly Permissive IAM Policies

**Name:** `iam-security`
**Version:** `1.0`
**Author:** `golden-gate`
**Tags:** `infrastructure`, `security`, `authorization`, `drafted`
**Presubmit Level:** `warn`
**Complexity:** `medium`

**Description:** Detects overly permissive IAM policies, wildcard permissions, and privilege escalation paths.

---

## Selectors

**Include paths:** `/*.tf`, `/.hcl`, `**/.json`, `/*.yml`, `/.yaml`, `**/.ts`, `/*.py`

**Exclude paths:** `/.test.`, `/.spec.`, `/test/`, `/tests/`, `/generated/`, `/cdk.out/`, `/node_modules/`, `/package.json`, `/package-lock.json`, `/.github/***`

---

## Overview

This rule detects IAM policies that violate the principle of least privilege, including wildcard actions and resources, admin-level access on service roles, unguarded cross-account trust, and policies that enable privilege escalation.

IAM misconfigurations are the single most common root cause of cloud security breaches. A single overly permissive role can give an attacker lateral movement across an entire AWS account.

This rule applies to Terraform HCL, AWS CloudFormation (JSON/YAML), AWS CDK (TypeScript/Python), and raw IAM policy documents embedded in any supported format.

---

## Remediation / To Fix

1. Replace `Action: "*"` with specific actions needed (e.g., `s3:GetObject`, `s3:PutObject`).
2. Replace `Resource: "*"` with specific ARN patterns (e.g., `arn:aws:s3:::my-bucket/*`).
3. Add condition keys to cross-account trust policies (`aws:PrincipalOrgID`, `sts:ExternalId`).
4. Require MFA for privilege escalation actions (`iam:CreateRole`, `iam:AttachRolePolicy`).
5. Use AWS managed policies where possible instead of inline wildcard policies.

**Reference:** [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

> *If this finding is not applicable, reply to the PR comment explaining why. We will track it as acknowledged and it will not block your PR.*

---

## Rules

1. **Flag wildcard actions.** IAM policies with `Action: "*"` or `"Action": ["*"]` grant unrestricted access to every AWS API. Every policy must enumerate specific actions.
2. **Flag wildcard resources.** `Resource: "*"` grants access to every resource in the account. Policies must use specific ARN patterns scoped to the resources the role actually needs.
3. **Flag admin-level managed policies on service roles.** `AdministratorAccess`, `PowerUserAccess`, or `IAMFullAccess` attached to Lambda execution roles, ECS task roles, EC2 instance profiles, or any service role is a critical finding.
4. **Flag cross-account trust without conditions.** `AssumeRole` trust policies that allow external accounts without `aws:PrincipalOrgID`, `sts:ExternalId`, or other condition constraints enable unrestricted cross-account access.
5. **Flag privilege escalation paths.** Policies granting `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PutRolePolicy`, `iam:CreatePolicyVersion`, or `iam:PassRole` without MFA conditions allow a compromised principal to escalate its own privileges.
6. **Flag public S3 bucket policies.** Bucket policies with `Principal: "*"` without condition constraints (e.g., `aws:SourceVpce`, `aws:SourceIp`, `aws:PrincipalOrgID`) make bucket contents accessible to anyone on the internet.
7. **Flag missing deny boundaries.** Sensitive operations (deleting KMS keys, modifying CloudTrail, disabling GuardDuty) should have explicit deny statements as guardrails via SCPs or permission boundaries.
8. **Flag overly broad service-linked permissions.** Lambda functions, ECS tasks, or Step Functions with permissions far exceeding their stated purpose (e.g., a Lambda that reads from one DynamoDB table but has `dynamodb:*` on `Resource: "*"`).

---

## Do NOT Flag

* **AWS managed policies referenced by name** (e.g., `arn:aws:iam::aws:policy/ReadOnlyAccess`) - these are curated by AWS and regularly updated.
* **Deny statements** - deny restricts access, it does not expand it; `Effect: Deny` with `Action: "*"` is a valid security pattern.
* **Policies in clearly labeled test/sandbox environments** - resources tagged `Environment: test` or in a sandbox account (if identifiable from context).
* **CDK-generated policy documents in `cdk.out/`** - flag the CDK source code instead, not the synthesized output.
* **Read-only policies on non-sensitive resources** - `s3:GetObject` on a public assets bucket is acceptable.
* **Service-linked roles created by AWS** - roles prefixed with `AWSServiceRoleFor*` are managed by AWS.
* **Condition-constrained wildcards** - `Action: "s3:*"` with a tight Condition block limiting to a specific VPC endpoint or source IP is a valid pattern (flag only if conditions are missing).
* **Permission boundaries** - these constrain permissions, they don't grant them.
* **Design decisions explicitly documented** in adjacent code comments (e.g., "broad permissions required for cross-account replication").
* **VPC PrivateLink `allowed_principals` and VPC Endpoint Service configurations** - `aws_vpc_endpoint_service.allowed_principals` is network-level access control, not an IAM trust policy. It does not support IAM condition keys (`aws:PrincipalOrgID`, `sts:ExternalId`). Do not flag account-level ARNs in `allowed_principals` for missing conditions.
* **Non-IAM AWS resource attributes that accept principal ARNs** - services like VPC Endpoint Service, RAM resource shares, and Lake Formation grants use principal ARNs for access control outside the IAM policy framework. Only flag principal ARNs within IAM policy documents (`aws_iam_policy`, `aws_iam_role_policy`, `assume_role_policy`, CloudFormation `AWS::IAM::*`).

---

## Examples

### INCORRECT: Incorrect

#### Terraform: Cross-account trust with no conditions

```hcl
resource "aws_iam_role" "cross_account_role" {
  name = "cross-account-deploy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"
      Principal = {
        AWS = "arn:aws:iam::123456789012:root"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "admin_attach" {
  role       = aws_iam_role.cross_account_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
```

#### AWS CDK: Public S3 bucket and overly permissive role (TypeScript)

```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';

const bucket = new s3.Bucket(this, 'DataBucket', {
  bucketName: 'customer-data-bucket',
});

bucket.addToResourcePolicy(new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  principals: [new iam.AnyPrincipal()],
  actions: ['s3:GetObject', 's3:PutObject'],
  resources: [bucket.arnForObjects('*')]
}));

const fn = new lambda.Function(this, 'Processor', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
});

fn.addToRolePolicy(new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: ['*'],
  resources: ['*'],
}));
```

#### CloudFormation: Privilege escalation path without MFA (YAML)

```yaml
Resources:
  DeployRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: deploy-automation-role
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
            Action: "sts:AssumeRole"
      Policies:
        - PolicyName: deploy-policy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - "iam:CreateRole"
                  - "iam:AttachRolePolicy"
                  - "iam:PutRolePolicy"
                  - "iam:PassRole"
                  - "iam:CreatePolicyVersion"
                Resource: "*"
```

#### Pulumi Python: Wildcard action/resource on a Lambda role

```python
import json
import pulumi_aws as aws

lambda_role = aws.iam.Role("lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
        }]
    })
)

# VIOLATION: Action "*" + Resource "*" grants unrestricted access
aws.iam.RolePolicy("lambda-full-access",
    role=lambda_role.id,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }]
    })
)
```

### CORRECT: Correct

#### Terraform: Least-privilege Lambda role scoped to specific resources

```hcl
resource "aws_iam_role" "lambda_role" {
  name = "my-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-scoped-access"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query"
        ]
        Resource = "arn:aws:dynamodb:us-east-1:123456789012:table/my-table"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::my-bucket/uploads/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:us-east-1:123456789012:log-group:/aws/lambda/my-function:*"
      }
    ]
  })
}
```

#### Terraform: Cross-account trust with org and external ID conditions

```hcl
resource "aws_iam_role" "cross_account_role" {
  name = "cross-account-deploy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"
      Principal = {
        AWS = "arn:aws:iam::123456789012:role/deploy-pipeline"
      }
      Condition = {
        StringEquals = {
          "aws:PrincipalOrgID" = "o-*",
          "sts:ExternalId" = "deploy-pipeline-2024"
        }
      }
    }]
  })
}
```

#### AWS CDK: Scoped bucket policy and least-privilege function role (TypeScript)

```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';

const bucket = new s3.Bucket(this, 'DataBucket', {
  bucketName: 'customer-data-bucket',
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  encryption: s3.BucketEncryption.KMS,
});

bucket.addToResourcePolicy(new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  principals: [new iam.ArnPrincipal('arn:aws:iam::123456789012:role/data-reader')],
  actions: ['s3:GetObject'],
  resources: [bucket.arnForObjects('reports/*')],
  conditions: {
    StringEquals: {
      'aws:PrincipalOrgID': 'o-*',
    },
  },
}));

const fn = new lambda.Function(this, 'Processor', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
});

bucket.grantRead(fn, 'uploads/*');
```

#### CloudFormation: Privilege escalation guarded by MFA condition (YAML)

```yaml
Resources:
  DeployRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: deploy-automation-role
      PermissionsBoundary: !Sub "arn:aws:iam::${AWS::AccountId}:policy/DeployBoundary"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/ci-pipeline"
            Action: "sts:AssumeRole"
            Condition:
              StringEquals:
                "aws:PrincipalOrgID": "o-*"
      Policies:
        - PolicyName: deploy-policy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - "iam:PassRole"
                Resource:
                  - !Sub "arn:aws:iam::${AWS::AccountId}:role/app-*"
                Condition:
                  StringEquals:
                    "iam:PassedToService": "lambda.amazonaws.com"
              - Effect: Allow
                Action:
                  - "cloudformation:CreateStack"
                  - "cloudformation:UpdateStack"
                  - "cloudformation:DescribeStacks"
                Resource:
                  - !Sub "arn:aws:cloudformation:*:${AWS::AccountId}:stack/app-*"
```

#### Pulumi Python: Least-privilege Lambda role scoped to specific actions and resources

```python
import json
import pulumi_aws as aws

lambda_role = aws.iam.Role("lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
        }]
    })
)

# CORRECT: specific actions against specific ARN patterns
aws.iam.RolePolicy("lambda-scoped-access",
    role=lambda_role.id,
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": "arn:aws:s3:::my-uploads-bucket/*"
            },
            {
                "Effect": "Allow",
                "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
                "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/app-data"
            }
        ]
    })
)
```
