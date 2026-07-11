# Code Review Checklist

Use this during Phase 4 when code is in scope. Group findings into Advisories using the format in SKILL.md.

## Inference / Serving Endpoints

### Authentication & Authorization
- [ ] All inference endpoints require auth (bearer token, mTLS, signed request)
- [ ] No `if request.headers.get('Authorization') is None: pass` patterns
- [ ] Token validation happens before any model invocation or expensive work
- [ ] Tenant identity is extracted from auth, not request body
- [ ] Service-to-service auth uses mTLS or signed JWTs, not shared secrets

### Network Binding
- [ ] Default bind address is `127.0.0.1`, not `0.0.0.0`
- [ ] If bound to `0.0.0.0`, there's an explicit reverse proxy + auth in front
- [ ] No services exposed via Docker port mapping without auth (`-p 0.0.0.0:8080:8080`)

### Input Validation
- [ ] Request schema validated before processing (pydantic, JSON schema)
- [ ] Max payload size enforced (Content-Length check or framework limit)
- [ ] Max rows / max tokens / max sequence length enforced
- [ ] Fail-early on type mismatch with clean error response (not 500)
- [ ] Hyperparameter bounds checked against allowlist or range

### Rate Limiting & Timeouts
- [ ] Per-tenant rate limit on invocations (not just per-request)
- [ ] Per-tenant concurrent request limit
- [ ] Server-side timeout on inference (must be ≤ client timeout)
- [ ] Backpressure/503 response when overloaded (not crash)

### Logging & Audit
- [ ] All inference calls logged with tenant ID, user ID, model version, latency
- [ ] No sensitive data (PII, credentials) in logs
- [ ] Failed auth attempts logged separately
- [ ] Logs structured (JSON) for ingestion to SIEM

---

## Sandbox / Code Execution Services

### Endpoint Security
- [ ] `/execute` requires authentication
- [ ] Bound to localhost by default
- [ ] Documented network policy (e.g., only callable from agent service in same pod)

### Container Image (Dockerfile)
- [ ] `USER` directive set to non-root before `CMD`/`ENTRYPOINT`
- [ ] Minimal base image (distroless, alpine, or slim)
- [ ] No `apt-get install` of unnecessary tools (curl, wget, ssh) in final image
- [ ] No secrets in image layers (docker history clean)
- [ ] Multi-stage build to exclude build tools

### Container Runtime Flags
- [ ] `--read-only` on root filesystem
- [ ] Writable scratch via `tmpfs` mount only
- [ ] `--cap-drop ALL` (and explicit `--cap-add` for what's needed)
- [ ] `--security-opt no-new-privileges:true`
- [ ] `--pids-limit` set
- [ ] `--memory` and `--cpus` set
- [ ] `--network=none` or strict egress allowlist
- [ ] Seccomp profile applied (`--security-opt seccomp=...`)
- [ ] AppArmor / SELinux profile if available

### Code Execution Safety
- [ ] No `eval()` / `exec()` on raw user input outside the sandbox
- [ ] No `pickle.load()`, `yaml.load()` (use `yaml.safe_load`), `dill.load` on untrusted data
- [ ] Subprocess calls use list args, not `shell=True` with interpolated strings
- [ ] No path traversal in file operations (validate against allowlist of dirs)

### Configuration & Secrets
- [ ] No hardcoded API keys, passwords, tokens
- [ ] Secrets loaded from environment, vault, or parameter store
- [ ] `.env` files in `.gitignore`, not committed
- [ ] Default credentials changed (admin:admin etc.)
- [ ] Database connection strings use IAM auth or short-lived credentials where possible

### Dependencies
- [ ] `pyproject.toml`/`requirements.txt` pins versions (no floating `*`)
- [ ] No known-vulnerable versions (run `pip-audit` or equivalent)
- [ ] License audit complete
- [ ] No deprecated cryptography (md5, sha1 for security purposes, pycrypto)

### Model Loading
- [ ] Model weights loaded from trusted source (verified hash)
- [ ] No `weights_only=False` in `torch.load` for untrusted checkpoints
- [ ] Custom model classes don't enable arbitrary code execution on load

---

## Common Advisory Templates

### Unauthenticated execution endpoint

```markdown
## Advisory N: Unauthenticated code execution endpoint
- **Severity:** High
- **Status:** Open
- **Owner:** <service team>

### Impact
The sandbox service accepts and executes arbitrary <language> code via HTTP without authentication. If an attacker can reach the endpoint, this enables remote code execution within the sandbox container and can be used for abuse, data exfiltration attempts, and further pivoting.

### Attack Preconditions
- Sandbox container is running.
- Endpoint is reachable from any untrusted context (misconfigured port exposure, shared host/network, forwarded ports, CI/dev environments).
- No compensating controls (network ACL, reverse proxy auth, mTLS) are enforced.

### Evidence
- `<path/to/server.py>`
- `<path/to/start_background.sh>`

### Recommended Remediation
1. Require authentication for execute (bearer token or mTLS).
2. Bind service to localhost-only unless explicitly configured otherwise.
3. Enforce request schema validation, max payload size, and strict timeout caps.
4. Add rate limiting and structured audit logs for all execution calls.

### Verification
- Unauthenticated request to execute is rejected with 401/403.
- Authenticated valid request succeeds.
- Requests from non-local/untrusted sources are blocked by default deployment.
```

### Weak container isolation

```markdown
## Advisory N: Weak sandbox container isolation defaults
- **Severity:** High
- **Status:** Open
- **Owner:** Platform/DevOps + <service team>

### Impact
Running attacker-controlled code in a container with default privileges/networking and root user materially increases blast radius if the container is compromised or abused.

### Attack Preconditions
- Adversary can submit code to sandbox service.
- Container runtime policy is default/non-hardened.
- Host or neighboring workloads are accessible via network or mounted resources.

### Evidence
- `<path/to/Dockerfile>`
- `<path/to/start_background.sh>`

### Recommended Remediation
1. Run as non-root user in the image (`USER` directive).
2. Start container with hardened flags:
   - `--read-only`
   - `--cap-drop=ALL`
   - `--security-opt no-new-privileges:true`
   - `--pids-limit`, `--memory`, `--cpus`
   - `--network=none` (or strict allowlist networking only if required)
3. Mount a minimal writable `tmpfs` for execution scratch.
4. Add seccomp/AppArmor profiles and egress controls.

### Verification
- Container process runs as non-root.
- Capability set is empty/minimal.
- Outbound network is blocked unless explicitly allowlisted.
- Resource exhaustion tests are contained by limits.
```
