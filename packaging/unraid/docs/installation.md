# Install BookshelfNG on Unraid

BookshelfNG is a Snapetech NG fork of Bookshelf for ebook and audiobook library
management and acquisition. It works independently; SeerrNG integration is optional.

> **Latest published releases:** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977`. The published ChaptarrNG migration supports migration-158 SQLite; older schemas and PostgreSQL sources are unsupported by that release.
>
> ChaptarrNG PR #131 remains draft. Its application-code snapshot is `50e4cc14cf9cf87bbfeebbbb114cadbbeab6b5a3`, which merges current main at `95f112e7` and includes the stable `master` image alias; the current documentation-only PR head is `f0acc9dce90da958b73ba4ed7bbf05f40bde3a29`. The alias regression script passes locally. Exact-head Build [39221717722](https://github.com/snapetech-org/chaptarrng/actions/runs/39221717722) passed against that PR head (merge candidate `c859c45e6eeff894789a3e884df96a4c8fd057ac`): Linux 4,412 passed/0 failed, macOS 4,407/0, Windows 4,373/0, and PostgreSQL migration fixtures 53/0; all four validation receipts reconciled. CodeQL [39221713053](https://github.com/snapetech-org/chaptarrng/actions/runs/39221713053), security analysis [39221717638](https://github.com/snapetech-org/chaptarrng/actions/runs/39221717638), NuGet submission [39221720997](https://github.com/snapetech-org/chaptarrng/actions/runs/39221720997), and dependency review [39221717657](https://github.com/snapetech-org/chaptarrng/actions/runs/39221717657) passed. The release-note contract passed; disposable-fork validation was skipped by its external-fork gate. Keep the release freeze in place; representative-data, parity disposition, installed-rollback, and update-channel acceptance remain open. Do not point ChaptarrNG at live BookshelfNG appdata or use the candidate restore flow for production migration.
>
> The Unraid transition [PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) also remains a draft. Its template-preservation check passes, but the real Community Applications upgrade and rollback flow has not been accepted. Both release-readiness gates remain unset; no migration bridge is published.

## Existing installations

Keep the current BookshelfNG image until you are ready to migrate. The legacy
Community Apps template on `main` still points to BookshelfNG. A transition
candidate preserves its appdata path, port, media/download mappings, user IDs,
timezone, and Hardcover settings while switching to the standard ChaptarrNG
image. It is not published and must remain on its feature branch until the
application release and Unraid update-flow gates pass. The XML and
settings-preservation check passed; run
`python3 scripts/test-transition-template.py` to repeat it.
Read the
[BookshelfNG-to-ChaptarrNG migration guide](https://github.com/snapetech-org/bookshelfng/blob/main/docs/migrate-from-bookshelfng-to-chaptarrng.md),
upgrade BookshelfNG to `.71`, stop the service, and keep an independent
appdata backup before switching. New installations should use the
[ChaptarrNG Unraid template](https://github.com/snapetech-org/chaptarrng-unraid).
For a manual BookshelfNG install needed to inspect or roll back an existing
library, use [the legacy template XML](../templates/bookshelfng.xml); it installs
`ghcr.io/snapetech-org/bookshelfng:latest`. Stable releases keep `:main`,
`:master`, and `:latest` on the same image; branch builds use development tags.

- Map persistent appdata to `/config` and your media to `/data`.
- Map downloads to `/download`, matching your download client's container paths.
- Set a personal Hardcover API token in `HARDCOVER_AUTH` or BookshelfNG settings.
- Open the web interface on port 8787 and configure indexers and download clients.
- One instance can manage ebooks and audiobooks. SeerrNG can use two service
  entries with the same URL and API key when requesting both formats.
- Existing Readarr or softcover databases require migration before using the
  Hardcover image; changing the image tag alone is not a migration.

## Source and support

- [BookshelfNG application source and documentation](https://github.com/snapetech-org/bookshelfng)
- [Unraid package and SeerrNG integration support](https://github.com/snapetech-org/seerrng/issues)

BookshelfNG is derived from Bookshelf and Readarr and distributed under GPLv3.
