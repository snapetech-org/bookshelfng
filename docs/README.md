# Documentation index

Use the [main README](../README.md) for the project overview, quick start, and
metadata provider configuration.

## Product behavior and library workflows

| Guide | Covers |
| --- | --- |
| [Setup experience contract](maintainers/setup-experience-contract.md) | Keep setup work focused on the existing, fail-closed migration to ChaptarrNG during retirement |
| [Fork rationale, capabilities, and compatibility](capabilities-and-compatibility.md) | Why BookshelfNG is maintained, its standalone and SeerrNG features, upstream comparison, and replacement criteria |
| [Import matching and formats](import-matching-and-formats.md) | Coexisting ebook and audiobook files, import thresholds, weighted edition terms, and preferred series |
| [Catalog metadata and unmapped files](catalog-metadata-and-unmapped-files.md) | Combining metadata, covers, and author images across catalogs; retrying unmapped files with the UI, API, or CLI |
| [Media storage](media-storage.md) | Initializing new authors' format paths, per-author and bulk moves, previews, API/CLI usage, permissions, and library consolidation |
| [Search and downloads](search-and-downloads.md) | Add-page catalog search, torrent and direct-download indexers, browser-assisted link resolution, torrent adoption, and queue handling |
| [Series pack search](series-pack-search.md) | Searching a series and reviewing multi-book packs in Manual Import |
| [Author metadata refresh](author-metadata-refresh.md) | Stored author metadata, refresh schedule, request limits, and troubleshooting |
| [Encrypted portable backups](encrypted-backups.md) | Passphrase-protected backup export, restore, API routes, and file format |
| [Reporting issues](reporting-issues.md) | Which application and container logs to include for UI and API failures |

## Audiobooks and integrations

| Guide | Covers |
| --- | --- |
| [Audiobook metadata](audiobookshelf-metadata.md) | Narrator fields and tags, plus Audiobookshelf OPF sidecars |
| [Audiobook M4B merging](audiobook-m4b-merging.md) | Combining multi-track downloads into chaptered M4B files |
| [BookLore integration](booklore-integration.md) | Uploading imported files to BookLore BookDrop |

## Installation and release operations

| Guide | Covers |
| --- | --- |
| [Move BookshelfNG to ChaptarrNG](migrate-from-bookshelfng-to-chaptarrng.md) | The final-release helper, complete appdata snapshots, preview/apply/rollback commands, media review, and supported migration limits |
| [Standalone installation](standalone-install.md) | Native archives, Windows installer, packages, and platform setup |
| [Distribution channels](distribution.md) | Published artifacts, release destinations, and publisher configuration |
| [BookshelfNG .NET 10 source builds (archive)](dotnet-10-platform-builds.md) | Legacy BookshelfNG backend and UI build, including its Linux x86 and FreeBSD runtime packs; these are not ChaptarrNG targets |
| [Release-note fragments](../release-notes/README.md) | User-facing release-note format and preview command |
| [Legacy optional diagnostics module (archive)](https://github.com/snapetech-org/chaptarrng/blob/main/docs/OPTIONAL_DIAGNOSTICS.md) | ChaptarrNG's disabled-by-default replacement, aggregate events, explicit opt-in, and privacy limits |

## Fork consolidation and retirement

Current status (2026-10-20): BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` is at [`a733e5f4`](https://github.com/snapetech-org/chaptarrng/commit/a733e5f473025bc6b85f0116a01960912245c2c8). Recent fixes restore exact Direct Download ebook format matching, preserve unrelated ebook containers during audiobook upgrades, reinstate the configured free-space check for imports, and make bulk library and import-list actions retryable. Exact-head Build [39528253542](https://github.com/snapetech-org/chaptarrng/actions/runs/39528253542) and CodeQL [39528252358](https://github.com/snapetech-org/chaptarrng/actions/runs/39528252358) are running; Semgrep [39528253768](https://github.com/snapetech-org/chaptarrng/actions/runs/39528253768), Trivy [39528253623](https://github.com/snapetech-org/chaptarrng/actions/runs/39528253623), Security analysis [39528253699](https://github.com/snapetech-org/chaptarrng/actions/runs/39528253699), and dependency submission [39528259936](https://github.com/snapetech-org/chaptarrng/actions/runs/39528259936) passed. No release, package, image, or migration bridge was published; operator-data, rollback, integration, and installed channel acceptance remain open.

The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `a733e5f473025bc6b85f0116a01960912245c2c8`. It covers 732 post-fork commits (723 absent from pinned upstream history) and 1,119 changed paths: 81 reviewed mappings and 653 reviewed dispositions (177 retained, 132 equivalent, 172 ported, and 172 non-runtime retirements). Another 466 paths remain open (141 without mapped targets and 325 requiring semantic review). This pass reviewed five media-import and replacement code/test paths, including format-safe upgrades and direct-import free-space checks; the exact-head Build is running. Path-level coverage is not feature-parity proof, and no runtime retirement is approved. Keep BookshelfNG in service; representative data, real rollback, provider fulfillment, installed channel handoff, and operator acceptance remain open. No release or bridge was published.

| Guide | Covers |
| --- | --- |
| [Setup experience contract](maintainers/setup-experience-contract.md) | Keep setup work focused on the existing, fail-closed migration to ChaptarrNG during retirement |
| [BookshelfNG feature inventory and ChaptarrNG retirement matrix](maintainers/bookshelfng-parity-roadmap.md) | BookshelfNG enhancements that must be ported or replaced before this fork can retire |
| [BookshelfNG to ChaptarrNG consolidation report](maintainers/chaptarr-consolidation.md) | Full source inventory, database conversion contract, distribution bridge, evidence, and release gates |
