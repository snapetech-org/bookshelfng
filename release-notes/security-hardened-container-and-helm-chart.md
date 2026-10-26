---
category: security
audience: operators
area: packaging
action: Before upgrading, confirm the existing /config volume is writable by GID 10001.
breaking: true
---
The Helm chart now runs without root privileges, drops all Linux capabilities, applies resource bounds, and includes container health checks. Confirm access to an existing `/config` volume before upgrading; this Kubernetes configuration uses UID/GID 10001 instead of PUID/PGID.
