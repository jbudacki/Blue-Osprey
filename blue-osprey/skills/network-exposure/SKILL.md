---
name: network-exposure
description: "Detect unintentional network exposure, publicly accessible databases, public APIs without authorization, public load balancers without WAF, missing VPC endpoints, and wide-open security groups such as 0.0.0.0/0 on management or database ports. Use when Codex reviews Terraform, CDK, Pulumi, CloudFormation, Kubernetes, or infrastructure networking changes."
---

# Network Exposure Rule: Public Resources and Open Ports

**Name:** `network-exposure`
**Version:** `1.0`
**Tags:** `infrastructure`, `security`, `networking`, `drafted`
**Presubmit Level:** `warn`
**Complexity:** `medium`

**Description:** Detects overly broad network access, publicly accessible databases (RDS), and management ports (SSH/RDP) open to the internet.

---

## Selectors

**Include paths:** `/*.tf`, `/.hcl`, `**/.json`, `/*.yml`, `/.yaml`, `**/.ts`, `/*.py`

**Exclude paths:** `/.test.`, `/.spec.`, `/test/`, `/tests/`, `/generated/`, `/cdk.out/`, `/node_modules/`, `/package.json`, `/package-lock.json`, `/.github/***`

---

## Overview

Publicly exposed infrastructure components, especially databases and management interfaces, are primary targets for automated attacks. This rule identifies configurations that place sensitive resources in public subnets or open critical ports to the entire internet (`0.0.0.0/0`).

This rule applies to Terraform HCL, AWS CloudFormation (JSON/YAML), AWS CDK (TypeScript/Python), and Pulumi.

---

## Rules

1. **Flag publicly accessible databases.** RDS instances with `publicly_accessible = true` or placed in `PUBLIC` subnets are a critical finding. Databases should always reside in `PRIVATE` subnets.
2. **Flag wide-open management ports.** Security groups allowing ingress on port 22 (SSH), 3389 (RDP), or 5432 (PostgreSQL/Database) from `0.0.0.0/0` (any IPv4) are a high-severity finding. These should be restricted to specific CIDR blocks or trusted security groups (e.g., a Bastion host).
3. **Flag public ALBs without WAF.** Public-facing Application Load Balancers should be associated with a WAF Web ACL to protect against common web exploits.
4. **Flag unauthenticated Public APIs.** API Gateway methods without an `AuthorizationType` (e.g., COGNITO, IAM, or custom authorizer) are exposed to the public internet.
5. **Flag missing VPC endpoints.** Traffic to sensitive AWS services (S3, DynamoDB) should stay off the public internet by using VPC Gateway or Interface Endpoints.

---

## Do NOT Flag

* **Load Balancers intended to be public.** `internetFacing: true` for an ALB is acceptable if it is protected by a WAF and restricted to web ports (80/443).
* **Security groups restricted to internal CIDRs.** Ingress from `10.0.0.0/8` or other internal ranges is acceptable.
* **Explicitly documented public resources.** For example, a public API intended for guest access with a comment explaining the decision.
* **CloudFront-only access.** S3 buckets or ALBs restricted to CloudFront Origin Access Identity (OAI) or Origin Access Control (OAC).

---

## Examples

### INCORRECT: Incorrect

#### AWS CDK: Public RDS and wide-open Security Group

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

const database = new rds.DatabaseInstance(this, 'Database', {
  engine: rds.DatabaseInstanceEngine.postgres({
    version: rds.PostgresEngineVersion.VER_15_4,
  }),
  instanceType: ec2.InstanceType.of(
    ec2.InstanceClass.R6G, ec2.InstanceSize.LARGE
  ),
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC }, // VIOLATION: Public subnet
  publiclyAccessible: true, // VIOLATION: Publicly accessible
});

const sg = new ec2.SecurityGroup(this, 'AppSG', {
  vpc,
  description: 'Application security group',
  allowAllOutbound: true,
});

sg.addIngressRule(
  ec2.Peer.anyIpv4(), // VIOLATION: anyIpv4 (0.0.0.0/0)
  ec2.Port.tcp(5432),
  'PostgreSQL from anywhere'
);

sg.addIngressRule(
  ec2.Peer.anyIpv4(), // VIOLATION: SSH from anywhere
  ec2.Port.tcp(22),
  'SSH from anywhere'
);
```

#### Pulumi Python: Wide-open SSH and Public RDS

```python
import pulumi_aws as aws

# VIOLATION: SSH open to the internet
app_sg = aws.ec2.SecurityGroup("app-sg",
    description="Application security group",
    vpc_id=vpc.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp", from_port=22, to_port=22, cidr_blocks=["0.0.0.0/0"],
    )],
)

# VIOLATION: publicly-accessible RDS instance
db = aws.rds.Instance("main",
    engine="postgres",
    instance_class="db.r6g.large",
    allocated_storage=100,
    publicly_accessible=True,
    vpc_security_group_ids=[app_sg.id],
)
```

### CORRECT: Correct

#### Terraform: Private DB, Scoped SGs, and VPC Endpoints

```hcl
resource "aws_security_group" "db_sg" {
  name        = "db-security-group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from app tier only"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id] // Scoped to app tier
  }
}

resource "aws_db_instance" "main" {
  publicly_accessible  = false // CORRECT: Private
  db_subnet_group_name = aws_db_subnet_group.private.name // CORRECT: Private subnet
  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

# CORRECT: VPC endpoints keep traffic internal
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
}
```

#### AWS CDK: WAF-protected ALB and Private Subnets

```typescript
const database = new rds.DatabaseInstance(this, 'Database', {
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }, // CORRECT: Private
  publiclyAccessible: false, // CORRECT: Private
});

const alb = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
  vpc,
  internetFacing: true,
  securityGroup: albSg,
});

// CORRECT: WAF protection for the public ALB
new wafv2.CfnWebACLAssociation(this, 'WafAssoc', {
  resourceArn: alb.loadBalancerArn,
  webAclArn: webAcl.attrArn,
});
```
