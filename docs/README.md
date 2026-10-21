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

BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` and application code are at [`6fc744ef`](https://github.com/snapetech-org/chaptarrng/commit/6fc744ef3db7aba815e7669f3794260c236a5a2a). Current source includes the disabled-by-default BookshelfNG issue [#114](https://github.com/snapetech-org/bookshelfng/issues/114) author-path setting and migration support, format-specific metadata-profile refresh, Calibre English language compatibility, whole-author path updates on folder moves, and the reviewed book-file organization/transfer port. These changes remain unpublished in `.977`. Exact-head Build [39542301711](https://github.com/snapetech-org/chaptarrng/actions/runs/39542301711) for `6fc744ef` passed Linux and PostgreSQL migration; macOS and Windows lanes are still running. CodeQL, security analysis, Semgrep, Trivy, and dependency submission passed. Focused fixtures pass author/migration 11/11, configuration persistence 1/1, format-profile refresh 5/5, Calibre language 4/4, Calibre proxy/series 6/6, book-file move planning 15/15, and whole-author move paths 3/3. No release, tag, package, image, installer, or migration bridge has been published. Representative operator-data migration and rollback, complete feature/data acceptance, provider and SeerrNG workflows, installed update-channel handoff, and operator acceptance remain open; keep BookshelfNG in service.

The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `6fc744ef3db7aba815e7669f3794260c236a5a2a`. It covers 732 post-fork commits (723 absent from pinned upstream history) and 1,119 changed paths: 85 reviewed mappings and 713 reviewed dispositions (177 retained, 133 equivalent, 232 ported, and 171 non-runtime retirements). Another 406 paths remain open (136 without mapped targets and 270 requiring semantic review). Recent passes dispositioned backup/restore, optional diagnostics, the BookshelfNG migration controller, six historical SQLite migration paths, author refresh, book-added handling, format-scoped media moves, author profile refresh, Calibre language compatibility, and edition metadata and selection, format-aware author/book operations, Calibre proxy behavior, book-file organization and move behavior, and series scoping, repository/cutoff search semantics, and API resource/backup behavior, release-search responses, and guarded command routes, and metadata-profile schema behavior using source and fixture evidence. Path-level coverage is not feature-parity proof, and no runtime retirement is approved.

| Guide | Covers |
| --- | --- |
| [Setup experience contract](maintainers/setup-experience-contract.md) | Keep setup work focused on the existing, fail-closed migration to ChaptarrNG during retirement |
| [BookshelfNG feature inventory and ChaptarrNG retirement matrix](maintainers/bookshelfng-parity-roadmap.md) | BookshelfNG enhancements that must be ported or replaced before this fork can retire |
| [BookshelfNG to ChaptarrNG consolidation report](maintainers/chaptarr-consolidation.md) | Full source inventory, database conversion contract, distribution bridge, evidence, and release gates |
