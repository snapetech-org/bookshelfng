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
| [.NET 10 source builds](dotnet-10-platform-builds.md) | Complete backend and UI builds, plus Linux x86 and FreeBSD runtime packs |
| [Release-note fragments](../release-notes/README.md) | User-facing release-note format and preview command |
| [Optional diagnostics module](../src/Bookshelf.Diagnostics/README.md) | Installation, configuration, and exported data |

## Fork consolidation and retirement

Current status (2026-10-20): BookshelfNG `0.4.21.71` remains its final public release and ChaptarrNG `v0.9.977` its latest. ChaptarrNG's migration candidate code is at `55f6ae1a2eac79e2af4ae9a7a2d92cd827ab5ad1`, adding the Books index Both filter, combined Bookshelf Formats view, interactive series-pack search, hash-based torrent adoption, edition/narrator retry actions, restricted audiobook-scoped SeerrNG narrator operations, and responsive UI shell/theme updates. Exact-head Build [39474807076](https://github.com/snapetech-org/chaptarrng/actions/runs/39474807076) passed Linux, Windows, and PostgreSQL migration jobs; Windows installer upgrade/rollback checks passed. macOS was cancelled before runner setup on both attempts, so no macOS result is available. No release or package was prepared; operator-data and channel acceptance remain open.

The schema-v4 inventory pins BookshelfNG `c63eb84813392cdb398d9e6bf4446694952f256d` to ChaptarrNG `main` at `cc9be068bd0b8d430a640a0b0562026ed2929c6b`: 679 post-fork commits, 1,116 paths, 35 reviewed mappings, and 501 dispositions (177 retained, 129 equivalent, 33 ported, 162 non-runtime retirements). Another 615 paths remain open (226 unmapped, 389 requiring semantic review). One exact-identical file is now recorded as retained. Path review does not establish feature parity. Keep BookshelfNG in service; representative data, rollback, provider fulfillment, installed channel handoff, and operator acceptance remain open. No release or bridge was published.

| Guide | Covers |
| --- | --- |
| [Setup experience contract](maintainers/setup-experience-contract.md) | Keep setup work focused on the existing, fail-closed migration to ChaptarrNG during retirement |
| [BookshelfNG feature inventory and ChaptarrNG retirement matrix](maintainers/bookshelfng-parity-roadmap.md) | BookshelfNG enhancements that must be ported or replaced before this fork can retire |
| [BookshelfNG to ChaptarrNG consolidation report](maintainers/chaptarr-consolidation.md) | Full source inventory, database conversion contract, distribution bridge, evidence, and release gates |
