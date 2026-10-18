# Setup experience contract during retirement

BookshelfNG `0.4.21.71` is the final published source release and publishing
remains gated. This repository should not gain a new first-run wizard or new
setup feature. The applicable user experience is the existing BookshelfNG to
ChaptarrNG migration path documented in
[the migration guide](../migrate-from-bookshelfng-to-chaptarrng.md) and
[the retirement report](./chaptarr-consolidation.md).

## Apply the contract to the handoff

**Current decision: read-only preview only.** Until data, parity, rollback,
and installation-channel acceptance close, do not apply conversion, start
ChaptarrNG against BookshelfNG appdata, or discard the source backup. Normal
ChaptarrNG startup can convert a supported source database automatically.

Keep the existing helper and migration workflow as the entry point. It should
make the source version, supported migration path, backup location, preview
result, and rollback option clear before applying changes. Preserve the
current fail-closed behavior for unsupported schemas, ambiguous source
databases, and unpublished candidate builds.

Use the migration preview to show what is recognized and what needs an
operator decision. Do not guess formats for ambiguous books, merge independent
libraries, copy media files, or rewrite external provider settings. Require
explicit review before applying the conversion after the acceptance gates
close, then report verification results and the location of retained
source/converted backups.

## Contract

- Keep current BookshelfNG settings and migration behavior as the source of
  truth; do not add a parallel onboarding path.
- State which behavior belongs to the final `.71` release and which is only
  present in an unpublished candidate.
- Ask for confirmation only when an operation changes user data or starts a
  migration; make preview and inspection read-only.
- Explain unsupported paths before a user stops the old service or changes
  installation channels.
- Keep ChaptarrNG's own setup experience and integration tests responsible for
  the destination application.

For new installs and ongoing setup, direct users to the supported ChaptarrNG
release status and its Quickstart. BookshelfNG's remaining setup guidance is
for safe migration and retirement only.

ChaptarrNG PR #132 merged format-specific root setup to source `main` as
`0f1fea44`; the exact-main Build run [39159951469](https://github.com/snapetech-org/chaptarrng/actions/runs/39159951469)
passed Linux, macOS, Windows, PostgreSQL migration, and native-runner receipt
checks. This Quickstart change is not in published `.977` while the release
gate remains closed.

## Remaining tasks

BookshelfNG is release-frozen, so these are migration-path and documentation
tasks. They do not authorize new setup UI or another migration tool.

- [x] **B1 — P1: Keep the migration guide's go/no-go decision current.**
  Maintain the opening status in
  `docs/migrate-from-bookshelfng-to-chaptarrng.md` alongside
  `docs/maintainers/chaptarr-consolidation.md`. State the exact public
  BookshelfNG source version, public ChaptarrNG converter version, supported
  database/schema, release-gate state, and whether the next action is “stop”
  or “preview.” Keep candidate-only support clearly marked as unavailable.
  **Done when:** an operator can decide from the first screenful whether their
  installed versions are eligible, without reading the historical investigation.

- [ ] **B2 — P1, blocked on release acceptance: Revalidate the published
  migration journey when the gates change.** Use the existing helper's
  preview, media-review, apply, verification, and rollback sequence; update
  the public guide only from a supported release and accepted operator-data
  evidence.
  **Done when:** every documented command targets a released build, ambiguous
  ebook/audiobook classifications still stop for explicit review, and the
  guide reports the verified backup and rollback behavior for that release.

- [ ] **B3 — P2: Hand users off to the ChaptarrNG path at the right point.**
  Once a supported migration build is available, keep the final migration
  checkpoint in the guide linked to ChaptarrNG's Quickstart for indexers,
  download clients, and format-specific roots.
  **Done when:** BookshelfNG stops prescribing ongoing setup after migration
  and the link names the destination release and the first post-migration task.
