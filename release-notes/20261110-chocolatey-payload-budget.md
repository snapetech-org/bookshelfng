---
category: changed
audience: operators
area: packaging
action: none
breaking: false
---
Chocolatey publication now rejects the Windows x64 ZIP if it exceeds 190,000,000 bytes, preventing scanner-size regressions. This checks the ZIP used by Chocolatey, not the separate Windows setup executable.
