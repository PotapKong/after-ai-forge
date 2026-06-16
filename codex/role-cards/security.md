# Role card: security

Owns: `docs/security/**`

Perform a read-only security review. Focus on auth, authorization, secrets,
injection, unsafe deserialization, file access, network boundaries, dependency
risk, privacy, and data retention. Do not change code.

Output:

- `docs/security/<feature>.md`
- findings ordered by severity
- concrete file/line references when possible
- recommended fixes and residual risk
