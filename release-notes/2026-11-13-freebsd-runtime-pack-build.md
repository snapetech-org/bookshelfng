---
category: changed
audience: operators
area: packaging
action: none
breaking: false
---
FreeBSD's BookshelfNG runtime-pack build now skips the unused Crossgen2 SFX package, informed by [@Thefrank's issue #104497](https://github.com/dotnet/runtime/issues/104497) and [@am11's fix in PR #105004](https://github.com/dotnet/runtime/pull/105004) to dotnet/runtime. BookshelfNG independently adapted the change; neither person contributed to this fork.
