---
category: security
audience: operators
area: release-pipeline
action: none
breaking: false
---

Docker builds now omit local environment files, license files, and signing material from the build context while keeping the example environment file available.
