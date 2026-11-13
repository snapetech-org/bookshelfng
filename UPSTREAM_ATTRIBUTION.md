# Upstream source attribution

This ledger publicly credits 10 source records from upstream Bookshelf and Chaptarr that informed implemented behavior or maintained consolidation work in this fork.

The linked people made their reports, suggestions, discussions, or code contributions to the upstream project. This is source credit only: it does not claim that they contributed directly to this fork, endorsed it, or participated in the fork integration. Fork maintainers adapted, integrated, or verified the resulting behavior separately.

The list covers issue-driven features and upstream PR branches explicitly merged by BookshelfNG, one later Chaptarr performance adaptation, and one Chaptarr record retained by the consolidation review without a shipping claim.

## Credited Bookshelf sources

BookshelfNG integrated or adapted these upstream Bookshelf records.

- [issue #7](https://github.com/pennydreadful/bookshelf/issues/7) — “FR: Allow Spoken and ebook to exist in the same directory,” opened upstream by [@Jdiesel87](https://github.com/Jdiesel87). BookshelfNG integrated or adapted the upstream behavior.
- [issue #64](https://github.com/pennydreadful/bookshelf/issues/64) — “\[ENH\] Edition Filter,” opened upstream by [@SystemIdleProcess](https://github.com/SystemIdleProcess). BookshelfNG integrated or adapted the upstream behavior.
- [issue #97](https://github.com/pennydreadful/bookshelf/issues/97) — “Allow multiple formats for a single book,” opened upstream by [@nickuhlig](https://github.com/nickuhlig). BookshelfNG integrated or adapted the upstream behavior.
- [issue #126](https://github.com/pennydreadful/bookshelf/issues/126) — “\[Feature Request\] Set "Preferred Series",” opened upstream by [@dobbleg1000](https://github.com/dobbleg1000). BookshelfNG integrated or adapted the upstream behavior.
- [PR #185](https://github.com/pennydreadful/bookshelf/pull/185) — “Fix data loss when importing a book matched to the wrong file.,” opened upstream by [@nightah](https://github.com/nightah). BookshelfNG integrated or adapted the upstream behavior.
- [PR #186](https://github.com/pennydreadful/bookshelf/pull/186) — “fix(import): don't abort the library scan on a book with no monitored edition,” opened upstream by [@4o66](https://github.com/4o66). BookshelfNG integrated or adapted the upstream behavior.
- [PR #187](https://github.com/pennydreadful/bookshelf/pull/187) — “fix(scan): scheduled RescanFolders should reconsider unmatched files,” opened upstream by [@4o66](https://github.com/4o66). BookshelfNG integrated or adapted the upstream behavior.
- [PR #188](https://github.com/pennydreadful/bookshelf/pull/188) — “fix(import): search results matched to a DB book keep its BookFiles,” opened upstream by [@luisqagt](https://github.com/luisqagt). BookshelfNG integrated or adapted the upstream behavior.

## Credited Chaptarr source

This later Chaptarr contribution was also adapted into BookshelfNG.

- [PR #218](https://github.com/Chaptarr/chaptarr/pull/218) — “perf(books): reuse the author book list and cache BuildWorkGroups per author (#163, #172),” opened upstream by [@jordanfelle](https://github.com/jordanfelle). BookshelfNG independently adapted the upstream Chaptarr contribution.

## Reviewed Chaptarr source, not claimed as shipped

- [PR #114](https://github.com/Chaptarr/chaptarr/pull/114) — “fix(api): preserve media type for scoped book lookup,” opened upstream by [@snapetech](https://github.com/snapetech). BookshelfNG’s maintained Chaptarr consolidation review cites this upstream validation record; the citation does not claim that PR #114 was implemented in or contributed directly to BookshelfNG.

## Reviewed .NET runtime source and BookshelfNG disposition

- [dotnet/runtime issue #104497](https://github.com/dotnet/runtime/issues/104497) — cross-built FreeBSD ILCompiler packaging, reported upstream by [@Thefrank](https://github.com/Thefrank), and resolved upstream by [PR #105004](https://github.com/dotnet/runtime/pull/105004) from [@am11](https://github.com/am11). BookshelfNG independently narrows its custom FreeBSD runtime-pack build by omitting the unused Crossgen2 SFX package after the .NET 10.0.15 packaging step failed on missing framework dependencies. This does not adopt the upstream two-stage ILCompiler build or claim either upstream author contributed directly to BookshelfNG.

_Attribution ledger refreshed 2026-11-13; 12 source records._
