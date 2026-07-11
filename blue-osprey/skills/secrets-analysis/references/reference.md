# Secrets Analysis Reference

## Secret Categories and Patterns

| Category | Description | Examples |
|----------|-------------|----------|
| **api_keys** | Generic and service-specific API keys | OpenAI (`sk-`), Stripe (`pk_`, `sk_`), GitHub (`ghp_`) |
| **cloud** | Cloud provider credentials | AWS (`AKIA`, `secret_key`), GCP, Azure |
| **database** | Connection strings and DB passwords | `postgres://`, `mongodb://`, `mysql://` |
| **crypto** | Cryptographic keys and certificates | `-----BEGIN EXAMPLE PRIVATE MATERIAL-----` |
| **encoded** | Base64 or hex encoded credentials | Encoded auth headers |
| **services** | SaaS and third-party service tokens | Slack (`xoxb-`), Twilio, SendGrid |

## Risk Classification Matrix

| Severity | Description | Remediation |
|----------|-------------|-------------|
| **CRITICAL** | Exposed production credentials, active cloud keys, primary API keys. | Immediate rotation, incident response. |
| **HIGH** | Hardcoded passwords, JWT tokens, private keys in dev/test code. | Remove from code, move to secret manager. |
| **MEDIUM** | Inactive or test credentials, internal service tokens. | Cleanup and rotation. |
| **LOW** | Minor configuration secrets, non-sensitive IDs. | Follow best practices. |

## Mitigation Strategies

1.  **Secret Managers**: Use AWS Secrets Manager, HashiCorp Vault, or Google Secret Manager.
2.  **Environment Variables**: Inject secrets at runtime via environment variables (e.g., `.env` files, but ensure they are gitignored).
3.  **Key Rotation**: Implement automated key rotation policies.
4.  **Pre-commit Hooks**: Use tools like `pre-commit` or `detect-secrets` to prevent secrets from being committed.
5.  **Audit Logs**: Monitor access logs for the exposed credentials.
