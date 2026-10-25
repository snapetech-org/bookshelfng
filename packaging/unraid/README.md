# BookshelfNG for Unraid

This repository publishes the standalone BookshelfNG Unraid Docker template.
**Built on .NET 10 LTS**, BookshelfNG is a Snapetech NG fork of Bookshelf for
ebook and audiobook library management and acquisition. It works independently;
SeerrNG integration is optional.

> **Published state (2026-10-21):** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977` remain the latest releases. ChaptarrNG PR [#131](https://github.com/snapetech-org/chaptarrng/pull/131) is merged to `main`, but its migration and compatibility work is unpublished and not approved for cutover. BookshelfNG issue [#144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open; keep BookshelfNG running and do not apply migration or start ChaptarrNG against its appdata.
>
> The legacy handoff remains a draft in [Unraid PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) at candidate `1261a9f8`. Its exact-head build, template, package-sync, dependency, release-note, Semgrep, and Trivy checks passed. Publication jobs were skipped. Actual Community Applications update/rollback and representative-data migration/rollback remain open, so the `main` template continues to point at BookshelfNG. Keep the release-readiness gates unset.
>
> Current ChaptarrNG source candidate is [`102d9cbe`](https://github.com/snapetech-org/chaptarrng/commit/102d9cbe09c47ca683b1daeb339252b58a2037f3), with restored Direct Download catalog search for KEPUB, MOBI, and AZW3, KEPUB detail-link resolution, and Books/Ebook release classification. Exact-head Build [39524671037](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671037) is running; Security Analysis [39524671043](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671043), Semgrep CE [39524671084](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671084), Trivy [39524671053](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671053), and NuGet submission [39524699566](https://github.com/snapetech-org/chaptarrng/actions/runs/39524699566) passed. The release-note contract was skipped on the main push; no CodeQL run is attached. No release or package was prepared, and public `.977` is unchanged.
>
> A local source-build smoke on ChaptarrNG `ef0a144d` and SeerrNG `ce632a6e` passed with a synthetic populated migration-158 fixture: ChaptarrNG reached schema 121, retained a source backup, and both SQLite databases passed integrity and foreign-key checks. SeerrNG's real ReadarrAPI read the audiobook and ebook and created, polled, and cancelled a synthetic pending import using the restricted key. Placeholder `.m4b`/`.epub` files mean this does not validate real media, provider fulfillment, operator data, PostgreSQL operator data, or installed rollback. See the [migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md). The release freeze and cutover decision remain unchanged.

## Existing installations

Keep the current BookshelfNG image. The cutover is frozen: read-only preview is
allowed, but do not apply migration or switch an existing appdata directory to
ChaptarrNG while BookshelfNG issue #144 remains open. The legacy Community Apps
template on `main` still points to BookshelfNG. A transition
candidate keeps the existing BookshelfNG entry, appdata path, port, media and
download mappings, user IDs, timezone, and Hardcover settings while switching
to the standard ChaptarrNG image. It is not published and must remain on its
feature branch until the application release and Unraid update-flow gates
pass. The XML and settings-preservation check passed; run
`python3 scripts/test-transition-template.py` to repeat it. Read the
[BookshelfNG-to-ChaptarrNG migration guide](https://github.com/snapetech-org/bookshelfng/blob/main/docs/migrate-from-bookshelfng-to-chaptarrng.md).
When cutover is approved, upgrade BookshelfNG to `.71`, stop the service, and
keep an independent appdata backup before switching. New installations should use the
[ChaptarrNG Unraid template](https://github.com/snapetech-org/chaptarrng-unraid).
For a manual BookshelfNG install needed to inspect or roll back an existing
library, use [the legacy template XML](templates/bookshelfng.xml); it installs
`ghcr.io/snapetech-org/bookshelfng:latest`. Stable releases keep `:stable`,
`:main`, `:master`, and `:latest` on the same verified image digest; branch
builds use development tags.

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
This template repository uses the same GPLv3 license.
