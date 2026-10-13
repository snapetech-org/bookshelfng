# BookshelfNG legacy template for Unraid

This legacy listing is being retired in favor of ChaptarrNG. The updated
template switches the image to ChaptarrNG's standard build while preserving
the BookshelfNG appdata, media/download mount targets, and default web port.
Back up appdata before applying the update. New installations should use the
[ChaptarrNG Unraid listing](https://github.com/snapetech/chaptarrng-unraid).

## Existing installations

Open **Apps > Previous Apps** and apply the updated BookshelfNG template using
the standard ChaptarrNG image. Read the [migration
guide](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
before upgrading. For a manual install, use [the template XML](templates/bookshelfng.xml).

- Keep the existing `/config`, `/data`, and `/download` mappings, PUID/PGID,
  timezone, Hardcover variables, and port 8787.
- The first ChaptarrNG startup converts only the supported BookshelfNG
  migration-158 SQLite schema and retains a source backup in `/config`.
- Unsupported databases fail closed. Restore the independent appdata backup and
  previous image if startup does not complete.
- A template update does not change containers pinned to another image/tag or
  installed outside this Community Applications listing.

## Source and support

- [ChaptarrNG migration guide](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
- [ChaptarrNG application source](https://github.com/snapetech/chaptarrng)
- [Unraid package support](https://github.com/snapetech/seerrng/issues)

This template repository is distributed under GPLv3.
