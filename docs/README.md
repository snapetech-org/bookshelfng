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

BookshelfNG `0.4.21.71` remains the final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` now contains the 10-RID standalone archive candidate at code and main head [`4d9c4b2d`](https://github.com/snapetech-org/chaptarrng/commit/4d9c4b2db0f438f05d81fb109aa6c32924ec5e85). Exact-head Build [39573719771](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719771) and no-publication standalone validation [39573719493](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719493) are in progress. Security analysis [39573719545](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719545), Trivy [39573719526](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719526), Semgrep [39573719587](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719587), and dependency submission [39573720905](https://github.com/snapetech-org/chaptarrng/actions/runs/39573720905) passed; CodeQL [39573719260](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719260) is in progress. No release, package, image, installer, or migration bridge has been published.

The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG code candidate `4d9c4b2db0f438f05d81fb109aa6c32924ec5e85`: 1,119 changed paths, 102 reviewed mappings, and 821 explicit dispositions (177 retained, 135 equivalent, 270 ported, and 239 repository-only retirements). Another 298 paths remain open (68 without mapped targets and 230 requiring semantic review). No runtime feature retirement is approved; path review is not feature-parity proof. Synthetic migration and rollback evidence is recorded, but representative operator data, installed-channel handoff, provider and SeerrNG acceptance, and operator sign-off remain open. No release or cutover has been authorized.

| Guide | Covers |
| --- | --- |
| [Setup experience contract](maintainers/setup-experience-contract.md) | Keep setup work focused on the existing, fail-closed migration to ChaptarrNG during retirement |
| [BookshelfNG feature inventory and ChaptarrNG retirement matrix](maintainers/bookshelfng-parity-roadmap.md) | BookshelfNG enhancements that must be ported or replaced before this fork can retire |
| [BookshelfNG to ChaptarrNG consolidation report](maintainers/chaptarr-consolidation.md) | Full source inventory, database conversion contract, distribution bridge, evidence, and release gates |
