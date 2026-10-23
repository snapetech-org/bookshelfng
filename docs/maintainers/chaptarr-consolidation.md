# BookshelfNG retirement and ChaptarrNG consolidation

## Current status — 2026-10-23

BookshelfNG 0.4.21.71 and ChaptarrNG v0.9.977 remain the latest public app releases. The owner authorized one final BookshelfNG security-maintenance release, 0.4.21.72; its tag and publication remain pending exact-head CI. ChaptarrNG [main](https://github.com/snapetech-org/chaptarrng/tree/main) is the migration target, and the release freeze resumes after that one-time update.

ChaptarrNG main contains a candidate-only Debian bridge builder under the BookshelfNG package identity. A local candidate was built from the checksum-verified public ChaptarrNG v0.9.977 Linux x64 archive; the checksum-verified BookshelfNG 0.4.21.71-1 package confirmed the old package identity and conffile. An isolated dpkg transaction upgraded that actual package and downgraded back with edited config and data canaries; dependency checks were bypassed and systemd was mocked. Separately, a Debian Trixie apt transaction using those actual packages resolved dependencies (including libicu76 and ca-certificates), installed the CA bundle, upgraded and downgraded, and preserved the edited config/data canaries without a conffile prompt. In a systemd-running Trixie container, the actual `.71` service upgraded to the `.977` candidate, restarted, and passed `/ping`; after restoring the pre-upgrade data copy, downgrade to `.71` also restarted and passed `/ping`. This used a fresh empty `.71` database, not operator data. PPA publication, real-host acceptance, and representative-data rollback remain open. No compatibility package was published.
Rebuilt local `.978` BookshelfNG-identity AppImage and Flatpak candidates passed same-identity update and rollback rehearsals from checksum-verified public `.71` packages. Migration preview left each source unchanged; startup reached schema 121 with four authors and nine books, preserved split ebook/audiobook paths under the shared author root, and passed SQLite integrity and foreign-key checks. Restore recovered the exact schema-158 source DB, and each public `.71` package started on the restored data with `/ping` HTTP 200. BookshelfNG commit `55850043` added JSON-only request guards to six state-changing API actions; ChaptarrNG commit `12993c12` ports all six and adds a regression fixture. The exact-head Core suite passed 4,648 tests with 0 failures and 25 skips. These synthetic checks and the route-level port do not establish representative-data or published-channel acceptance; artifacts remain unsigned and unpublished. See the [ChaptarrNG candidate evidence](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md#legacy-install-channels).

The current schema-v4 inventory pins BookshelfNG source 685b31c93d7146258c02446b01cb34c6f5d962b5 to ChaptarrNG target 4b57b479d73c844db19278233e25efe94509e99b: 875 reachable post-fork commits (866 absent from the pinned upstream history) and 1,151 changed paths. It records 90 reviewed mappings and 757 dispositions (175 retained, 143 equivalent, 263 ported, 176 repository-only retirements), leaving 394 open paths (261 requiring semantic review, 129 without mapped targets, two source-deleted paths, and two identical paths); 13 unique-basename candidates remain review hints. The 92 path decisions and 756 prior feature dispositions carry forward where their pinned source and mapped target blobs are unchanged. The scoped ported records include embedded audiobook disc/track ordering and RSS fuzzy-title fallback; the comparer and pending-queue ports remain separate. The fuzzy fallback disposition is limited to the RSS path and its focused regression fixture; no BookshelfNG mapping is inferred from the release-push provenance fix. ChaptarrNG commit 3fe0a8f1 restores migrated-audiobook release-candidate priority; 813b7ff1 restores migrated pending-audiobook queue order; cd1b3fe9 orders inferred audiobook parts by complete embedded disc/track tags; and 4b57b479 preserves release-push provenance through decision evaluation. This remains path-level review, not runtime or migration acceptance. The Release Core suite passed 4,709 tests, skipped 25, and failed 0; commit-hook Semgrep found zero findings and push-readiness checks passed. On upstream PR [#114](https://github.com/Chaptarr/chaptarr/pull/114), exact-head Semgrep [39972277607](https://github.com/Chaptarr/chaptarr/actions/runs/39972277607) and Trivy [39972277647](https://github.com/Chaptarr/chaptarr/actions/runs/39972277647) are action_required with no jobs started; approving those workflow runs requires repository-admin rights, which this agent account lacks, so hosted validation remains open. A populated SQLite conversion and database rollback rehearsal passes on a disposable snapshot; live media/provider behavior, installed-channel handoff, production rollback, and cutover acceptance remain open. Launchpad PPA configuration preflight is ported, but no PPA publisher bridge is configured and channel acceptance remains open; the Bookshelf-owned bridge workflow test remains open for semantic review. Candidate package and installer paths remain evidence only; publication and installed-channel acceptance are open. No runtime feature retirement is approved. Raw unique-basename matches are review hints, never automatic mappings. Path review remains separate from behavior, data, and operator acceptance.
On ChaptarrNG commit `813b7ff1`, eight focused M4B importer cases passed locally with the existing `chaptarrng-seerrng-smoke:local` image and its pinned m4b-tool 0.5.2. They cover merge and chapter behavior, Move/Copy source handling, and failure fallback; the input media are synthetic, so representative files and restart/resume acceptance remain open.

The exact-head SeerrNG Compose smoke also passed on 2026-10-23: ChaptarrNG `813b7ff13bdfe051843f2648fa32c2ace93cb2d6` was built through `Dockerfile.build` and tested against SeerrNG `16258e03365686bd8ca4ea6d17623252277d6f05`. Normal startup converted the disposable populated migration-158 fixture; SeerrNG's compiled `ReadarrAPI` read one audiobook and one ebook with the restricted service key, which was denied administrative and unrelated-command access. The pending-import create, poll, cancel, and terminal-state checks passed. Records, placeholder media, and API keys were synthetic. The run's containers, network, and named volumes were removed; its local image cache was retained. This does not establish live provider fulfillment, retries, availability/history parity, operator-data migration, full SeerrNG workflow acceptance, or rollback.

A populated SQLite source snapshot now passed preview, conversion, integrity and foreign-key checks, row/path accounting, and database rollback on a disposable copy. Remaining semantic parity, live media/provider behavior, installed Windows/Unraid and package-channel handoff, PostgreSQL operator data, SeerrNG workflows, production rollback, and operator acceptance remain open. Keep BookshelfNG in service and do not publish or cut over.

## Current audit inventory and regeneration — 2026-10-23

This inventory and documentation refresh is maintainer-only. It changes no
BookshelfNG runtime, package, or release content.

The details below preserve integration and migration-test snapshots. The current app-code and package validation, exact target pin, and audit counts are stated above; earlier-head results are historical.

At that checkpoint, the BookshelfNG source commit was `6e1a62e12` with an Editions and Narrations
book-details tab backed by `GET /api/v1/book/{id}/editions/catalog` and the
`editionCatalog` capability. ChaptarrNG `main` now includes that tab, the
series narrator comparison, and wanted-edition variants. Candidate code
snapshot `8b4c6e23` integrated then-current `main` with the migration work and
retains facade-specific provider IDs, proxied covers, and file-backed
ownership. Local translation, type, targeted ESLint/Stylelint, and
release-note preview checks pass. Its release-note contract, dependency review,
security scan, and NuGet checks pass. CodeQL
[39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712)
passes; cross-platform Build
[39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks.
Public ChaptarrNG `.977` predates the catalog UI.

The published `.977` converter maps bare numeric provider IDs to Goodreads,
including for native Hardcover BookshelfNG data. Its earlier populated
round-trip preview and integrity checks did not test provider identity; do not
apply `.977` to a native Hardcover database. The merged, unreleased source requires
explicit provider mode and, with `HARDCOVER=true`, passed a populated
migration-158 SQLite preview, apply, restore preview, and rollback on a
task-scoped copy. The live BookshelfNG service remained running; these
candidate commands did not block network access. The source snapshot remained
unchanged. Apply passed integrity and foreign-key checks; rollback restored a
byte-identical retained source backup and preserved the converted database
separately. Native Hardcover identities were retained for migrated authors,
books, and editions.

That data exercise exposed positive file references to missing editions and
history rows whose source book disagreed with the referenced file. The current
importer preserves such files as unmapped and retains conflicting history on
its source book without unsafe file or edition links. Focused importer,
edition-catalog, series-catalog, and capability tests pass 52/52 locally. This is one populated SQLite
candidate rehearsal; ambiguous-media review, older real schemas, PostgreSQL
operator data, full feature parity, installed rollback, and channel acceptance
remain open. All release and bridge gates remain closed.

The ChaptarrNG retirement candidate at that checkpoint added older SQLite migration coverage, one-schema migration-158 PostgreSQL support, native Hardcover identity handling, a separate BookOrbit Book Dock integration, SeerrNG edition-catalog compatibility, and previewable media moves. PR #131 was still draft at that historical checkpoint. Code head `2c0401fc` passed exact-head hosted run [39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646), including Linux, macOS, and Windows suites, all four PostgreSQL fixtures, release-note and runner-receipt validation, CodeQL, dependency review, secret scan, and NuGet submission. Docs-only checkpoint `898b72fd` passed exact-head hosted run [39198708193](https://github.com/snapetech-org/chaptarrng/actions/runs/39198708193). Docs-only checkpoint `ddec3e81` passed exact-head hosted run [39199730309](https://github.com/snapetech-org/chaptarrng/actions/runs/39199730309). Earlier docs-only head `353aeba1` passed exact-head run [39201211634](https://github.com/snapetech-org/chaptarrng/actions/runs/39201211634); CodeQL, dependency/security, dependency-review, and NuGet checks passed too. Disposable-fork validation was skipped by its gate. The local SeerrNG Compose smoke against `ddec3e81` and SeerrNG `10f06eab9` passed capability discovery, empty-library paging, and restricted-key checks; it does not establish populated-data or full workflow acceptance. Fifty-two focused importer, catalog, and capability tests pass locally. The populated SQLite copy-only round trip is documented in the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/8b4c6e23/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md); it does not establish operator-data acceptance. Provider, database, feature, installed rollback, and channel acceptance gates remain open. Earlier runs on `e4db2d46` and `f5f57644` are historical candidate checkpoints, not current-head validation. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131).

ChaptarrNG PR #132 also merged on 2026-10-18 as `0f1fea44`, adding
format-specific root setup to Quickstart. Current-main Build run
[39159951469](https://github.com/snapetech-org/chaptarrng/actions/runs/39159951469)
passed Linux, macOS, Windows, PostgreSQL migration, and native-runner receipt
reconciliation. The Quickstart improvement remains source-only; it is not in
published `.977` while the ChaptarrNG release gate is closed.

The migration bridge is disabled. ChaptarrNG AUR `0.9.977-1` is published;
BookshelfNG's public AUR identity remains at `0.4.21.71-1` on the BookshelfNG
payload. A local `bookshelfng-bin 0.9.977-1` candidate passed a network-disabled
pacman upgrade from `.71` and downgrade back to `.71`, preserving a modified
environment file and synthetic data canary. Its installed migration commands
also passed preview, conversion, and restore against a synthetic populated
migration-158 database, including SQLite integrity and foreign-key checks.
An active systemd rehearsal then upgraded `.71` to the local candidate, started
ChaptarrNG for automatic conversion, restored migration 158, downgraded to
`.71`, and started BookshelfNG again. SQLite integrity and foreign-key checks
passed throughout. The isolated container's network-online wait was masked;
representative operator data and host-specific service settings remain open.
COPR built `chaptarrng 0.9.977-1` successfully for Fedora 43, 44, 45,
and Rawhide x86_64; the legacy COPR trigger was skipped. ChaptarrNG Chocolatey
`.977` built and passed the hosted package-transition smoke, but its publish
returned HTTP 403 and the live feed has no `chaptarrng` entry. The BookshelfNG
Chocolatey identity remains public at `0.4.21.70`. GHCR published the standard
`.977` image but did not redirect legacy aliases. See the maintained
[retirement status page](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md)
and the user-facing
[migration guide](../migrate-from-bookshelfng-to-chaptarrng.md) for the current
channel checklist and operator procedure.

ChaptarrNG `v0.9.977` remains the latest public release; `.978` is a source
version bump. PR #128 merged release and distribution workflows that fail
closed unless `CHAPTARRNG_RELEASE_READY=true`, and the repository variable is
unset. Do not publish a release, package, image, or channel update while
retirement acceptance remains open. BookshelfNG PR #148 merged its fail-closed publisher gate to `main` as `c6b4642`; its tag-triggered image/release jobs, manual distribution retries, and legacy bridge require `BOOKSHELFNG_RELEASE_READY=true`, which remains unset. PR #127
merged to ChaptarrNG `main` as `b3089a39`. It adds selectable supplemental
catalogs, per-field preferences, and exact cross-catalog recovery for unmapped files through ISBN, ASIN,
provider IDs, and normalized title/author evidence. Linux, macOS, Windows,
PostgreSQL migration, CodeQL, dependency/security, and release-note checks
passed on its exact head. Four provider-dispatch CodeQL findings on an earlier
head were reviewed and dismissed as false positives because they route only to
allowlisted public APIs. The merged source is not in public `.977` and has not
closed settings or converted-operator-data acceptance.

ChaptarrNG PR #129 merged to `main` as `949ae3dd`. Its clean head
`a671f4b3` passed hosted Linux, macOS, Windows, PostgreSQL migration, CodeQL,
dependency/security, and release-note checks. It ports the opt-in M4B merge
settings, tagged track ordering and chapter titles, original-track fallback,
and source cleanup only after successful move-mode import; copy mode retains
the sources. A synthetic two-track smoke using the `.977` toolchain produced
AAC at 44.1 kHz stereo and preserved the supplied chapter titles and offsets.
That validates m4b-tool and its sidecar format. At the 2026-10-19 checkpoint,
then-draft ChaptarrNG PR #131 at commit `bdd7518f` added a six-case tool-enabled synthetic importer smoke that
passed locally in an isolated Linux container with `m4b-tool` 0.5.2,
`mp4v2` 2.1.1, and FFmpeg/FFprobe 6.1.1. Successful cases verify tag order,
chapter titles/offsets, output metadata, registration, Move-mode cleanup, and
Copy-mode source retention.
Failure cases verify fallback to separate original-track imports in both
modes when FFprobe cannot read a source and when `m4b-tool` fails after a
controlled FFmpeg conversion error. Focused tests also cover fallback with a
mocked converter. Synthetic embedded-chapter Move/Copy and TagLib-write cases pass on c4fa. Representative M4B files and restart/resume remain open. The source change is not in public `.977`; neither merge closes
real-data migration/rollback, settings parity, full feature parity, or
installer/channel acceptance.

ChaptarrNG PR #130 merged to `main` as `9f1ae60b`; hosted Linux, macOS,
Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note
checks passed. When no explicit `BookMatchingStrictness` is configured, the
converter maps legacy `BookImportMinimumMatchPercent` values 50–66 to
Aggressive, 67–82 to Balanced, and 83–99 to Strict; an explicit mode takes
precedence, invalid legacy values fail closed, and the original source row is
preserved. The report identifies this as a lossy approximation between
different algorithms. Converted-data acceptance remains open, and the change
is not in public `.977`.

Historical path-level inventory checkpoint (2026-10-19): BookshelfNG source
`c63eb84813392cdb398d9e6bf4446694952f256d` was compared with ChaptarrNG target
`29852b1334ee049e30de84b44806932a3e9364f4`. It covers 679 reachable post-fork
commits (670 absent from the pinned upstream history) and 1,116 changed paths:
239 paths without mapped targets, 408 undispositioned semantic differences, 176 retained identical paths, 129 equivalent paths (118 C# paths checked automatically, 8 with Roslyn, and 3 license/build/documentation files), six ported files (four project files, the release-note process guide, and the contributor guide), 158 approved non-runtime retirements (145 historical release-note fragments, 12 BookshelfNG logo assets, and one obsolete Readarr Azure Pipelines definition), and two paths absent from the Bookshelf snapshot. Schema v4 records 25
rechecked path correspondences, no unconfirmed basename hints, and 469 reviewed
source-path dispositions out of 1,116 (176 retained, 129 equivalent, 6 ported, and
158 non-runtime artifact retirements (145 release-note fragments, 12 logo assets, and one obsolete Azure pipeline)). The 647 undispositioned paths and the
separate feature-parity gate remain open; no runtime feature retirement is approved. PRs #127,
#129, #130, and #131 are included in ChaptarrNG `main`.
The source remains unpublished because the retirement release gate is closed. These counts identify a review queue; path or text similarity does not prove that behavior is equivalent or
safely retired. The C# token state is limited to supported literal syntax and
requires comment text to match after whitespace normalization. It establishes
source-level code equivalence only, not project inclusion, runtime behavior,
or feature parity. The complete machine-readable path ledger is in
[`chaptarr-consolidation-inventory.json`](chaptarr-consolidation-inventory.json).

The pinned audit has 197 undispositioned semantic-review paths, largest in
`src/NzbDrone.Core/MediaFiles` (17), `src/NzbDrone.Core/DecisionEngine` (14),
`frontend/src/Settings` (13), `src/NzbDrone.Core/Download` (9), and
`frontend/src/Store` (8). Another 66 changed paths have no mapped target file.
These are source-file counts for sequencing direct comparisons, not feature
counts or a risk ranking.

The detailed investigation below records historical candidate revisions and
their test evidence. Its pinned source counts and older release/channel rows
are snapshots, not current publication status. BookshelfNG issue #144 was closed by
the maintainer on 2026-10-22; its final body still keeps BookshelfNG in service
and withholds release and channel authorization until the acceptance gates
close. Closing the issue did not close those gates.

At the GitHub security audit for this work, neither repository had open
CodeQL or Dependabot alerts. Secret scanning is disabled on both repositories,
so there is no server-side secret-alert inventory. The release workflows and
local dependency checks are recorded separately from this migration evidence.

## Historical investigation snapshot — 2026-10-14

Status at that snapshot: implementation and validation in progress; **not safe
to redirect releases**. AI-assisted investigation and implementation by
Codex. Confidence was high for one populated migration-158 SQLite run,
moderate for broader conversion behavior, and low for retirement readiness.

> The inventory, branch names, pull-request states, migration target version,
> and release-channel observations below are evidence recorded on October 14.
> They are retained as history; the current status above supersedes them.

The review inventory was refreshed again on 2026-10-19. Its current source
and target pins and path states are recorded above. This October 14 section
retains the code, pull-request, and release-channel observations from that
snapshot; those observations are historical, not current status.

At this review, BookshelfNG `main` is `5d696fb0`; ChaptarrNG `main` is
`6731a436`, compared with upstream `develop` at `e67374f4`. ChaptarrNG `main`
is 606 commits ahead and zero behind upstream across 1,485 net-changed paths.
The PR #100 candidate is 25 commits ahead of ChaptarrNG `main`, zero behind,
with 359 changed paths. Open ChaptarrNG product, security, and validation PRs
#78, #100, #103, and #105–#109, along with open dependency updates, remain in
the cumulative upstream retirement gate. The integration branch
`codex/bookshelf-consolidation-integrated-20261014` is at PR head
`561bf3954d0bb2bcc3beb546accdec76f26718e4`. The importer is wired into
ordinary ChaptarrNG startup and uses the same standard product as fresh
installs. It is under review as [ChaptarrNG PR
#100](https://github.com/snapetech-org/chaptarrng/pull/100), but is not merged
or released; BookshelfNG is not ready to retire.

The local focused migration fixtures pass 23/23. The full Release-mode Core
suite passed 4,065 tests with 0 failures and 3 skipped on the same .NET
application sources as current PR #100 head; its latest commit changes only
the validation engine and its tests. A hosted Windows run on the preceding
head failed four migration/rollback tests. The validation engine now extracts
only a safe exception type and method frame, with regression coverage proving
that exception text, paths, and values stay redacted. Exact-head hosted checks,
including a Windows rerun, are queued. Local results do not close the hosted
platform gate.

ChaptarrNG PRs #73, #76, and #77 merged on October 13, 2026. BookshelfNG PR
#112 and SeerrNG PR #203 also merged. At that snapshot, the then-current local candidate and its new
hosted checks were separate from those earlier merges. BookshelfNG PR #128 is
open at `5743d1a610e8d1fd7e66c104df0e00fdaa5ee812`, PR #130 is open at
`094ac1a0a30687523fa6111dbf01286e5a7fff04`, and SeerrNG PR #280 is open at
`e844689d277bec83befd855536980b68d5045ceb`. Their required hosted checks are
queued. The conversion and channel evidence below records what has actually
been tested and what remains open.

## Populated database proof — 2026-10-14

On 2026-10-14, preview, explicit apply, and ordinary startup passed on
separate copies of one real populated BookshelfNG migration-158 SQLite
database using the ordinary ChaptarrNG Linux/amd64 image. The preview left the
source hash unchanged and accounted for every source row, including volatile
rows deliberately reset by the importer. The retained backup matched the
source table definitions and every source row. The
promoted native v119 database passed SQLite integrity and foreign-key checks.
Normal startup served the UI and preserved the existing port, URL base, API
key, SSL setting, and Docker image-pull update mechanism. The live BookshelfNG
service was not changed.

Some books needed an explicit media choice because the source did not
identify a single target format. The choices used for the technical apply
exercise were not reviewed as correct classifications. ChaptarrNG `v0.9.976`
keeps unresolved records in both catalogs without monitoring and writes a
private review file, so an operator map is no longer required to continue.
This run proves one exact populated SQLite schema and its standard-image path. It does not prove older schemas,
PostgreSQL, every provider or setting, in-place rollback on an installed service, all client
behavior, feature parity, or any published package-channel bridge.

## Pinned evidence and preservation

- Historical BookshelfNG code inventory: `9b0847973610f166523e155d3977049566d40745`,
  which was 30 commits ahead and zero behind `origin/main` at
  `ace06bc2766d26c8c5951563dd20679a486870bb`. Later documentation-only
  commits refresh the report without changing this source-code comparison.
- Historical ChaptarrNG integration base `683924daadf3201a467913c2ac4207eda6e61ea8`
  was 318 commits ahead and 3 behind its then-current main. The former
  candidate snapshot `1141c79687302366463bf87fed4565c4cc76090c` has been
  superseded; the current PR #100 head is `561bf3954d0bb2bcc3beb546accdec76f26718e4`,
  and its complete source-path comparison is in the regenerated inventory
  below.
  ChaptarrNG PR #73 merged as `5d8fffae` after all 14 reported checks passed.
  Its earlier Windows failures were resolved before merge. BookshelfNG PR #112
  merged as `7f7e07f0` with 10 successful checks and 4 skipped checks.
  ChaptarrNG PR #76 merged as `b2827c7a`; 13 checks passed, while receipt
  reconciliation exposed source-fingerprint drift. The platform receipts were
  captured after frontend CSS-module generation changed two tracked declaration
  files and created one untracked declaration; the PostgreSQL receipt used the
  clean committed tree. ChaptarrNG PR #77 merged as `ee2efc55` on October 13,
  moving the frontend build after receipt export and adding a workflow-order
  regression check. PR #100's required hosted checks passed before merge; its Windows rerun is
  noted below. Current PR #131 validation is tracked separately.

  The focused converter coordinator fixture passes 5/5 and the current
  populated importer/startup fixture passes 5/5. The fixture exercises mixed
  media and profile mapping, edition cover/link and narrator data,
  edition/file/history and series links, settings, users and notifications,
  orphan-ID reservation, restart idempotence, and safe refusal paths. The
  full Release-mode Core suite passed 4,065 tests with 0 failures and 3 skipped
  on the same .NET application sources as the current integration head.
  Twenty-three focused migration fixtures include
  rollback after a post-migration write. A self-contained Linux x64
  artifact with the production UI and updater converted the populated
  synthetic fixture on the isolated agentic VM through normal startup,
  retained a source backup identical at the table-definition and row level,
  reached migration v119, served the UI assets, and restarted without
  duplicating records. The target passed integrity and foreign-key checks and
  listened only on 127.0.0.1. Seven BookLore proxy tests passed, and the
  explicit live contract test passed against official BookLore v2.4.0: login
  succeeded, multipart upload returned 200 with an empty body, and the exact
  file bytes appeared in BookDrop. A separate, isolated BookOrbit v3.2.0
  instance passed setup, login, Book Dock access, EPUB upload and listing, and
  unsupported-file rejection. These contract checks prove API upload and file
  admission, not downstream processing of a valid production book or a real
  BookLore-user transition. Separate focused
  reruns passed 16 migration-safety cases, 29 metadata/ranking/series cases,
  and 29 rename/path cases. A hosted Windows run on the prior PR #100 head
  failed four migration/rollback tests; the corrected exact-head rerun passed
  in [run 38638159695](https://github.com/snapetech-org/chaptarrng/actions/runs/38638159695)
  before PR #100 merged as fa5384e.
- ChaptarrNG feature snapshot: `24b340fffc43eb0883995a21665d3d051eb66abe`.
  Its historical comparison against `origin/main` at `660cc034` showed 317
  commits ahead and 4 behind across 703 paths. PR #76 later integrated the
  maintained backlog into main at `b2827c7a`; PRs #69–#75 are also merged.
  The remaining feature and migration blockers are tracked in the itemized
  guide below. PR #77 merged as `ee2efc55` with the receipt-fingerprint
  correction.
  ChaptarrNG's itemized cumulative blocker table is in its
  [fork feature guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
- SeerrNG PR [#203](https://github.com/snapetech-org/seerrng/pull/203) at source
  head `dc6fe6e203ab25374581f2c24e2c858d919a549d` was squash-merged into
  `main` at `97aa148bed3a72cc02ca11f9f9d3341c230cceeb` on October 13, 2026.
  The final hosted run passed all four unit shards, lint/build, Playwright, six
  Cypress shards, docs, i18n, native validation, CodeQL, GitGuardian, and
  release-note checks; image and deployment jobs were skipped for the PR. Its
  VM smoke used an empty Chaptarr library, so it does not prove populated
  Bookshelf identity, request, or history continuity.
- Unraid companion: `bookshelfng-unraid` transition work remains on draft PR #5,
  branch `codex/bookshelfng-unraid-transition-20261018`, at current candidate
  head `1261a9f8403d88a53178b33a9f7ffeb1922d7dff`. Exact-head build
  [39387655037](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387655037),
  template [39387655072](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387655072),
  package-sync [39387655163](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387655163),
  dependency review [39387654992](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387654992),
  release-note [39388511404](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39388511404),
  Trivy [39387654943](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387654943),
  Semgrep CE [39387655051](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387655051), and Semgrep OSS
  [118511740958](https://github.com/snapetech-org/bookshelfng-unraid/runs/118511740958) passed. The local
  template contract also passes. Publication jobs were skipped; no live
  Community Applications update/rollback or representative-data migration has
  been accepted.
  The candidate keeps the Bookshelf container/template identity, port `8787`,
  `/config`, `/data`, `/download`, and PUID/PGID/TZ, while changing the image to
  `ghcr.io/snapetech/chaptarrng:latest`. It has not been merged or exercised
  through Unraid Community Applications. The separate ChaptarrNG Unraid
  listing remains the fresh-install path.
- YunoHost companion repos are separate package identities: BookshelfNG uses
  app id `bookshelfng` and port `8787`; ChaptarrNG uses `chaptarrng` and port
  `8789`. The Bookshelf package is on its historical `testing` branch, so its
  installed-app update path must be proven rather than inferred from the
  Chaptarr package.
- The BookshelfNG Helm chart is `charts/bookshelfng` and serves port `8787`;
  Merged ChaptarrNG PR #131 includes the source-level same-name chart candidate; Helm resource identity validation passed, but no chart has been republished and live update/rollback acceptance remains open.
  It preserves the Helm release, service, StatefulSet, selector, port, `/config`
  mount, and PVC identities. It requires explicit approval, source provider
  mode, and an immutable image digest, and rejects more than one SQLite
  writer. The chart is unpublished; installed PVC upgrade, GitOps sync, and
  rollback acceptance remain open.
- BookshelfNG branch used for the earlier cross-project audit: `codex/bookshelf-chaptarr-consolidation-20261012`.
- The latest published BookshelfNG release is 0.4.21.71; ChaptarrNG v0.9.977 is the latest public destination release. The published .71 archive is the migration-158 source schema baseline for read-only lineage tests.
- The generated [inventory](chaptarr-consolidation-inventory.json) covers all reachable commits after the first fork parent, including merged upstream work. It pins BookshelfNG source `7ee2917974cf2d66b3c6daa3cf5827873689ee3b` to ChaptarrNG target `0be2fe09fc8301db8a064ded4f36c5b961e06b37`: 873 commits (864 absent from upstream) and 1,151 changed paths. It records 89 reviewed mappings and 753 dispositions (175 retained, 143 equivalent, 259 ported, 176 repository-only retirements); 398 paths remain open (265 needing semantic review, 130 without mapped targets, two source-deleted paths, and one identical path). The maps carry forward decisions only when source and target blobs are unchanged, then record the four JSON-guard API routes and the same-origin bundled-asset URL guard against these exact heads. Subsequent source or target changes still require renewed review. The 24 per-project NuGet lock-file snapshots are retired as build-time artifacts; ChaptarrNG uses central package management, but direct package versions differ, so no dependency-graph equivalence is claimed. The 11 per-component test-project manifests are retired as obsolete build layout; their source test files remain open for semantic review. Recent passes cover migration and backup paths, provider behavior, author and book-file moves, metadata/profile refresh, search semantics, Goodreads series pagination, first-run authentication recovery, database-backed unmapped retry and UI workflows, and three CLI helper ports for single/bulk media moves and unmapped matching. Focused Goodreads pagination tests pass 5/5; all three migration CLI helpers pass Bash syntax, help, and ShellCheck. The exact-head Core suite passed 4,648 tests with 0 failures and 25 skips after the JSON-only API guards were ported. Other focused fixture counts are in the historical source summary below. Exact-head Build 39542301711 for `6fc744ef` passed Linux, macOS, Windows, PostgreSQL migration, and native-runner receipt checks. The earlier audited application snapshot was `3b2081f6`. Exact-head status for current `main` is tracked in the [Build ChaptarrNG workflow](https://github.com/snapetech-org/chaptarrng/actions/workflows/build.yml). Exact-head Build [39555739781](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739781) for `3b2081f6` completed successfully on Linux, macOS Intel, Windows, PostgreSQL migrations, and native-runner receipt reconciliation. The earlier documentation-only ChaptarrNG `main` commit `2ec458ff` changed no application code. At that earlier checkpoint, the 10-RID archive candidate was `4d9c4b2d`; current CI is summarized above. For ChaptarrNG application head `3b2081f6`, Trivy [39555739847](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739847) and Security analysis [39555739718](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739718) passed. Semgrep [39555740058](https://github.com/snapetech-org/chaptarrng/actions/runs/39555740058) and Automatic Dependency Submission [39555745916](https://github.com/snapetech-org/chaptarrng/actions/runs/39555745916) passed; CodeQL [39555739133](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739133) completed successfully. Earlier runs were canceled when newer main commits arrived. The review map preserves path-level review only; it is not runtime or feature-parity proof.

Regenerate the tracked-source inventory with:

```sh
python3 scripts/audit-chaptarr-consolidation.py \
  --bookshelf /path/to/bookshelfng \
  --chaptarr /path/to/chaptarrng-candidate \
  --source 685b31c93d7146258c02446b01cb34c6f5d962b5 \
  --target 813b7ff13bdfe051843f2648fa32c2ace93cb2d6 \
  --fork-base c21c4134fdb710481ed69db05bf943b0acdbbf60 \
  --upstream 3ac41f7e31427684a37138e8e539b7e6c7b73869 \
  --review-map docs/maintainers/chaptarr-consolidation-review-map.json \
  --disposition-map docs/maintainers/chaptarr-consolidation-disposition-map.json \
  --output docs/maintainers/chaptarr-consolidation-inventory.json
```

The 24 BookshelfNG per-project `packages.lock.json` paths are dispositioned as a port to ChaptarrNG central package management in `src/Directory.Build.props` and `src/Directory.Packages.props`. Direct package versions differ on some dependencies, so this disposition records the dependency-resolution mechanism only; it does not claim the resolved dependency graphs are equivalent. Exact-head build and security checks remain separate acceptance evidence.

The inventory records a `candidateTargetPath` and its `candidateTargetBlob`
only when an otherwise-unmapped source file has one target-tree file with the
same basename. Treat these as a search hint and pinned blob reference. Record
reviewed renamed-file mappings or approved retirements in
[`chaptarr-consolidation-review-map.json`](chaptarr-consolidation-review-map.json),
then regenerate the ledger. The review map pins the exact source and target
commits; stale pins, unknown paths, missing targets, duplicate decisions, and
decisions without rationale/evidence are rejected. Mapping evidence must cite
the exact target commit and target blob; retirement evidence must cite the
target commit. A mapping remains marked for semantic review, while an
explicitly approved retirement is recorded as `approved-retirement`; the tool
does not authenticate reviewer identities or infer feature equivalence from a
path decision.

Record one disposition for each changed source path in
[`chaptarr-consolidation-disposition-map.json`](chaptarr-consolidation-disposition-map.json).
Each entry pins a feature name and evidence to the inventory's exact source and
target revisions. `retained`, `ported`, and `equivalent` entries require a
reviewer and one or more target paths that exist at the pinned target revision;
their evidence must cite the exact target commit and every target blob.
`retired` entries require a named approver, approval reference, and target
commit in the evidence. The `--require-complete-dispositions` flag fails if any
changed path is missing a decision; the current map records 755 of 1,151
paths, leaving 397 undispositioned.
These records make review coverage auditable but do not prove runtime behavior,
migration safety, or operator acceptance. The inventory is schema v4.

A ported or equivalent entry looks like this:

```json
{
  "sourcePath": "src/Bookshelf/OldFeature.cs",
  "disposition": "ported",
  "feature": "Bookshelf import behavior",
  "targetPaths": ["src/Chaptarr/NewFeature.cs"],
  "reviewedBy": "maintainer",
  "rationale": "The behavior was ported to the target service.",
  "evidence": "Compared against target commit <full-sha>; target blob <blob-sha> for src/Chaptarr/NewFeature.cs; focused regression fixture."
}
```

The source and target paths are placeholders in this schema example. Replace
them with a changed source path and target paths that exist at the pinned
revisions before using an entry.

For a retired path, replace `reviewedBy` and `targetPaths` with `approvedBy`
and `approvalReference`, such as a maintainer's issue or pull-request decision.
The inventory marks a retired disposition as `approved-retirement`. If both
the review map and disposition map contain a decision for the same path, their
retirement decisions must agree.
Do not fill entries from filenames, path similarity, or generated inventory
states alone.

The BookshelfNG Build workflow tests unique, missing, and ambiguous basename
handling, reviewed mappings, stale pins, duplicate decisions, approved
retirements, complete and incomplete disposition maps, invalid target paths,
and missing retirement approvals through
`scripts/test-audit-chaptarr-consolidation.py`. The local audit-tool suite passes
31/31 tests. BookshelfNG `main` at source commit
`2811718076d84777a1b1132e4e5d2abd21231229` passed Build
[39497849780](https://github.com/snapetech-org/bookshelfng/actions/runs/39497849780),
including the Chocolatey verifier test; those hosted checks do not include the
current uncommitted audit-script changes. Unraid transition PR
[#5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) at head
`1261a9f8403d88a53178b33a9f7ffeb1922d7dff` passed its exact-head build,
template, dependency, package-sync, release-note, Trivy, and Semgrep checks;
image and standalone publication jobs were skipped. The candidate remains draft
pending representative-data and Community Applications update/rollback acceptance.
Earlier tooling receipts include hosted Build [39317318315](https://github.com/snapetech-org/bookshelfng/actions/runs/39317318315)
on commit `14032c9466b1d35f06a46d2a58239588723f63f0` and follow-up main Build
[39317910281](https://github.com/snapetech-org/bookshelfng/actions/runs/39317910281)
on commit `f9c3f404249dd6e170abdd94e2e1bc54ec61d764`, both of which passed the
audit tests. An earlier tooling checkpoint, main commit
`7a5822d93722824e38ea7a593f67abe1218d5eb6`, passed Build [39300427550](https://github.com/snapetech-org/bookshelfng/actions/runs/39300427550), CodeQL [39300427634](https://github.com/snapetech-org/bookshelfng/actions/runs/39300427634), and NuGet submission [39300429597](https://github.com/snapetech-org/bookshelfng/actions/runs/39300429597).

## Hard compatibility boundaries

1. **Database migrations are unrelated.** BookshelfNG has 46 migration
   classes whose version attributes range from 1 through 158. The Chaptarr
   baseline at PR #73 has its own rebased migration history (113 numbered
   classes, versions 1 through 114, with version 103 absent). The current
   integration candidate has 117 numbered migration files through version
   119; it removes the conflicting version 108 migration and carries that
   schema repair at version 117, then applies versions 118 and 119. Never copy
   `VersionInfo` into a Chaptarr database or run its numbered migrations
   against BookshelfNG's schema.
2. **Filename resolution is not schema conversion.** Chaptarr's
   `PathExtensions.GetDatabase()` keeps a non-empty `chaptarr.db`; when it is
   absent or empty, it selects a single non-empty legacy file from `readarr.db`
   and `audioarr.db`. If both legacy files are non-empty, startup stops with an
   ambiguity error instead of choosing or merging them. The resolver does not
   inspect schema. The startup lineage guard validates the selected database
   before migration, while `DatabaseRestorationService.Validate()` separately
   checks SQLite integrity and Chaptarr's dual-root columns for restore
   candidates. Each independently operated BookshelfNG instance can be
   migrated from its own appdata directory; merging two databases from one
   directory is unsupported.
3. **Identity changes.** BookshelfNG has one book row with multiple formats;
   Chaptarr has provider-scoped identity and media-type-specific behavior.
   Its native Hardcover mode stores many primary provider IDs as bare numeric
   values. At this 2026-10-19 checkpoint, the ChaptarrNG migration candidate used the same explicit
   mode (`HARDCOVER=true`, unless `HARDCOVER_NATIVE=false`) to route those
   values to Hardcover, and otherwise retains the Goodreads interpretation;
   preview reports the selected dialect. The source-side helper candidate has
   a `--provider-mode` option for applying one choice consistently. These
   changes still need hosted and converted-data validation. Durable
   old-to-new author/book/edition/file maps and compatibility for existing
   clients referring to numeric local IDs remain separate acceptance work.
4. **Port changes.** BookshelfNG uses 8787; ChaptarrNG uses 8789. The legacy
   distribution must retain 8787, URL base, TLS settings and reverse-proxy paths.
5. **Updater ownership.** BookshelfNG's `ReadarrCloudRequestBuilder` queries
   `https://readarr.servarr.com/v1/` with a TODO to create its own endpoint.
   Changing Snapetech GitHub releases cannot redirect those installed clients.
   A package/container upgrade or one-time bridge installation is necessary
   for installations without a Snapetech-controlled update subscription.
6. **Immutable pins remain immutable.** Digest-pinned containers, fixed version
   tags, offline machines, manual archives and disabled updaters cannot be
   silently upgraded. Never overwrite old release assets or version tags.
7. **Configuration aliases are incomplete.** Current Chaptarr bootstrap maps
   `Readarr:Postgres` and `Audioarr:Postgres` into the native configuration,
   while application, authentication, server and update options bind from
   `Chaptarr:*`. Audit and translate BookshelfNG `Readarr__*` settings plus
   `BOOKSHELF_ALLOW_API_KEY_QUERY`, `BOOKSHELF_SEERRNG_API_KEY`,
   `BOOKSHELF_METADATA_SOURCES`, `BOOKSHELF_M4B_MERGE`, and `METADATA_URL`.
   Retain TLS, URL base, custom ports, proxy trust and all secrets with native
   precedence. Existing `apikey` query clients must continue working only where
   the old Bookshelf installation allowed them; do not change Chaptarr's global
   default for unrelated installs.

## Database conversion contract — required, incomplete

The released `.69` baseline databases are real application-created but empty.
The fixture generator also seeds one linked synthetic author, book, ebook and
audiobook editions/files, series, profile/root-folder settings, user, history,
notification, and blocklist rows into the released schema. The BookshelfNG
binary can read the synthetic author and book through its API, and SQLite
integrity and foreign-key checks pass. This proves source-schema readability,
not conversion. Conversion must build a new native Chaptarr database and keep
the Bookshelf database recoverable until the new instance has passed startup
and library checks.

| BookshelfNG data | ChaptarrNG destination | Required conversion rule |
| --- | --- | --- |
| `Authors` plus `AuthorMetadata` | `Authors` and provider identity columns | Merge provider identities without treating bare IDs from different catalogs as equal; translate ebook/audiobook roots, profiles, monitoring and tags separately |
| One `Books` row with `SeriesBookLink` relationships | One or more media-specific `Books` rows plus `SeriesBookLink` rows | Split when ebook and audiobook identity or monitoring differs; persist an old-author/book to new-author/book map before converting dependents |
| `Editions` and their provider IDs | Media-scoped `Editions` and provider ID fields | Preserve ISBN, ASIN, language, format, publisher, release date and narrator data; map each old edition to its new ID without assuming title equality means identity |
| `BookFiles`, `ExtraFiles`, and Calibre links | `BookFiles`, `ExtraFiles`, and Calibre metadata | Preserve every path, size, timestamp, part, quality, chapter/duration metadata, and Calibre association; never delete or move library files during conversion |
| `Users` | Native `Users` | Preserve identifier, username, and the legacy SHA-256 password hash; Chaptarr revalidates that hash on first login and upgrades it to salted PBKDF2, which must be proven with a populated fixture |
| Quality/metadata profiles, root folders, naming, indexers, download clients, notifications, and `Config` | Native settings and profile tables | Use explicit key-by-key aliases and per-setting defaults; preserve secrets only through the documented credential path and never log them. Do not drop unsupported profile settings such as `PreferredEditionTerms` or `PreferredSeries`; add native support or halt conversion |
| `History`, `DownloadHistory`, `MetadataFiles`, `Blocklist`, and import-list state | Native history, metadata-file, blocklist, and import-list tables | Map author/book/edition/file IDs through the durable identity map; define which cache and event rows are safe to retain, rebuild, or reset |
| `VersionInfo`, commands, scheduled tasks, transient import state, FTS/index tables | Native migration history and rebuilt derived state | Never copy source migration rows or queued work; run only Chaptarr migrations, then rebuild FTS and other derived indexes from converted records |

Every one of the source's 39 tables needs an explicit preserve, transform,
rebuild, or deliberate-reset disposition; no table may disappear by omission.

The published `v0.9.977` converter is SQLite-only, supports the exact
migration-158 Bookshelf schema, and bundles the embedded source migration
chain. Its table guard rejects schemas before migration 14 because they still
use `Blacklist`. PR #126 merged a version-aware fix and synthetic migration-1
rollback fixture into `main`, with hosted Linux, macOS, Windows, and PostgreSQL
migration checks passed. The fix is not in `.977`; no release will be cut
until the retirement gates close. The populated synthetic v22 fixture
validates source upgrade, conversion, preview immutability, and rollback. This
does not establish real-data support for older schemas. The populated fixture validates a subset
of table dispositions; complete provider/configuration coverage, PostgreSQL
import, and automatic discovery of a separate Bookshelf data directory remain
open.

The first-pass disposition below names every table in the released `.69`
schema. Some mappings now exist in the local candidate, but each remains open
until populated fixtures and real-data checks validate its semantics.

| BookshelfNG source tables | Proposed ChaptarrNG disposition | Required checks |
| --- | --- | --- |
| `AuthorMetadata` | Transform into native `Authors` metadata and provider identity columns | Preserve all populated metadata and qualify provider IDs; retain ambiguous identities for review. |
| `Authors` | Transform into native `Authors`, joining `AuthorMetadata` and translating common and format-specific paths, profiles, monitoring, tags, and add options | Preserve local identity aliases and both format settings independently. |
| `Books`, `Editions` | Transform into media-specific native `Books` and `Editions`; split one source book when ebook and audiobook state differs | Preserve every ISBN/ASIN, provider ID, edition property, cover/link metadata, narrator data and monitored state; map source book and edition IDs to all target rows. |
| `Series`, `SeriesBookLink` | Transform into native `Series` and duplicate links only where a source book splits across media | Preserve series identifiers, primary status, positions and ordering without duplicate logical links. |
| `BookFiles`, `ExtraFiles`, `MetadataFiles` | Preserve file paths and metadata while remapping author, book, edition and file foreign keys | Confirm every path/size/timestamp/part and Calibre reference; never move or delete media. |
| `Users` | Preserve username, identifier and legacy password hash in native `Users` | Prove legacy login and one-time salted-hash upgrade; never copy fixture or production credentials into logs. |
| `Config` | Transform with explicit key aliases and native precedence | Account for every key, secret-bearing setting, URL base, port, TLS, proxy and environment alias; fail on unknown security-sensitive keys. |
| `QualityProfiles`, `MetadataProfiles`, `QualityDefinitions`, `NamingConfig`, `RootFolders`, `Tags` | Transform into native profiles, roots, naming and tags; derive per-format settings from the source's shared values and overrides | Preserve cutoffs, formats, language, naming, Calibre settings and fallback behavior; add support or halt if preferred terms/series cannot be represented. |
| `CustomFilters`, `CustomFormats`, `DelayProfiles`, `ReleaseProfiles`, `RemotePathMappings`, `Indexers`, `DownloadClients`, `Metadata`, `Notifications`, `ImportLists` | Transform settings/contracts and foreign keys into native integration tables | Preserve enablement, tags, priorities, credentials, protocol/category and trigger behavior; unknown contracts must be reported, not dropped. |
| `Blocklist`, `History`, `DownloadHistory`, `PendingReleases`, `ImportListExclusions` | Preserve user-visible history and pending work with target identity mapping | Preserve event meaning and provider/book references; validate pending rows before allowing acquisition to resume. |
| `Commands`, `ScheduledTasks`, `DownloadClientStatus`, `IndexerStatus`, `ImportListStatus`, `NotificationStatus`, `VersionInfo` | Deliberately reset transient queues/health/task state and rebuild target migration history | Never copy source commands or migration versions; let Chaptarr initialize its own scheduled tasks and schema. |

The released `.69` SQLite schema is not a table-for-table copy. An isolated
runtime probe on October 13, 2026 found 39 Bookshelf tables at migration 158
and 79 Chaptarr tables at migration 119. Both fresh databases passed
`integrity_check` and had no foreign-key violations; those probes contained
only application defaults. Thirty-eight table names are shared;
`AuthorMetadata` exists only in BookshelfNG, while Chaptarr has 41 additional
tables, including derived search indexes. Bookshelf stores creator data in
`Authors` plus a separate `AuthorMetadata` table and links `Books` through
`AuthorMetadataId` and `ForeignBookId`. Chaptarr folds provider metadata into
`Authors` and uses media-scoped `Books`/`Editions` relationships.

The published ChaptarrNG converter uses a SQLite staging coordinator and row
importer wired into the full startup migration path. It accepts only the exact
BookshelfNG migration-158 table set; older or altered schemas fail closed. It
snapshots the source, migrates a native target, imports source rows with
explicit row accounting, validates SQLite integrity and foreign keys, retains
a Bookshelf backup, and promotes only after validation. The importer maps
author metadata and profiles, splits mixed books, and carries editions, files,
series, blocklist, settings, and supported history relationships. It preserves
edition image and link arrays, maps narrator strings into the target narrator
list, and reserves orphan file IDs against future reuse. Unresolved format
records are preserved in both catalogs without monitoring and reported in a
private review file. Unsupported provider identities and multiple selected
editions of one format still fail closed without changing source bytes. The
coordinator fixtures passed 5/5 and the populated startup/import fixture
passed 5/5 on the earlier candidate. The published migration-158 rehearsal
proves one SQLite database only; broader data, configuration, real-data
rollback, and channel coverage remain open.

Several compatibility questions remain after the first populated fixture:

- Mixed source books now split into media-specific target rows. Editions,
  files, series links, and file-specific history follow the mapped target row;
  generic book-level history retains the source ID, which is the primary
  target row. Review this behavior against representative user histories.
  Existing clients that refer to source numeric book IDs still need tested
  compatibility beyond the database conversion itself.
- Source `DownloadHistory` has no `BookId`; the importer retains event and
  author state and uses Chaptarr's `BookId = 0` sentinel. Replay and
  deduplication behavior remains untested against a populated download client.
- Blocklist rows convert local author/book links to provider-qualified IDs.
  A row with no supported provider identity fails closed; no collision-safe
  legacy identity adapter exists yet.
- Orphan `ExtraFiles.BookFileId` values remain unchanged and are reserved above
  the target file-ID sequence. The current fixture proves the immediate and
  future-ID boundary, but real sidecar and cleanup workflows still need tests.
- User identifiers and stored legacy password hashes are copied, but a real
  first login and one-time salted-hash upgrade have not been exercised through
  the converted database.
- Settings are not yet proven key-by-key. Common profile/root/config rows,
  import-list settings, and notifications have fixture coverage, but provider
  contracts, credentials, path aliases, and source-only settings still need a
  full field audit; non-empty unmatched columns in direct-copy tables now fail
  closed.

The populated fixture covers dual-format books, file-specific history,
bookless download history, a supported blocklist identity, settings, users,
notifications, and an orphaned extra-file reference. Unsupported provider and
ambiguous monitoring cases preserve the source bytes. Real databases, old
schemas, every provider/setting contract, and client behavior remain open.

Chaptarr's app-folder resolver keeps a non-empty `chaptarr.db`, selects exactly
one non-empty `readarr.db` or `audioarr.db` only when the primary is absent or
empty, and rejects two non-empty legacy candidates. It resolves filenames
before database recovery; the lineage check runs after restore and before
migration. Full SQLite main-database startup invokes the importer for a
detected Bookshelf schema. Conversion handles one database in the selected
data directory and does not discover a separate Bookshelf mount. Two
independent installations can be migrated separately by keeping separate
appdata directories; one Bookshelf database is not merged into another. The
restore service's own candidate validation remains separate from lineage
conversion.

The converter must identify the exact Bookshelf database family and supported
schema version before writing. It must stop both applications, checkpoint
SQLite WAL, take a verified backup, and convert into a separate destination; for
PostgreSQL, use a separate target database or schema. A failed conversion leaves
the source untouched and the target unpublished. Promotion happens only after
SQLite integrity/foreign-key checks (or PostgreSQL equivalents), mapping and
row-count invariants, a clean Chaptarr startup, and API/file checks pass. The
original database and a rollback path remain available after promotion.

## Feature disposition and acceptance work

The BookshelfNG enhancements are a retirement gate as a whole and as
individual capabilities. Every row below is still an open blocker: a related
class, API label, or feature name is not evidence of equivalent behavior. A
row closes only after its behavior, configuration, identity, persisted data,
failure cases, and relevant clients have passed the stated acceptance work.
The exhaustive source commit/path inventory is an additional gate; these
feature rows do not replace it.

This gate answers whether BookshelfNG can be retired into ChaptarrNG. It is
separate from the later ChaptarrNG-to-Chaptarr gate. ChaptarrNG's existing
fork-maintained features, its features actively being added (including work
not yet in a published release), and every BookshelfNG feature retained by
this consolidation form one cumulative blocker set. The union blocks
ChaptarrNG retirement as a whole; each capability, sub-capability, migration
or data path, source-change group, and channel is also an individual gate.
Composite rows close only when every item they cover has passed its acceptance
checks. The combined matrix is maintained in the ChaptarrNG
[fork feature guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers).

The maintained backlog snapshot `24b340f` was historically 317 commits ahead
of and 4 behind `origin/main` at `660cc034`, across 703 changed paths. PR #76
later integrated that work into main at `b2827c7a`; PRs #69–#75 are merged.
The remaining active capabilities, proposed channel changes, and acceptance
evidence are listed in the ChaptarrNG
[itemized cumulative blocker matrix](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
PR #73's metadata-preference port is merged, but its capability parity and
release acceptance remain individual blockers. Active capabilities count
before release.

| BookshelfNG capability or change | ChaptarrNG finding (source unless stated) | Retirement status | Required disposition and evidence |
| --- | --- | --- | --- |
| Rich book lookup; SeerrNG capabilities; paged books; format availability | A populated synthetic smoke passed on 2026-10-18 against ChaptarrNG candidate `0.9.978.0`, code head `1a0a1cf7`, and SeerrNG `0b267d526`. It verified status/capability discovery, one audiobook through SeerrNG's paged-library adapter, migrated audiobook and ebook provider identities in ChaptarrNG, and denial of administrative and unrelated command routes with the restricted key. A current-source Compose smoke against PR #131 head `ddec3e81` (code snapshot `2c0401fc`) and SeerrNG `10f06eab9` passed capability discovery, empty paged-library access, and restricted-key denial for administrative and unrelated command routes. | **Open blocker — end-to-end integration parity unproven** | Test unchanged SeerrNG settings, requests and history, pending work, availability links, and proxy deployments against a populated migrated library. |
| Native Hardcover, pacing, retry headers, author reuse, and refresh-age policy | Native Hardcover and V5 metadata implementations exist in a different provider pipeline | **Open blocker — semantic parity unproven** | Compare cache lifetime, key isolation, batching, 429 handling, refresh rules, and identity routing; retain configured behavior. |
| Supplemental catalogs: Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify; per-field preferences | ChaptarrNG main after PR #127 (`b3089a39`) includes these adapters, selectable sources, qualified IDs, and per-field choices; hosted platform and security checks passed. Not in public `.977`. | **Source port merged; operator/settings acceptance open** | Preserve source selection/fallback, qualified IDs, field choices, provider-specific request constraints, and saved settings on converted operator data. |
| Cross-catalog unmapped recovery; normalized title and identifier matching | ChaptarrNG main after PR #127 uses exact ISBN/ASIN/provider IDs or normalized title and author, checks media type and stable identities, and queues the existing pending-author import without attaching files. PR #130 adds a lossy mapping from 50–66 to Aggressive, 67–82 to Balanced, and 83–99 to Strict when no explicit mode exists; invalid legacy values fail closed. Hosted checks passed. The source is not in public `.977`. | **Source port merged; behavioral/data acceptance open** | Verify no-false-match, ambiguity, converted provider IDs, the threshold approximation, and no-delete constraints on representative libraries. |
| Multiple ebook/audio formats; per-format folders and profile overrides | Native media-specific models, roots, and profiles exist | **Open blocker — conversion and isolation unproven** | Convert all rows and references; verify fallback rules, sibling-format isolation, monitoring, imports, upgrades, scans, and renames. |
| Combined Bookshelf Formats view | ChaptarrNG `main` loads audiobook and ebook shelf records together, groups only matching Hardcover, Goodreads, or Open Library work IDs, retains separate detail/progress/monitoring state, and applies bulk monitoring to both formats. Focused grouping and API fixtures cover safe identities and summed author counts; the browser view is not in published `.977`. | **Source implementation added; mixed-library acceptance remains open** | Verify matched aliases, mismatched and absent IDs, duplicate editions, reload/retry, per-book and bulk monitoring, and layout on a representative converted library. |
| Books index Both filter | ChaptarrNG `main` loads both media types through the paged Books endpoint, labels each row, and keeps status, monitoring, and quality-profile selection scoped to that row. Focused regressions cover query behavior and per-format profiles. Commit `a733e5f4` adds retryable paged mass-search, Select All, bulk Update, refresh, and RSS Sync workflows; unstarted search requests are invalidated on filter or format changes. Not in public `.977`. | **Source implementation added; browser acceptance remains open** | Verify paging, custom filters, sort order, narrator controls, selected-row and bulk edits, and per-format profiles on a representative mixed library. |
| Weighted edition terms, preferred series, narrator evidence, and publisher/dramatized cases | Merged ChaptarrNG PR #131 adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; Chaptarr's stronger match evidence stays ahead of the preference signal | **Source port merged; retirement blocker remains open** | Preserve weights, series choices, missing-evidence neutrality, tie behavior, and manual-review boundaries; verify the full Bookshelf edge-case set after profile/database conversion. |
| Optional M4B merge, chapters, part order, and completion state | ChaptarrNG PR #129 merged to main as 949ae3dd; PR #131 commit c4fa8125 fixes source cleanup after successful profile-based multipart merges in Move mode while Copy mode retains originals. Embedded-chapter Move/Copy tests and TagLib write/reprobe checks pass on exact-head Linux Build [39288736177](https://github.com/snapetech-org/chaptarrng/actions/runs/39288736177), together with the six-case pinned-tool M4B merge/fallback smoke. The same run passed PostgreSQL migration and release-note checks; Windows build and full test steps passed; macOS was cancelled before starting, so the cross-platform matrix is incomplete. | Source port merged; acceptance remains open | Validate representative M4B media and restart/resume with representative Move/Copy deployments. |
| Vendored TagLibSharp patch (253 changed source paths; byte-preserving MPEG-4 `chpl` handling) | Merged ChaptarrNG source vendors the BookshelfNG TagLibSharp fork and passes a synthetic version-1 `chpl` fixture that verifies exact atom preservation while writing a title. The vendor contains its LGPL-2.1 `COPYING` file; its strong-name key matches the key already committed with the BookshelfNG vendor source. | **Local port and focused regression pass; broader compatibility remains an open blocker** | Prove behavior on representative existing M4B files and across tag edits, conversion outputs, and failure cases; review continued use of the vendor signing identity and upstream the supported implementation. |
| Add New search preference | Optional search-as-you-type preference | ChaptarrNG `main` carries the browser preference and waits for Hardcover configuration before issuing that provider's search. This behavior is not in published `.977`. | **Source behavior implemented; browser acceptance open** | Check persistence, repeated-query search, clearing during a slow request, and a host/origin change. |
| Import-list preview/history and Hardcover connection recovery | Per-list preview, sync history, saved Hardcover identity status, and retryable provider errors | Commit `a733e5f4` shows loading, connected, or unavailable Hardcover status; connection checks can be retried, preview/history errors expose available API details, and closing the modal discards stale preview responses. Focused CJS fixtures pass; these UI changes are not in public `.977`. | **Source implementation added; provider acceptance remains open** | Verify status refresh, preview/history errors, retries, saved credentials, and provider behavior against representative accounts. |
| Interactive series-pack search | Search for an indexer pack covering one series, then map the downloaded files to individual books | ChaptarrNG `main` adds the series-row action and API query. The search uses local series links, the selected author's catalog, and the series media type; the cached release retains the books for Manual Import. A focused C# fixture covers the author-scoped ordered series and import context. | **Source implementation added; live workflow acceptance open** | Confirm results, grab, queue tracking, and per-file Manual Import assignment against a running instance. |
| Existing-torrent adoption and seeding preservation | Native continuation/adoption work exists | ChaptarrNG `main` checks info hashes before a torrent grab, prompts for explicit interactive adoption, tracks the existing client ID without requesting the indexer again, and skips duplicates in automated searches. New fixtures cover hash matching, adoption, stale/unavailable client states, and no second download. | **Source implementation added; edge cases remain open** | Test same-category and wrong-category cases, completed downloads, seeding-data preservation, completion import, and restart behavior with supported clients. |
| Direct Download and browser-assisted grab | ChaptarrNG source `a1146edd` restores KEPUB, MOBI, and AZW3 catalog search, resolves KEPUB detail-page links, and marks direct ebook releases with Books/Ebook category 7020. Regression fixtures cover the catalog query/results, KEPUB resolution, and category. Build [39524671037](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671037) failed the KEPUB extension-label regression; commit `a1146edd` fixes it. Exact-head Build [39539307423](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307423) passed Linux, macOS, Windows, PostgreSQL, and native-runner receipt reconciliation on the previous candidate; Build [39542301711](https://github.com/snapetech-org/chaptarrng/actions/runs/39542301711) for `6fc744ef` passed Linux, macOS, Windows, PostgreSQL, and native-runner receipt checks; The earlier audited application snapshot was `3b2081f6`. Exact-head status for current `main` is tracked in the [Build ChaptarrNG workflow](https://github.com/snapetech-org/chaptarrng/actions/workflows/build.yml). Exact-head Build [39555739781](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739781) for `3b2081f6` completed successfully on Linux, macOS Intel, Windows, PostgreSQL migrations, and native-runner receipt reconciliation. The earlier documentation-only ChaptarrNG `main` commit `2ec458ff` changed no application code. The current audit now pins the 10-RID archive candidate at `4d9c4b2d`; current CI is summarized above. For ChaptarrNG application head `3b2081f6`, Trivy [39555739847](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739847) and Security analysis [39555739718](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739718) passed. Semgrep [39555740058](https://github.com/snapetech-org/chaptarrng/actions/runs/39555740058) and Automatic Dependency Submission [39555745916](https://github.com/snapetech-org/chaptarrng/actions/runs/39555745916) passed; CodeQL [39555739133](https://github.com/snapetech-org/chaptarrng/actions/runs/39555739133) completed successfully. Earlier runs were canceled when newer main commits arrived. Preceding Build [39538783209](https://github.com/snapetech-org/chaptarrng/actions/runs/39538783209) was cancelled when the Calibre tag correction landed before its platform matrix completed. Earlier Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373) passed Linux, macOS, Windows, PostgreSQL migration, and runner-receipt checks. Other fixtures cover ordered source fallback, legacy URL-array settings, API-key preservation/redaction, durable state across restart, interrupted-transfer handling, browser fallback recovery, redirect-hop validation, private-address rejection, and redirect-body clearing. | **Source-level settings and recovery compatibility covered; retirement acceptance remains open** | Validate representative saved configurations, real client/source behavior, installed-state handoff, supported browser architectures, and source/transfer recovery on a deployed instance. Verify interrupted transfer/restart on an installed instance before closing the row. |
| BookLore BookDrop and BookOrbit transition | Optional BookLore integration ported in PR #73; seven proxy tests and live BookLore v2.4.0 upload/file-placement checks pass. Merged ChaptarrNG PR #131 adds a separate BookOrbit destination; mock tests cover authentication, streaming, redirects, rejection, and partial batches; isolated BookOrbit v3.2.0 setup/login/access/EPUB-upload/listing and unsupported-file checks pass. | **Open blocker — real-user transition and downstream processing** | Preserve BookLore settings and credentials as BookLore; never infer a BookOrbit host or account from them. Configure ChaptarrNG's BookOrbit settings separately. Test BookOrbit's later processing of a production book and document a real-user handoff. Keep the non-atomic partial-batch behavior clear and test rejected-file recovery. |
| Provider settings and built-in integrations | Merged PR #131 source checks provider implementation and `ConfigContract` compatibility across indexers, download clients, import lists, notifications, and metadata. It retains settings only when the contract and serialized fields match a Chaptarr provider. Unsupported pairs or unknown fields are disabled in the staged copy, reported without secret values, and block apply before promotion. Alias handling covers `LegacyAudiobookshelfMetadata`; unknown metadata-file consumers also block apply. Fixtures cover QBittorrent, MyAnonamouse, Direct Download, Goodreads and BookLore contracts, unsupported plugins, unknown settings, and sidecar consumers. Exact-head Build [39332160991](https://github.com/snapetech-org/chaptarrng/actions/runs/39332160991) passed on application-code head `7b4c66e3`. | **Implementation safety covered; integration acceptance remains open** | Validate each supported provider's saved credentials, live API behavior, identifiers, generated metadata, and error handling against representative converted data; keep unknown plugins blocked until mapped or explicitly retired. |
| Previewable single/bulk media moves and extra-file handling | Folder and colocation models differ | **Source implementation merged; hosted validation passed, acceptance remains open** | Preview and confirm single or bulk moves, include registered book sidecars, block conflicts, bind execution to a fresh preview token, and leave unknown/external files and author-wide extras untouched. Validate cross-device behavior, partial-failure recovery, root containment, and representative libraries before closing parity. Head `2c0401fc` fixes Windows-only test failures caused by POSIX fixture paths; exact-head hosted run `39196795646` passed. |
| Optional diagnostics assembly | ChaptarrNG `v0.9.977` ships the separate `Chaptarr.Diagnostics.dll` replacement. It is disabled by default; the legacy BookshelfNG enable flag is honored only when the archived `plugins/Bookshelf.Diagnostics.dll` marker exists, and an explicit ChaptarrNG setting takes precedence. Reporter fixtures cover the fixed event allowlist, aggregate-only payload, legacy endpoint/token fallback, invalid endpoint rejection, and explicit disable. PR #131 now adds startup-path fixtures for default-off, marker-gated legacy opt-in, explicit current enable/disable, and missing-module behavior. | **Replacement implemented; installed transition acceptance remains open** | Verify appdata and environment handoff on representative installed deployments, including both marker states and default-off behavior. |
| Restricted service key, query-key policy, trusted proxies, body/rate limits | ChaptarrNG main `29852b13` ports explicit proxy IP/CIDR and CORS origin allowlists, 600/minute per-client rate limiting (60–6,000 configurable), a 16 MiB global body cap (1–128 MiB configurable), and the legacy request-ID response header. `CHAPTARR:Server` settings take precedence; the legacy `Readarr:Server` keys remain accepted. The backup restore route keeps its separate 1 GiB limit. These changes are not in public `.977`. | **HTTP control source parity implemented; installed acceptance remains open** | Verify legacy key aliases, trusted hops, browser origins, existing credentials, and large backup restores on representative deployments. Authentication and query-key aliases must preserve existing client behavior and configured restrictions. |
| Encrypted backups and format-scoped profiles | Merged PR #131 includes recognized BookshelfNG ZIP restore with lineage/version validation, staged restore, and normal-startup conversion, plus portable BKSENC01 `.enc` export and restore (introduced at candidate `38be9422`, present in code commit `b7e900d4` and application-code commit `0e881d92`). The encryption service was cross-checked against BookshelfNG source; tests cover round-trip, wrong passphrases, tampering, truncation, malformed input, staging cleanup, and preserving an existing destination. Build [39313568727](https://github.com/snapetech-org/chaptarrng/actions/runs/39313568727) passed on Linux, macOS, and Windows, including PostgreSQL migration, release-note, receipt, and Linux pinned-tool M4B checks. Prior docs-only PR head `93213b67` passed exact-head Build 39316535744 on Linux, macOS, Windows, PostgreSQL migration, release-note contract, and native-runner receipt reconciliation. Public `.977` still lacks these restore and encrypted-backup paths. | **Source implementation merged; acceptance remains open** | Test legacy archive recovery, secret handling, profile conversion, and rollback on representative data; never expose credentials in logs. |
| .NET 10, platform builds, ImageSharp removal, and security/dependency fixes | .NET 10 is present; target has different dependencies and still uses licensed ImageSharp | **Open blocker — patch-by-patch review pending** | Review each security and dependency change; retain compatible fixes and prove supported OS/architecture builds. |
| Release notes, announcements, package sync, and validation workflow | ChaptarrNG has separate release and validation workflows | **Open blocker — legacy identities not bridged** | Preserve old package/container IDs through tested compatibility artifacts; complete required per-repository validation without duplicate publication. |
| Every remaining fork change in the pinned source inventory | The current schema-v4 audit pins BookshelfNG source `7ee2917974cf2d66b3c6daa3cf5827873689ee3b` to ChaptarrNG target `0be2fe09fc8301db8a064ded4f36c5b961e06b37`: 1,151 changed paths, 89 reviewed mappings, 753 dispositions (175 retained, 143 equivalent, 259 ported, 176 repository-only retirements), and 398 open paths (265 requiring semantic review, 130 without mapped targets, two source-deleted paths, and one identical path). No runtime feature retirement is approved. The M4B, author, AudioBookShelf, catalog, media-move, compatibility, and migration guides are documentation-only ports; package path dispositions describe candidates only. Runtime and operator acceptance remain open. | Path classifications do not establish semantic feature equivalence. | Disposition every remaining path as retained, ported, proven equivalent, or explicitly approved for retirement. |

The commit/path inventory remains the exhaustive review ledger. Every
behavioral change must be retained, ported, or proven equivalent; packaging
changes need a compatible channel disposition. Calling a feature obsolete
does not close its blocker. Any proposed removal remains open until an explicit
maintainer decision about its user impact. Similarity is not evidence, and the
combined feature set cannot be retired while any individual row or inventory
path remains open.

## Migration design

1. Detect lineage by schema and configuration, not filename or highest migration
   number. Reject unknown/mixed schemas without changing them. Detect active
   writers and refuse migration while the original app is running.
2. Take a consistent database backup (including WAL via the database backup
   API), configuration and application-state checkpoint. Check free space,
   ownership and integrity. Do not touch media or fetch metadata during conversion.
3. Create a new target database using Chaptarr's actual migrations. Convert into
   staging. Carry users/auth/API key, settings, root folders, download clients,
   indexers, tags, profiles, lists, notifications, authors, books, editions,
   files, series, history, blocklist, pending releases and transfer state.
   Classify every source table/column; never silently discard unknown state.
4. Map provider identity using explicit source lineage (`hardcover`/`softcover`)
   and stored provider identifiers. Preserve ebook/audio coexistence and all
   local foreign-key relationships. Record split records in an alias map used
   by legacy API routes and SeerrNG reconciliation. In native Hardcover mode,
   run preview and apply with that provider mode enabled so bare numeric IDs
   cannot be mistaken for Goodreads IDs.
5. Validate row accounting, foreign references, file path/size preservation,
   profile selections, historical references, encrypted backup round trip and
   unchanged credentials. Rebuild target indexes/FTS from converted rows.
6. Start a disposable target against staging with schedules and external writes
   disabled; run old and native API probes. Commit the migration marker and
   database/config switch only after all checks succeed. Use crash-recoverable
   phases and test termination at each phase. Restart must be idempotent.
7. Rollback before accepting new target writes restores the old checkpoint and
   image/package. After target writes, restoring an old checkpoint loses new
   work: require a deliberate recovery choice, never silently revert on boot.
8. PostgreSQL requires its own staged database/schema conversion and connection
   switch; SQLite-only proof cannot authorize PostgreSQL redirection.

## Distribution bridge matrix

Retain the old installation identity while delivering the ChaptarrNG application.
This avoids two services, data-directory moves and package-manager replacement
conflicts. The legacy package can remain a thin maintained compatibility package
after application development stops. Source retirement is not publisher retirement.

**Current state: no legacy bridge has been published or activated.** The
ordinary ChaptarrNG v0.9.977 image and native package are available, but
both repositories' release-ready flags remain unset and the migration bridge
is disabled. Do not publish a bridge release while retirement acceptance is
open.

ChaptarrNG PR [#100](https://github.com/snapetech-org/chaptarrng/pull/100)
and BookshelfNG PR
[#130](https://github.com/snapetech-org/bookshelfng/pull/130) are merged.
Their publisher code remains gated. The user-owned
[GHCR bridge](https://github.com/snapetech/bookshelfng-ghcr-release-bridge)
can retag the standard ChaptarrNG multi-architecture image only after a
validated gated release and verified package write access; the BookshelfNG
image aliases have not changed.

The ChaptarrNG AUR identity chaptarrng-bin 0.9.977-1 is public. The
BookshelfNG identity bookshelfng-bin 0.4.21.71-1 remains public on the
BookshelfNG payload. A local bookshelfng-bin 0.9.977-1 candidate passed an
isolated, network-disabled pacman upgrade from .71 and downgrade back to
.71, preserving an environment override and synthetic data canary. The
installed package also passed preview, conversion from a synthetic populated
migration-158 database, restore, and SQLite integrity/foreign-key checks.
An active systemd rehearsal stopped the `.71` BookshelfNG service during
upgrade, started ChaptarrNG for conversion, and restarted BookshelfNG after
restore and downgrade. The network-online wait was masked only in the isolated
test container. Acceptance with operator data and host-specific settings remains
open.

COPR built standard chaptarrng 0.9.977-1 for Fedora 43, 44, 45, and Rawhide;
the legacy trigger was skipped and old-identity upgrade acceptance remains
open. Chocolatey built the standard .977 package and passed a hosted
BookshelfNG-to-ChaptarrNG package smoke, but publication returned HTTP 403.
The live feed has no `chaptarrng` entry; the published Chocolatey
`bookshelfng` package remains at `0.4.21.70`, while the latest GitHub release
is `0.4.21.71`. The legacy identity was not submitted. BookshelfNG-Unraid PR
#5 is open as a draft; its Community Applications upgrade and rollback flow
has not been tested.

No server-side redirect reaches every historical installation. The
Readarr-owned in-app updater cannot be redirected by these repositories, and
pinned images, offline hosts, disabled updaters, and manual archives need an
explicit update action. Each retained channel needs its own tested bridge or
documented one-time handoff.

| Existing channel | Bridge needed | Automatic reach / acceptance |
| --- | --- | --- |
| GHCR and Docker Hub `latest`, `hardcover`, and `softcover` aliases | The merged gated publisher code can retag the exact standard ChaptarrNG multi-architecture digest; no second image build is needed. Legacy aliases remain unchanged. | Verify write access and exact digest equality for each registry. Tags affect only a later pull/recreate; running containers and immutable pins require an operator action. |
| Version/digest-pinned containers | Publish the standard ChaptarrNG image and provide a migration step and replacement digest | Explicit update needed; old pins remain recoverable |
| Unraid | Keep the BookshelfNG template identity and legacy mounts while changing its repository/tag to the ordinary ChaptarrNG image. Preserve port, `/config`, `/data`, `/download`, PUID/PGID, and TZ through the template and standard-image configuration. Update and sync companion `bookshelfng-unraid`. | Existing containers can pull the old image alias on their next update; changing the CA template alone does not rewrite an already-created container. Validate the installed template update plus stop, backup, conversion, restart, and rollback. |
| Debian/Ubuntu direct package and PPA | ChaptarrNG main has a candidate builder for a higher-version bookshelfng .deb, preserving the old package/service/data/environment identities; a dpkg --root round-trip with the actual public .71 package and local .977 candidate preserved a modified conffile and data canary. | Dependency-resolved apt, real systemd handoff, PPA source package, database migration/restore, and representative-data rollback remain untested; no bridge is published. |
| Fedora/RPM/COPR | The standard ChaptarrNG `.977` package built for Fedora 43, 44, 45, and Rawhide. The legacy trigger was skipped while the bridge is disabled. | Validate the old package identity, update the external bootstrap if needed, and exercise install, service stop, migration failure, retry, and rollback. |
| AUR `bookshelfng-bin` | Local `.977-1` candidate retains the package identity, service, data path, and hooks; pacman upgrade/downgrade and active systemd handoff plus migration/restore against synthetic populated migration-158 data passed | AUR helpers can install the candidate after publication, but there is no push mechanism. Acceptance with representative operator data and host-specific service settings remains open. |
| Chocolatey `bookshelfng` | The merged bridge candidate builds both package identities from the checksummed standard archive. The `.977` hosted upgrade smoke passed, but publication returned HTTP 403; no public `chaptarrng` package exists and the published `bookshelfng` package remains at `0.4.21.70` (GitHub release `0.4.21.71`). | Resolve publisher authorization before publishing, then validate the old identity with populated data, startup, and rollback. |
| Windows setup / portable | Bridge installer recognizes old installation, stops service, retains data/auth/port and recovery backup; launcher compatibility | One-time installer for unmanaged installs; old updater cannot be redirected by GitHub changes |
| macOS/Linux/FreeBSD archives | Legacy named wrapper/payload and migration-aware launcher in new bridge assets | Manual replacement unless an existing owned updater is subscribed; verify each platform rather than assuming Linux proof |
| AppImage | Rebuilt local `.978` candidate passed a same-identity update rehearsal from the public `.71` package using synthetic schema-158 data; preview, migration, shared-root path preservation, restore, and old-package restart passed. | Representative-data acceptance and a published update-channel rehearsal remain open; see the [candidate evidence](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md#legacy-install-channels). |
| Flatpak bundle | Rebuilt local `.978` bundle updated the existing `com.snapetech.BookshelfNG` app ID and passed the same synthetic schema-158 migration, path-preservation, restore, and public `.71` rollback start checks. | Representative-data acceptance and a subscribed Flathub update rehearsal remain open; a local bundle rehearsal does not validate a published remote. See the [candidate evidence](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md#legacy-install-channels). |
| Helm OCI chart | Merged ChaptarrNG PR #131 includes a source-only, fail-closed same-name chart. `helm lint`, render, package, and exact StatefulSet/Service/PVC spec comparison against the current BookshelfNG chart pass locally. It requires explicit migration approval, provider mode, and an immutable ChaptarrNG image digest. | No ChaptarrNG chart is published, and the legacy OCI source remains unchanged. Test a real PVC upgrade, configured Helm/GitOps sync, selectors, installed rollback, and one SQLite writer before publishing or recommending cutover. |
| YunoHost historical installs | BookshelfNG app id `bookshelfng` and port 8787 differ from ChaptarrNG app id `chaptarrng` and port 8789. BookshelfNG publishing is retired; inspect installed catalog identity and companion repo branch, then provide a tested upgrade under the old app id with its existing service, URL path, data directory, and rollback. | The ChaptarrNG app listing cannot update an installed BookshelfNG app. Existing installs are reachable only if the old package's configured repository still delivers the compatibility upgrade. |
| Cloudron / Coop Cloud / StartOS catalog files | Verify which were actually accepted/published, then retain installed catalog IDs and data contract | A repository recipe/submission is not proof of an installed distribution channel |

Verify registry/package ownership, configured publisher state and signatures with
read-only API checks before designing an upload as available. Missing credentials
must be reported as unverified/unpublished, not a successful migration channel.

## Ordered implementation and release gates

1. Complete pinned feature/commit review, bridge inventory and recovery design.
2. Port independent missing features with native target tests and release notes.
3. Build lineage guard, converter, compatibility aliases and legacy image/package
   launchers. Exercise migration against generated fixtures from actual released
   BookshelfNG binaries, not hand-written approximations alone.
4. Verify SeerrNG before/after requests, local IDs, provider dialects, availability,
   polling, restricted credentials and pending requests without recreating servers.
5. Run repository-native validation engines on exact integrated source, including
   existing unrelated/dirty work requested by the maintainer. Record failures,
   skipped tests, source identities and runtime/live proof separately.
6. Install into disposable LAN VM environments. Test old release -> bridge ->
   restart -> subsequent target upgrade; forced migration failure; interrupted
   migration; disk full; missing secret; mixed formats; empty and populated
   libraries; SQLite WAL; PostgreSQL; custom URL base and port; non-root ownership.
7. Test package-manager upgrade/remove/reinstall semantics, configured update
   subscriptions, checksums/signatures, immutable release assets and downgrade
   recovery. Windows/macOS/FreeBSD and arm64 need corresponding execution evidence.
8. ChaptarrNG PR #131 is merged to `main`; verify the merged tree and preserve its
   exact-head receipts. Continue SeerrNG, representative-data, and channel acceptance
   before preparing any BookshelfNG bridge automation.
9. Publish an immutable bridge release, test installation of its published artifacts,
   then advance moving aliases/publishers. Record digests and package versions.
   Keep old images/assets and the compatibility release machinery available.

## Evidence ledger

| Area | Current evidence | Status | Required action |
| --- | --- | --- | --- |
| BookshelfNG source inventory | Regenerated against source `7ee2917974cf2d66b3c6daa3cf5827873689ee3b` and ChaptarrNG target `0be2fe09fc8301db8a064ded4f36c5b961e06b37`: 873 commits, 1,151 paths, 89 reviewed mappings, 753 dispositions, and 398 open paths (265 semantic review, 130 unmapped, two source-deleted, one identical). The four JSON-guard API routes and the generated asset-URL guard are mapped and dispositioned at these exact heads. | Path classifications do not establish semantic feature equivalence. | Review and disposition the 398 open paths; keep production acceptance gates separate. |
| ChaptarrNG Bookshelf feature port | PR #131 merged the source implementation to ChaptarrNG `main` as `d2bcba79`, including the migration, settings/provider, backup, media-move, Editions and Narrations, BookOrbit, SeerrNG, and Windows installer work. Earlier local migration and isolated integration rehearsals remain synthetic or limited to one data copy. | Source implementation is present on `main`; release and operator acceptance remain open. | Review ambiguous media and validate conversion, rollback, provider fulfillment, representative M4B, downstream BookLore/BookOrbit behavior, SeerrNG request/fulfillment, and installed channels on representative deployments. |
| ChaptarrNG maintained and active features | At the earlier cross-project audit, ChaptarrNG `main` at `6731a436` was 606 commits ahead and zero behind upstream `develop` at `e67374f4`, across 1,485 net-changed paths. PR #100 at `561bf395` was 25 commits ahead of main across 359 paths; the audit also recorded PRs #78, #100, #103, and #105–#109 and open dependency updates. Recheck current upstream status before using this historical audit. | Historical upstream audit; current open PR/feature set not rechecked. | The earlier audit tracked upstream parity as a separate gate; refresh the ChaptarrNG-to-upstream comparison and carry forward only changes still open. Recheck current upstream changes and reconcile any remaining fork behavior before closing the Bookshelf retirement gate. |
| Bookshelf database compatibility | Merged ChaptarrNG PR #131 adds the embedded historical SQLite migration chain, migration-158 PostgreSQL source migration support, staged conversion/rollback handling, provider-setting checks, and a Windows migration installer. The exact-head synthetic Windows service round trip passed upgrade, automatic rollback, explicit restore, and data-directory checks. | Source code is merged but unpublished. A populated schema-158 SQLite snapshot passed preview, conversion, integrity and foreign-key checks, row/path accounting, and database rollback on a disposable copy. Older supported SQLite schema acceptance, PostgreSQL operator-data migration, ambiguous-media review, live providers/media, installed-service rollback, and channel handoff remain unaccepted. | Keep BookshelfNG in service. Validate representative populated source databases and media, source immutability, correct identities/settings/history/files, and real rollback before any production cutover. |
| ChaptarrNG runtime and SeerrNG (prior synthetic evidence) | The ordinary Linux/amd64 image previously started a populated converted database, served `/ping` and the production UI, preserved port, URL base, API key, SSL, configured indexers, and Docker image-pull update behavior, and passed SQLite/FK checks; the live BookshelfNG service was untouched. The newer source-built smoke at ChaptarrNG commit `12f290bd` and SeerrNG commit `fdc439aa9` seeded a synthetic BookshelfNG migration-158 database, converted it during normal startup to schema 121, retained the source backup, and persisted `HardcoverEnabled=true` for `HARDCOVER=true`. SeerrNG read both migrated audiobook and ebook records with their Hardcover identities. Capability discovery, restricted-key denial for administrative and unrelated commands, and the pending add/poll/cancel flow passed; the importer suite passed 43/43. The `.m4b`/`.epub` placeholders are not valid media. A separate six-case real-tool importer test passed synthetic M4B merge and fallback cases on candidate `12f290bd`, and Linux CI now runs it. | Synthetic conversion, record access, and request cancellation passed. | Validate representative data, successful provider fulfillment and retries, availability/history, unchanged settings, representative M4B and restart/resume, full parity, installed rollback, and update channels. |
| Frontend build and static checks | `yarn typecheck` and the production webpack bundle pass; targeted ESLint reports no errors in changed JavaScript files. The bundle emitted 18 CSS-order warnings. Whole-tree ESLint reports 862 errors and 17 warnings across the inherited frontend tree. | The inherited lint debt remains; changed-file checks show no reported errors. | Resolve change-caused issues and rerun relevant build/static checks before release. |
| Cross-project secrets | All three repositories ignore `.env`; BookshelfNG and SeerrNG have local ignored, untracked `.env` files, while this ChaptarrNG worktree has no `.env` file. No `.env` or `.lic` file is tracked. BookshelfNG's Docker ignore excludes `.env`/`.env.*`, the SixLabors license, and signing files while retaining `.env.example`; a disposable Docker build-context check confirmed `.env.example` stayed in the context and `.env` did not. The license file remains outside repository trees. | No `.env` or `.lic` files are tracked; the disposable Docker-context check excluded `.env` while retaining `.env.example`. | Repeat Git and Docker-context checks before release; keep secrets out of commits, logs, and artifacts. |
| Hosted PR checks | ChaptarrNG PR #131 merged to `main` as `d2bcba79` from validated head `87c57a2b`. Exact-head Build [39374140961](https://github.com/snapetech-org/chaptarrng/actions/runs/39374140961) passed Linux, macOS, Windows (including migration-installer fingerprint, service upgrade, automatic rollback, explicit restore, cleanup, and selected-data-directory checks), PostgreSQL migration, release-note contract, and native-runner receipt reconciliation. CodeQL, dependency review, dependency/secret scan, Semgrep CE, Trivy, NuGet, and Helm resource identity passed; disposable-fork validation was skipped by its gate. | The separate GHAS Semgrep OSS check remains failed with 12 reviewed SQL-format alerts and 3 fixed-test-path warnings; focused local SQL-rule scans returned zero findings. This exception is documented in PR #131. The merge does not close representative-data, parity, provider, rollback, or channel acceptance. No release was published; issue #144 remains open. | Keep the release freeze and BookshelfNG service in place until acceptance closes. |
| Distribution and migration | ChaptarrNG `v0.9.977` and its standard multi-architecture GHCR image are published; release gates remain closed. ChaptarrNG AUR `chaptarrng-bin 0.9.977-1` is public, and the BookshelfNG AUR identity has a local `.977-1` candidate that passed pacman upgrade/downgrade and active systemd service migration/restore against synthetic populated migration-158 data. COPR built the standard `.977` package for Fedora 43, 44, 45, and Rawhide; its legacy trigger was skipped. The `slskdn/bookshelfng` COPR repo has no package entries for Fedora 43/44/45/Rawhide. A Fedora 44 transaction upgraded the published BookshelfNG `.71` RPM to a local `.977` bridge candidate and downgraded back with config/data canaries; it used `rpm --nodeps` and mocked `systemctl`. The Chocolatey `.977` package and hosted upgrade smoke passed, but publication returned HTTP 403; BookshelfNG `.70` remains public. | No legacy redirect or compatibility package is published; the migration bridge remains disabled. | Complete representative AUR/service, live COPR/DNF, Chocolatey old-identity upgrade, GHCR write/digest, Unraid install/rollback, and pinned/offline/updater handoff acceptance. |
| Release decisions | ChaptarrNG PR #131 source is merged to `main`, but the merge is not a parity or retirement approval. Every BookshelfNG capability, migration path, and distribution channel remains an individual acceptance gate. | Current evidence does not support retiring BookshelfNG, redirecting releases, or enabling compatibility publishers. | Close the documented operator and maintainer acceptance gates first; only then review a separate release and channel handoff. |
