## Packaging

- BookshelfNG's custom FreeBSD runtime-pack build now skips the unused Crossgen2 SFX package. This change was informed by [@Thefrank's upstream dotnet/runtime issue #104497](https://github.com/dotnet/runtime/issues/104497) and its upstream resolution, [PR #105004 by @am11](https://github.com/dotnet/runtime/pull/105004). BookshelfNG independently adapted its release build; neither person contributed directly to this fork.
