# BookshelfNG for Unraid

This repository publishes the standalone BookshelfNG Unraid Docker template.
**Built on .NET 10 LTS**, BookshelfNG is a Snapetech NG fork of Bookshelf for
ebook and audiobook library management and acquisition. It works independently;
SeerrNG integration is optional.

> **Published state:** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977` remain the latest releases. The published converter is preview-only for migration-158 SQLite. While [BookshelfNG issue #144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open, do not apply migration or start ChaptarrNG against BookshelfNG appdata.
>
> ChaptarrNG PR #131 is at code head `ebe838dd7a74780692350c9d02826f219919582b`. Its Windows smoke uses the actual installer against a disposable BookshelfNG `.71` service with a populated migration-158 fixture. It injects a local `/ping` conflict to test automatic rollback, retries migration, then tests explicit restore. The Windows-targeted harness compiles locally and the fixture passes SQLite integrity and foreign-key checks. Exact-head Build [39339777476](https://github.com/snapetech-org/chaptarrng/actions/runs/39339777476) is still running, including the Windows service smoke and PostgreSQL migration. Release-note contract, Security analysis [39339777368](https://github.com/snapetech-org/chaptarrng/actions/runs/39339777368), Dependency review [39339777472](https://github.com/snapetech-org/chaptarrng/actions/runs/39339777472), Helm identity [39339777453](https://github.com/snapetech-org/chaptarrng/actions/runs/39339777453), and NuGet submission [39339771379](https://github.com/snapetech-org/chaptarrng/actions/runs/39339771379) passed. PR #131 remains draft and its installer is unpublished. Operator-data, feature-parity, update-channel, and Unraid Community Applications acceptance remain open. No bridge is published. BKSENC01 backup support is not in public `.977`.
>
> The Unraid transition [PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) remains draft. Its hosted template-preservation check passed in [run 39340267938](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39340267938). That check validates the candidate XML and settings preservation; it does not exercise a live Community Applications update or rollback. Both release-readiness gates remain unset; no migration bridge is published.


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
