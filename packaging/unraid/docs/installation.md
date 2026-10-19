# Install BookshelfNG on Unraid

BookshelfNG is a Snapetech NG fork of Bookshelf for ebook and audiobook library
management and acquisition. It works independently; SeerrNG integration is optional.

> **Published state:** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977` remain the latest releases. The published converter is preview-only for migration-158 SQLite. While [BookshelfNG issue #144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open, do not apply migration or start ChaptarrNG against BookshelfNG appdata.
>
> ChaptarrNG PR #131 remains draft. Candidate commit `12f290bd` built through its checked-in `Dockerfile.build` and passed a populated synthetic migration-158 smoke: normal startup converted the database, and SeerrNG read both migrated formats. The importer suite passed 43/43. A separate six-case real-tool importer check passed synthetic M4B merge and fallback cases on candidate `12f290bd`; Linux CI now runs it in a pinned tool image. The later candidate `38be9422` adds BKSENC01 portable `.enc` import/export, cross-checked against BookshelfNG's source encryption implementation. Exact-head Build [39267876585](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876585) is queued; the support is not in public `.977`. Representative audiobooks, operator-data acceptance, installed rollback, and channel handoff remain open; parity and release gates remain open. See the [source-build run record](https://github.com/snapetech-org/chaptarrng/blob/codex/bookshelf-retirement-next-20261018/integration/README.md#populated-migration-source-build-run-2026-10-19).
>
> The Unraid transition [PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) also remains a draft. Its template-preservation check passes, but the real Community Applications upgrade and rollback flow has not been accepted. Both release-readiness gates remain unset; no migration bridge is published.

## Existing installations

Keep the current BookshelfNG image. The cutover is frozen: read-only preview is
allowed, but do not apply migration or switch an existing appdata directory to
ChaptarrNG while BookshelfNG issue #144 remains open. The legacy Community Apps
template on `main` still points to BookshelfNG. A transition
candidate preserves its appdata path, port, media/download mappings, user IDs,
timezone, and Hardcover settings while switching to the standard ChaptarrNG
image. It is not published and must remain on its feature branch until the
application release and Unraid update-flow gates pass. The XML and
settings-preservation check passed; run
`python3 scripts/test-transition-template.py` to repeat it.
Read the
[BookshelfNG-to-ChaptarrNG migration guide](https://github.com/snapetech-org/bookshelfng/blob/main/docs/migrate-from-bookshelfng-to-chaptarrng.md).
When cutover is approved, upgrade BookshelfNG to `.71`, stop the service, and
keep an independent appdata backup before switching. New installations should use the
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
