---
category: security
audience: operators
area: release-pipeline
action: none
breaking: false
---
Trivy now resolves the trusted-registry data from the repository root before starting filesystem misconfiguration checks, so the full severity security scan can run reliably in CI.
