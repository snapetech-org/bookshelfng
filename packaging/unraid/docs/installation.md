# Install BookshelfNG on Unraid

BookshelfNG is a Snapetech NG fork of Bookshelf for ebook and audiobook library
management and acquisition. It works independently; SeerrNG integration is optional.

> **Published state:** BookshelfNG `0.4.21.71` and ChaptarrNG `v0.9.977` remain the latest releases. The published converter is preview-only for migration-158 SQLite. While [BookshelfNG issue #144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open, do not apply migration or start ChaptarrNG against BookshelfNG appdata.
>
> ChaptarrNG PR #131 remains draft at docs-only head `93213b67`, on top of application-code commit `0e881d92`. The application-code Build [39313568727](https://github.com/snapetech-org/chaptarrng/actions/runs/39313568727) passed Linux, macOS, and Windows, PostgreSQL migration, release-note, receipt, and Linux pinned-tool M4B checks; CodeQL, analysis, dependency/security, dependency-review, NuGet, and Helm identity checks also passed. Exact-head Build [39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744) for the docs follow-up passed on Linux, macOS, and Windows, including PostgreSQL migration and native-runner receipt reconciliation. Current details are in the [ChaptarrNG migration status](https://github.com/snapetech-org/chaptarrng/blob/codex/bookshelf-retirement-next-20261018/README.md#bookshelfng-migration-status). The Linux artifact from Build 39316535744 passed the populated synthetic migration-to-SeerrNG Compose smoke, including restricted-key checks and pending import add, poll, and cancel; see the migration guide for details. These checks do not establish operator-data, installed-rollback, or update-channel acceptance; the feature and release gates remain open. BKSENC01 backup support is not in public `.977`.
>
> The Unraid transition [PR #5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) remains a draft at branch head `69f53b434f7be565e5ca3bb8b734942758460451`. Its refreshed README and installation page point at ChaptarrNG PR #131 head `93213b67`; the exact-head template-preservation check passed in run [39317048739](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39317048739). The real Community Applications upgrade and rollback flow has not been accepted. Both release-readiness gates remain unset; no migration bridge is published.

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
