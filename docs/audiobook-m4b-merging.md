# Multi-file audiobook merging

BookshelfNG can combine a completed, identified audiobook download into one
chaptered M4B file. The feature is opt-in and disabled by default.

Set `BOOKSHELF_M4B_MERGE=true` in the BookshelfNG container environment. The
standard Docker image includes FFmpeg. For native installs, make `ffmpeg`
available on `PATH`, or set `BOOKSHELF_FFMPEG_PATH` to the executable path.

BookshelfNG merges two or more approved audio files that match the same book
and edition during completed-download processing. Manual imports and library
scans do not run this step, and existing M4B files are left alone. It orders
tracks by disc and track tags when present, then by numbered file name, and
uses each track title or filename as the chapter title. The output is stereo
AAC at 44.1 kHz and 128 kbps by default; set
`BOOKSHELF_M4B_AAC_BITRATE_KBPS` to a value from 48 to 320 to change the
bitrate.

If FFmpeg is unavailable, track durations cannot be read, conversion fails, or
the merged output is rejected by the import decision maker, BookshelfNG
removes the temporary output and imports the original files. Original tracks
are removed only after the M4B imports successfully in move mode. Copy mode
and downloads whose client does not allow moving files keep the source tracks.
The merge re-encodes audio, so it uses CPU and output quality depends on the
configured AAC bitrate.

The merge runs during completed-download processing. Existing library scans
and manual imports are unchanged. Existing standalone M4B downloads are also
left alone.

## Moving this setting to ChaptarrNG

The published ChaptarrNG `v0.9.977` does not honor
`BOOKSHELF_M4B_MERGE`, `BOOKSHELF_M4B_AAC_BITRATE_KBPS`, or
`BOOKSHELF_FFMPEG_PATH`. ChaptarrNG has native multipart and M4B conversion,
but that does not make these BookshelfNG settings equivalent. The source-only
[ChaptarrNG PR #129](https://github.com/snapetech-org/chaptarrng/pull/129) is
under review and is not available in a published build. The exact source-code
run on `05d78be4` failed the same four importer fixtures on Linux, macOS, and
Windows. Linux diagnostics on `e46b8974` traced them to a missing
`IBookService.GetBook` handler in the test proxy. Head `f47a7d6c` supplies the
existing book-service stub; hosted validation is running. Representative-media
acceptance remains open.
Preserve the settings in your deployment notes, but keep
`BOOKSHELF_M4B_MERGE` unset after migration until the ChaptarrNG migration
guide names a tested build that supports it.

BookshelfNG's updater does not update the application's image or package to
ChaptarrNG. Use the [migration guide](migrate-from-bookshelfng-to-chaptarrng.md)
for the current database and installation steps.

## Implementation references

- [M4B merge, conversion, validation, and cleanup](../src/NzbDrone.Core/MediaFiles/AudiobookM4bMergeService.cs)
- [Completed-download import integration](../src/NzbDrone.Core/MediaFiles/DownloadedBooksImportService.cs)
- [FFmpeg package in the container image](../docker/Dockerfile)
