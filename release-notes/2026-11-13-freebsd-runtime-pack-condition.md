---
category: fixed
audience: operators
area: packaging
action: none
breaking: false
---
The FreeBSD runtime-pack build now applies its Crossgen2 SFX exclusion to the clean FreeBSD source tree before compiling. This keeps the unused package's unresolved framework dependencies from stopping the .NET 10.0.15 runtime pack build.
