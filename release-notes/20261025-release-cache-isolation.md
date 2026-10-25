---
category: security
audience: operators
area: ci
action: none
breaking: false
---
Disable GitHub Actions cache access for the standalone release and recovery workflows. Jobs that process release artifacts can no longer read or write shared Actions caches, including when invoked through manual publisher recovery.
