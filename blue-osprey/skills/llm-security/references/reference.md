# OWASP Top 10 for LLM Applications (2025)

## Categories

1.  **LLM01: Prompt Injection**
    *   **Description**: Manipulating LLM outputs via crafted inputs to bypass filters or execute unauthorized actions.
    *   **Red Flags**: Direct concatenation of user input into prompts, lack of delimiters, no input validation.

2.  **LLM02: Insecure Output Handling**
    *   **Description**: Failing to sanitize LLM outputs before passing them to downstream functions (e.g., `eval`, `innerHTML`, SQL).
    *   **Red Flags**: `eval(response)`, `innerHTML = response`, unparameterized SQL queries using LLM output.

3.  **LLM03: Training Data Poisoning**
    *   **Description**: Tampering with training data or fine-tuning sets to introduce backdoors or biases.
    *   **Red Flags**: Lack of verification for external data sources, no anomaly detection in training sets.

4.  **LLM04: Model Theft**
    *   **Description**: Unauthorized access or exfiltration of proprietary models or weights.
    *   **Red Flags**: Unprotected model endpoints, lack of rate limiting on inference, insecure model storage.

5.  **LLM05: Supply Chain Vulnerabilities**
    *   **Description**: Using compromised third-party models, libraries (LangChain, OpenAI SDK), or data.
    *   **Red Flags**: Unpinned dependencies, lack of integrity checks for model weights, using obscure or unverified models.

6.  **LLM06: Sensitive Information Disclosure**
    *   **Description**: LLM reveals confidential data (PII, secrets, system info) via its output.
    *   **Red Flags**: PII in training data, secrets in system prompts, lack of output filtering.

7.  **LLM07: Insecure Plugin Design**
    *   **Description**: Plugins/Tools with excessive permissions or poor input validation.
    *   **Red Flags**: Plugins with destructive capabilities (e.g., `rm -rf`), lack of human-in-the-loop for sensitive actions.

8.  **LLM08: Excessive Agency**
    *   **Description**: LLM granted too many permissions, allowing it to perform unauthorized actions in the application environment.
    *   **Red Flags**: LLM having write access to databases, ability to send emails or make financial transactions without approval.

9.  **LLM09: Overreliance**
    *   **Description**: Application or users trusting LLM output without verification, leading to errors or security breaches.
    *   **Red Flags**: Automatic execution of LLM-generated code, no attribution or source verification.

10. **LLM10: Model Denial of Service**
    *   **Description**: Overloading the LLM with complex or massive inputs to exhaust resources or incur high costs.
    *   **Red Flags**: No rate limiting, no input size limits, high timeout values.

## Severity Classification

*   **Critical**: Prompt injection leading to data exfiltration, remote code execution via output, hardcoded API keys.
*   **High**: PII disclosure, destructive actions without approval, vulnerable dependencies.
*   **Medium**: Lack of rate limiting, high temperature in security tasks, minor configuration issues.
*   **Low**: Informational findings, minor best practice deviations.
