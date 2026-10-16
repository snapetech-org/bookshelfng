# Install BookshelfNG on Unraid

**Final BookshelfNG release:** `0.4.21.70`. The ChaptarrNG `v0.9.972`
converter supports the migration-158 SQLite schema, but this template remains
on the BookshelfNG image and does not migrate an installation. Back up appdata
and follow the [migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
before preparing a manual handoff; the bridge stays disabled by default.

BookshelfNG is a Snapetech NG fork of Bookshelf for ebook and audiobook library
management and acquisition. It works independently; SeerrNG integration is optional.

## Installation and setup

In Unraid, open **Apps**, search for **BookshelfNG**, and select **Install** on
[the BookshelfNG listing](https://ca.unraid.net/apps/bookshelfng-1fdcqrv18pja7r).
For a manual install, use [the template XML](../templates/bookshelfng.xml) with Unraid's Docker
template workflow. The image is `ghcr.io/snapetech/bookshelfng:latest`; this
moving tag tracks the Hardcover image used by the Community Apps template.

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
