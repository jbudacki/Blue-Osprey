# Cryptographic Security Reference

## Algorithm Security Status

| Algorithm | Type | Status | Recommendation |
|-----------|------|--------|----------------|
| **MD5** | Hash | 🔴 Broken | Replace with SHA-256 or better. |
| **SHA-1** | Hash | 🔴 Broken | Replace with SHA-256 or better. |
| **SHA-256/512** | Hash | 🟢 Secure | Use for general hashing. |
| **DES** | Symmetric | 🔴 Broken | Replace with AES-GCM (256-bit). |
| **3DES** | Symmetric | 🟡 Legacy | Replace with AES-GCM (256-bit). |
| **AES-ECB** | Symmetric | 🔴 Insecure | Never use. Use GCM or CBC with random IV. |
| **AES-GCM** | Symmetric | 🟢 Secure | Recommended for authenticated encryption. |
| **RSA-1024** | Asymmetric | 🔴 Broken | Minimum 2048-bit; recommend 4096-bit. |
| **ECDSA** | Asymmetric | 🟢 Secure | Use NIST P-256 or Ed25519. |

## Common Vulnerability Patterns

1. **ECB Mode (Electronic Codebook)**: Identical plaintext blocks result in identical ciphertext blocks, leaking patterns.
2. **Hardcoded IV/Nonce**: Reusing an Initialization Vector with the same key breaks security (especially in GCM/CTR).
3. **Insufficient Hashing Rounds**: Using low iteration counts for bcrypt/PBKDF2 makes passwords vulnerable to GPU cracking.
4. **Encoding as Encryption**: Confusing Base64, Hex, or XOR with actual cryptographic protection.
5. **Insecure RNG**: Using `random.random()` or `Math.random()` instead of CSPRNGs (e.g., `os.urandom`, `crypto.getRandomValues`).

## Post-Quantum Readiness (PQC)

Current RSA and Elliptic Curve algorithms are vulnerable to future quantum computers. 
*   **Transition Plan**: Start inventorying usage and look for "hybrid" deployment options.
*   **Algorithms to Watch**: ML-KEM (Kyber), ML-DSA (Dilithium).
