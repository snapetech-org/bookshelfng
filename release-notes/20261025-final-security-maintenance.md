---
category: security
audience: operators
area: dependencies
action: none
breaking: false
---
Updates the frontend lint toolchain's `zod` dependency to patched version 4.6.6, resolving GHSA-mrhx-c7xc-m3w5, and makes the required Trivy source scan fail closed when it cannot inspect the repository. Release asset builds disable setup-node's automatic package-manager cache after downloading runtime-pack artifacts, closing the remaining CodeQL cache-poisoning path. High-severity findings in the LinuxServer startup configuration remain covered by narrow, expiring exceptions documented in `security/trivy-exceptions.yaml`.
