# BookshelfNG Unraid retirement template

This legacy listing moves existing installations to ChaptarrNG. The updated
template preserves the BookshelfNG data and media mappings while changing the
image to the ChaptarrNG standard build. Back up appdata first. New
installations should use the [ChaptarrNG Unraid
listing](https://github.com/snapetech/chaptarrng-unraid).

## Existing installations

Open **Apps > Previous Apps** and apply the updated BookshelfNG template using
the standard ChaptarrNG image. Read the [migration guide](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
before upgrading. For a manual install, use [the template XML](../templates/bookshelfng.xml).

- Keep the existing `/config`, `/data`, `/download`, PUID/PGID, timezone,
  Hardcover variables, and port 8787 mappings.
- The first ChaptarrNG startup converts only the supported BookshelfNG
  migration-158 SQLite schema and retains a source backup in `/config`.
- Unsupported databases fail closed. Restore the independent appdata backup and
  previous image if startup does not complete.
- A template update does not affect containers pinned to other images or
  installed outside this Community Applications listing.

## Source and support

- [ChaptarrNG migration guide](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
- [ChaptarrNG application source](https://github.com/snapetech/chaptarrng)
- [Unraid package support](https://github.com/snapetech/seerrng/issues)
