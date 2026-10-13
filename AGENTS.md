# Agent instructions - BookshelfNG

## Communication and authority

These interaction rules apply to every model interface using this repository:

- Answer directly and accurately. Correct false premises when evidence supports it.
- Assess estimates independently and use explicit confidence levels: high, moderate, low, or unknown.
- Do not invent evidence. State when a result is unknown.
- Distinguish source changes, automated checks, visual inspection, and live service verification.
- Preserve upstream attribution and follow the repository's documented license and contribution terms.
- Do not publish, merge, deploy, or release without maintainer authorization. Authorization for one named action does not authorize unrelated actions.

## Required project reading

- Start with README.md and docs/README.md for product scope and the current documentation map.
- Read docs/capabilities-and-compatibility.md before changing provider identity, Readarr compatibility, format handling, migration, or fork-specific behavior.
- Read docs/development/validation-engine.md before selecting or reporting tests.
- Read release-notes/README.md before preparing a pull request for changes to user-facing behavior, security, operations, or user-facing documentation.
- Read the relevant operator guide when changing a documented workflow, such as docs/media-storage.md for media moves or docs/import-matching-and-formats.md for matching behavior.

## BookshelfNG behavior and data boundaries

- BookshelfNG is a standalone ebook and audiobook manager. SeerrNG integration is optional; do not make the core application depend on SeerrNG.
- Preserve the Readarr-compatible API and existing client behavior. Keep BookshelfNG branding separate from compatibility identifiers that existing clients depend on.
- One database can manage ebooks and audiobooks together. Keep compatible ebook formats and audiobook files on the same book record, and do not let an ebook replace an audiobook or one incompatible ebook format replace another.
- Metadata provider IDs belong to their provider. Do not treat Hardcover, Goodreads-compatible, Google Books, Open Library, or other catalog IDs as interchangeable. Do not silently switch the primary provider after authentication, rate-limit, malformed-response, or network errors.
- Existing library state lives under the configured data volume, normally /config. Tests and local validation must use disposable databases and media fixtures, never an operator's library or download folders.
- Media moves must stay scoped to registered media and supported sidecars. Preserve the preview, conflict, space, and confirmation checks. Do not sweep unknown files or merge another instance's database. Keep a recoverable source backup until a migration has been verified.
- Preserve the administrator-key boundary for media move operations and the opt-in boundary for optional diagnostics. The standard image must not acquire telemetry or reporting behavior by accident.

## Validation and evidence

- The backend targets .NET 10.0.401. Use the repository's declared Node versions: local Volta 20.11.1 is accepted, and CI uses Node 20.19.4.
- The build script clears _tests and _output. Use a disposable worktree when those directories contain artifacts that must be preserved.
- Build the test package before using the validation engine. Follow docs/development/validation-engine.md for the exact build, plan, and test commands.
- A validation plan is discovery evidence only. Report which tasks ran and the native NUnit totals, including skipped and inconclusive cases. A missing or zero-case NUnit report is not a pass.
- Keep live provider calls, real credentials, and operator data out of tests. A local test pass does not prove live metadata or download-client integration.
- For visible UI changes, report visual inspection separately from automated checks. A build or source assertion does not prove the rendered UI works.

## Release notes

Changes to user-facing behavior, security, operations, or user-facing documentation need a new fragment under release-notes/. Keep shipped fragments append-only and follow release-notes/README.md. Preview with yarn release-notes:preview --base origin/main --head HEAD. For an internal-only pull request, include the exact marker release-note: none in the description.
