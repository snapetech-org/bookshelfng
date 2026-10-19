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
`BOOKSHELF_FFMPEG_PATH`. ChaptarrNG PR #129 merged to `main` as `949ae3dd`
with this opt-in compatibility path. Its clean head passed the hosted Linux,
macOS, and Windows suites, PostgreSQL migration validation, CodeQL,
dependency/security, and release-note checks. A synthetic two-track smoke in
the `.977` image produced AAC at 44.1 kHz stereo and preserved the supplied
chapter titles and offsets; it checks the external tool and sidecar format.
ChaptarrNG draft PR #131 at commit `bdd7518f` adds a six-case tool-enabled
synthetic importer smoke. It passed locally in an isolated Linux container
with `m4b-tool` 0.5.2, `mp4v2` 2.1.1, and FFmpeg/FFprobe 6.1.1. Successful
cases check track ordering, chapters, metadata, registration, and Move/Copy
source handling. Failure cases
verify fallback to separate original-track imports in both modes when FFprobe
cannot read a source and when `m4b-tool` fails after a controlled FFmpeg
conversion error. Synthetic embedded-chapter Move/Copy and TagLib-write cases pass on c4fa. Representative M4B files and restart/resume remain open. Preserve these
settings in deployment notes, but keep `BOOKSHELF_M4B_MERGE` unset after
migration until a release with this support is available and the remaining
acceptance gates close.

BookshelfNG's updater does not update the application's image or package to
ChaptarrNG. Use the [migration guide](migrate-from-bookshelfng-to-chaptarrng.md)
for the current database and installation steps.

## Implementation references

- [M4B merge, conversion, validation, and cleanup](../src/NzbDrone.Core/MediaFiles/AudiobookM4bMergeService.cs)
- [Completed-download import integration](../src/NzbDrone.Core/MediaFiles/DownloadedBooksImportService.cs)
- [FFmpeg package in the container image](../docker/Dockerfile)
