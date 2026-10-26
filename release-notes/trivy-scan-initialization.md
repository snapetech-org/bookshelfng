---
category: security
audience: operators
area: release-pipeline
action: none
breaking: false
---
Trivy now loads the project's trusted-registry data through its filesystem scan command. This lets the required dependency, misconfiguration, and secret checks complete before release.
