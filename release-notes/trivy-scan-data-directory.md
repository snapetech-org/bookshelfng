---
category: security
audience: operators
area: release-pipeline
action: none
breaking: false
---
Trivy now reads the trusted-registry override from a dedicated directory of custom Rego data, matching its recursive loader so filesystem misconfiguration scans can apply the KSV-0125 registry exception.
