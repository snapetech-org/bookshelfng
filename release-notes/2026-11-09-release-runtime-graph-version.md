---
category: fixed
audience: operators
area: release-infrastructure
action: none
breaking: false
---

Self-contained releases now restore every runtime identifier against .NET 10.0.12 when the community Linux x86 and FreeBSD packs are enabled, matching MSBuild's solution-wide runtime graph while leaving ordinary builds on the latest servicing patch.
