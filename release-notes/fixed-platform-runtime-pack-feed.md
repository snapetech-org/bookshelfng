---
category: fixed
audience: operators
area: release-pipeline
action: none
breaking: false
---
The FreeBSD ASP.NET Core runtime-pack build now reuses the runtime feed already configured for the target, avoiding a duplicate NuGet source error and allowing Linux x86 and FreeBSD package artifacts to finish staging.
