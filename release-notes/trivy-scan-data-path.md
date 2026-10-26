---
category: security
audience: operators
area: release-pipeline
action: none
breaking: false
---
Trivy now reads the trusted-registry override from a dedicated custom-data directory during filesystem misconfiguration checks, matching its recursive Rego data loader so the full severity security scan can run reliably in CI.
