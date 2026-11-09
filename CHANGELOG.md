# Changelog

## [0.4.21.84](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.83..v0.4.21.84) - 2026-11-09

### Fixed

- Patch the active hosted .NET SDK's runtime metadata before restoring community Linux x86 and FreeBSD packs. The release job no longer patches an installed-but-inactive SDK servicing version.

## [0.4.21.83](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.82..v0.4.21.83) - 2026-11-09

### Fixed

- Pin the complete self-contained release restore graph to .NET 10.0.12 when building the community Linux x86 and FreeBSD packs, because MSBuild resolves the full runtime matrix together; ordinary builds continue using the latest 10.0.x servicing patch.

## [0.4.21.82](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.81..v0.4.21.82) - 2026-11-09

### Fixed

- Keep only the community-supplied Linux x86 and FreeBSD runtime archives on their available .NET 10.0.12 servicing packs while standard supported platforms continue using the patched 10.0.14 runtime.

## [0.4.21.81](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.80..v0.4.21.81) - 2026-11-09

### Fixed

- Normalize the retained public-fork validation release note to the current audience, area, action, and breaking-change metadata contract.

## [0.4.21.80](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.79..v0.4.21.80) - 2026-11-09

### Security

- Refresh the Alpine base and update the bundled .NET runtime to 10.0.14, resolving the fixable curl/libcurl and .NET runtime findings reported by the published-image release scan.

## [0.4.21.79](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.78..v0.4.21.79) - 2026-11-09

### Fixed

- Align the ChaptarrNG bridge release gate with its hosted-compatible wrapper condition so the release source validates cleanly.

## [0.4.21.78](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.77..v0.4.21.78) - 2026-11-09

### Upstream source attribution

- Publish the complete ten-record Bookshelf/Chaptarr attribution ledger, including the reviewed-but-not-shipped Chaptarr consolidation reference, with upstream author links and explicit dispositions.

### Fixed

- Restore compatible GitHub-hosted build, test, package, scan, and release routes while retaining dedicated isolation only where the trust boundary requires it.

## [0.4.21.77](https://github.com/snapetech-org/bookshelfng/compare/v0.4.21.76..v0.4.21.77) - 2026-11-09

### Upstream source attribution

- Publicly credit ten Bookshelf and Chaptarr issues and pull requests whose upstream code, reports, ideas, or validation records informed BookshelfNG behavior or maintained consolidation work. The [source ledger](UPSTREAM_ATTRIBUTION.md) separates implemented adaptations from reviewed-but-not-shipped provenance and makes clear that those people contributed upstream, not directly to this fork.
