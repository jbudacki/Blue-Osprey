# Security Principles Rubric

## Core Principles (7)

1. **Secure by Default**
   - **Definition**: Security is intrinsic and built-in, not an opt-in feature. The easiest path for a user or developer must also be the most secure path.
   - **Signals**: Hardened defaults, no "expert-only" security configurations required for basic safety, automated provisioning of secrets/certs.

2. **Constructive Friction**
   - **Definition**: The "right" thing (secure) is streamlined and frictionless. The "wrong" thing (insecure) is met with intentional, constructive resistance (not just a "no", but a requirement for higher scrutiny or alternative paths).
   - **Signals**: Automated guardrails, fast-track approvals for standard designs, manual review triggers for non-standard/high-risk exceptions.

3. **Shift Left & Shield Right**
   - **Definition**: Security engagement starts at the design phase (Shift Left) AND is continuously enforced by automated governance and monitoring in production (Shield Right).
   - **Signals**: Threat modeling in RFCs, IDE-integrated linting, runtime security policies, automated teardown of non-compliant infrastructure.

4. **Risk-Based Pragmatism**
   - **Definition**: Resources and scrutiny are concentrated on the highest-risk areas. Security does not treat a internal tool's CSS change with the same weight as a public-facing API's auth change.
   - **Signals**: Tiered review processes, clear risk categorization, willingness to accept low-impact risks to move faster on high-impact ones.

5. **Intelligence Feedback Loop**
   - **Definition**: Real-world signals (incidents, bug bounty findings, audit results) drive systemic, architectural fixes rather than one-off patches. There is a culture of humility regarding unknown risks.
   - **Signals**: Post-mortem action items that fix classes of bugs, trend analysis of vulnerability data, proactive hunting for "unknown unknowns."

6. **Partnership over Policing**
   - **Definition**: Security teams act as enablers and consultants to engineering, not just as auditors or "gatekeepers." Success is measured by the security of the product, not the number of findings.
   - **Signals**: Shared goals between security and dev, security "champions" programs, collaborative remediation.

7. **Transparent Criteria**
   - **Definition**: Security expectations, standards, and review criteria are documented and openly shared. Teams should be able to predict a security verdict before they even submit for review.
   - **Signals**: Publicly available security checklists, self-service security portals, clear SLAs for reviews.

---

## Anti-Patterns (6)

1. **Compliance Theater**
   - **Description**: Performing security activities to "check a box" or satisfy an auditor rather than to meaningfully reduce risk.
   - **Indicator**: Reviews that ask "did you do X?" without verifying *how* or *if* X actually works in this context.

2. **Manual Stop-Gap**
   - **Description**: Using expensive human expert cycles to perform repetitive tasks that should be handled by automation, scanners, or platform defaults.
   - **Indicator**: Security engineers manually reviewing every firewall change or dependency update.

3. **Proxy for Product Context**
   - **Description**: The security team attempts to act as the intermediary or "owner" of product knowledge that the engineering/product teams should hold themselves.
   - **Indicator**: Security making decisions about business risk without the business owner's involvement.

4. **Department of No**
   - **Description**: Blocking a feature or proposal because of risk without providing a clear, supported, and secure alternative path forward.
   - **Indicator**: "You can't use X" followed by silence, rather than "You can't use X, but here is the approved pattern for Y."

5. **One-Size-Fits-All Bureaucracy**
   - **Description**: Imposing the same heavy-weight process, documentation, and review requirements on all changes regardless of their risk profile.
   - **Indicator**: A 3-week security review required for a change to an internal-only documentation site.

6. **Throw It Over the Wall**
   - **Description**: Dumping large volumes of unverified, high-false-positive security findings on engineering teams without prior triage or context.
   - **Indicator**: Sending a raw 200-page PDF report from a generic scanner to a dev team and asking them to "fix everything."
