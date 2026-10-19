# BookshelfNG for Unraid

This repository publishes the standalone BookshelfNG Unraid Docker template.
**Built on .NET 10 LTS**, BookshelfNG is a Snapetech NG fork of Bookshelf for
ebook and audiobook library management and acquisition. It works independently;
SeerrNG integration is optional.

> **Published state:** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977` remain the latest releases. The published converter is preview-only for migration-158 SQLite. While [BookshelfNG issue #144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open, do not apply migration or start ChaptarrNG against BookshelfNG appdata.
>
> ChaptarrNG PR #131 is at documentation-only head `8912b7b3629248348c51daa0f1c39a6357e20ed7`. Exact-head Build [39334414682](https://github.com/snapetech-org/chaptarrng/actions/runs/39334414682) passed Linux, macOS, and Windows, PostgreSQL migration, release-note contract, and the Windows migration-installer build, SQLite fingerprint smoke, and service data-directory smoke. CodeQL [39334411350](https://github.com/snapetech-org/chaptarrng/actions/runs/39334411350), security [39334414694](https://github.com/snapetech-org/chaptarrng/actions/runs/39334414694), dependency review [39334414922](https://github.com/snapetech-org/chaptarrng/actions/runs/39334414922), Helm identity [39334414735](https://github.com/snapetech-org/chaptarrng/actions/runs/39334414735), and NuGet [39334412894](https://github.com/snapetech-org/chaptarrng/actions/runs/39334412894) passed. Disposable-fork validation remains skipped by its external-fork gate. This is not an installed BookshelfNG service migration or rollback test. Operator-data, installed-rollback, update-channel, and Unraid Community Applications acceptance remain open; no bridge is published. BKSENC01 backup support is not in public .977.
>
> The Unraid transition [PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) remains draft at branch head `69f53b434f7be565e5ca3bb8b734942758460451`. Its template-preservation check passed in run [39317048739](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39317048739) against the earlier ChaptarrNG PR #131 head `93213b67`; it has not been rerun against current candidate `8912b7b3629248348c51daa0f1c39a6357e20ed7`. The real Community Applications upgrade and rollback flow has not been accepted. Both release-readiness gates remain unset; no migration bridge is published.

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
This template repository uses the same GPLv3 license.
