# BookshelfNG for Unraid

This repository publishes the standalone BookshelfNG Unraid Docker template.
**Built on .NET 10 LTS**, BookshelfNG is a Snapetech NG fork of Bookshelf for
ebook and audiobook library management and acquisition. It works independently;
SeerrNG integration is optional.

> **Final release:** BookshelfNG `0.4.21.71` is the final source release. The
> legacy Unraid template has not yet switched to ChaptarrNG. ChaptarrNG `.977`
> accepts migration-158 SQLite; its current guard rejects versions before 14.
> Upgrade BookshelfNG to `.71` before migration, or wait for the version-aware
> ChaptarrNG fix now under hosted validation. An isolated Docker image-switch
> smoke passed with an empty database and rollback; the Community Apps template
> update flow and populated operator data remain untested.

## Installation and setup

In Unraid, open **Apps**, search for **BookshelfNG**, and select **Install** on
[the BookshelfNG listing](https://ca.unraid.net/apps/bookshelfng-1fdcqrv18pja7r).
For a manual install, use [the template XML](templates/bookshelfng.xml) with Unraid's Docker
template workflow. The image is `ghcr.io/snapetech-org/bookshelfng:main`; this moving tag tracks the
Hardcover image used by the Community Apps template.

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
