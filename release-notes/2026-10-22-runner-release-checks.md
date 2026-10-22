---
category: fixed
audience: operators
area: ci
action: none
breaking: false
---

The release-note check now calls GitHub's API with curl, so it works on the minimal shared runner without relying on the optional GitHub CLI.
