# BookshelfNG

> **Retirement status — 2026-10-21:** BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` is at [`e3759f7a`](https://github.com/snapetech-org/chaptarrng/commit/e3759f7a78d5ba35db73a7735dd79bbf84c12939). It now owns the Docker migration handoff helper and will include it in Linux standalone archives after a release is approved. Build [39533338459](https://github.com/snapetech-org/chaptarrng/actions/runs/39533338459) for this commit is running. The preceding Build [39530803846](https://github.com/snapetech-org/chaptarrng/actions/runs/39530803846) passed Linux, macOS, and PostgreSQL but failed one Windows path-normalization fixture before installer checks; the corrected focused fixture passes locally (8/8), and the exact-head Windows rerun is pending. CodeQL [39533337051](https://github.com/snapetech-org/chaptarrng/actions/runs/39533337051) is running; dependency submission [39533341590](https://github.com/snapetech-org/chaptarrng/actions/runs/39533341590), Semgrep [39533338188](https://github.com/snapetech-org/chaptarrng/actions/runs/39533338188), security analysis [39533338275](https://github.com/snapetech-org/chaptarrng/actions/runs/39533338275), and Trivy [39533338258](https://github.com/snapetech-org/chaptarrng/actions/runs/39533338258) passed. No release, package, image, installer, or migration bridge was published; operator-data, rollback, provider and SeerrNG workflows, installed-channel handoff, and operator acceptance remain open.
>
> The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `e3759f7a78d5ba35db73a7735dd79bbf84c12939`. It covers 732 post-fork commits (723 absent from pinned upstream history) and 1,119 changed paths: 83 reviewed mappings and 658 reviewed dispositions (177 retained, 132 equivalent, 177 ported, and 172 non-runtime retirements). Another 461 paths remain open (137 without mapped targets and 324 requiring semantic review). This pass dispositioned the ChaptarrNG Docker migration helper and its safety fixture, alongside the SeerrNG route-scoping middleware/context, configured extra-file rename, and media-import/replacement paths. The local helper checks and focused cross-platform fixture pass; exact-head Build is still running. Path-level coverage is not feature-parity proof, and no runtime retirement is approved.
>
> No release, tag, package, image, installer, or migration bridge was published. Keep BookshelfNG in service and do not start ChaptarrNG against BookshelfNG appdata. Issue [#144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open for representative data and rollback, semantic parity, provider workflows, installed channel handoff, and operator acceptance. Readiness variables remain unset. Historical validation notes below retain their original snapshot dates.

> Exact-head artifact repeat (2026-10-19): the Linux artifact from PR #131 Build [39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744) passed the checked-in SeerrNG Compose smoke with synthetic migrated audiobook and ebook records. Using SeerrNG rebuilt from `22f3bbc5874752b50a3b1206ca0bd3ebe0309f95`, it verified restricted-key access, administrative/unrelated command denial, and pending import create/poll/cancel. The candidate app artifact ran in a temporary image based on public `.977`; this did not validate candidate image packaging, successful acquisition, operator data, installed rollback, or channel handoff. Full details are in the [migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md#exact-head-artifact-repeat-2026-10-19).
> **Migration decision: keep BookshelfNG in service.** Do not apply the converter or start ChaptarrNG against BookshelfNG appdata; normal ChaptarrNG startup converts a supported source database automatically. A passing preview is not cutover approval. See the [migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md).
> BookshelfNG PR #154 improved empty-database selection in source `main`, but the fix is not in the published `.71` helper. The `.71` helper may print a zero-byte `readarr.db` as selected beside a populated `audioarr.db`; ChaptarrNG `.977` independently ignores empty legacy files when choosing its migration source. See the [migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md) for the version-specific behavior.
> A local AUR candidate passed isolated pacman upgrade/downgrade, package-level preview/conversion/restore, and an active systemd service upgrade and rollback against a synthetic populated migration-158 database. Real operator data and host-specific service settings remain open. The network-online wait was masked only inside the network-isolated test container.
> A Fedora 44 RPM transaction upgraded the published `.71` package to a local `.977` bridge candidate and downgraded back with config/data canaries. The run used `rpm --nodeps` and a mocked `systemctl`; it did not run a real service or migrate a database. The current `slskdn/bookshelfng` COPR repository has no package entries for Fedora 43, 44, 45, or Rawhide, so live COPR/DNF acceptance remains open.
>
> Prior ChaptarrNG PR #131 application-code validation: snapshot `0612cb4c90b75818e5349eb868cc0638825de02a` passed exact-head Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373): Linux, macOS, and Windows tests, PostgreSQL migration smoke, native-runner receipt reconciliation, and release-note contract passed. CodeQL [39239934583](https://github.com/snapetech-org/chaptarrng/actions/runs/39239934583), security [39239940344](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940344), NuGet submission [39239932165](https://github.com/snapetech-org/chaptarrng/actions/runs/39239932165), and dependency review [39239940313](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940313) passed. Disposable-fork validation [39239940512](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940512) was skipped by its external-fork gate. SeerrNG's adapter and request-route suite at source commit `b810153c` passed 4 files / 283 tests. The Linux artifact also passed the earlier empty-library API and authorization smoke. A populated source-build smoke on later code is recorded in the migration guide.
> Populated synthetic migration-to-SeerrNG smoke (2026-10-19): ChaptarrNG candidate `12f290bd` built through its checked-in `Dockerfile.build`, converted a disposable migration-158 database during normal startup, retained the source backup, and persisted `HardcoverEnabled=true` for `HARDCOVER=true`. SeerrNG `ReadarrAPI` at commit `fdc439aa9` read both migrated audiobook and ebook records and their Hardcover identities. Capability discovery, restricted-key authorization, and pending add/poll/cancel passed; the ChaptarrNG importer suite passed 43/43. The `.m4b`/`.epub` placeholders do not exercise media processing. A separate real-tool importer check passed all six synthetic multipart M4B cases on candidate `12f290bd`; Linux CI now runs it in a pinned tool image. Synthetic embedded-chapter tests now pass on the later candidate; representative audiobooks and restart/resume remain unverified. This is not operator-data, installed rollback, or channel acceptance. At the time of this smoke PR #131 was draft; it merged on 2026-10-20. Issue #144 and all release gates remain open, and no release or alias bridge was published. See the [migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md#populated-migration-to-seerrng-source-smoke-2026-10-19).
>
> Historical candidate CI: PR #131 head `38be9422a0390c0b3d4d1c453ec14b25d3aa99a4` added portable BookshelfNG BKSENC01 `.enc` backup import/export, cross-checked against BookshelfNG's source implementation. Its exact-head Build [39267876585](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876585) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. CodeQL [118112421054](https://github.com/snapetech-org/chaptarrng/runs/118112421054), security analysis [39267876503](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876503), and dependency review [39267876754](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876754) passed; disposable-fork validation was skipped by its external-fork gate. The merged source and latest exact-head validation are recorded above. The release freeze and retirement gates remain in force.
>

>
> M4B validation update (2026-10-19): ChaptarrNG PR #131 commit
> `c4fa8125095f583ad9eee534f70328e8eef1b44c` fixes Move-mode cleanup after a
> successful profile-based multipart merge. Embedded-chapter tests first exposed
> that source tracks remained; fixture isolation alone did not resolve it.
> Exact-head Build
> [39288736177](https://github.com/snapetech-org/chaptarrng/actions/runs/39288736177)
> passed Linux's full suite and pinned-tool M4B checks, PostgreSQL migration
> smoke, and release-note contract. Windows build and full test steps passed. The macOS job was cancelled before a runner started, so the cross-platform matrix is incomplete. CodeQL, security, dependency-review, and NuGet checks passed.
> Representative media, restart/resume, and operator acceptance remain open.
> No release or bridge was published.
>
> Prior exact-head ChaptarrNG PR #131 validation (2026-10-19): candidate
> `b7e900d49648269d5118bbfba44289c0200b095b` passed Build
> [39292223717](https://github.com/snapetech-org/chaptarrng/actions/runs/39292223717)
> on Linux, macOS, and Windows. PostgreSQL migration smoke, release-note
> contract, native-runner receipt reconciliation, and the Linux pinned-tool
> M4B smoke passed. CodeQL, security/secret scan, dependency review, and NuGet
> submission passed; disposable-fork validation was skipped by its gate. This
> is code validation only; representative data, parity, installed rollback,
> and channel acceptance remain open. No release or bridge was published.
> The prior docs-only PR #131 head was commit
> `93213b677a0bbb256aaf782c389a4f1a3d9c2ee7` on top of application-code commit
> `0e881d921dd55aa89e12747557ccaadbb2352a21`. Exact-head Build
> [39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744)
> passed Linux, macOS, Windows, PostgreSQL migration, release-note contract,
> and native-runner receipt reconciliation in full attempt 3. The
> application-code Build
> [39313568727](https://github.com/snapetech-org/chaptarrng/actions/runs/39313568727)
> passed on Linux, Windows, and macOS, including PostgreSQL migration,
> release-note validation, native-runner receipt reconciliation, and Linux
> pinned-tool M4B checks; CodeQL, security/dependency, dependency-review,
> NuGet, analysis, and Helm identity checks passed too. Disposable-fork
> validation was skipped by its external-fork gate. This is code validation
> only. At that checkpoint PR #131 remained draft; representative-data acceptance, semantic
> parity, installed rollback, and channel handoff remain open. No release or
> bridge was published.
>
> Follow-up request lifecycle probe (2026-10-19): then-draft ChaptarrNG PR #131 commit `d97136040e5f76f6aa0b140d5c0ed74f8de7501e` added [`integration/seerrng-request-lifecycle.mjs`](https://github.com/snapetech-org/chaptarrng/blob/d97136040e5f76f6aa0b140d5c0ed74f8de7501e/integration/seerrng-request-lifecycle.mjs), wired into `integration/seerrng-smoke.compose.yml`. It passed against the prebuilt Linux candidate `0.9.978.0` from Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373) (application snapshot `0612cb4c90b75818e5349eb868cc0638825de02a`) and SeerrNG source `b810153c`: the real `ReadarrAPI` adapter created, polled, and cancelled a synthetic unavailable-author import, and ChaptarrNG returned terminal `Failed` / `Cancelled by user`. `node --check`, Prettier, and Compose configuration validation passed. The earlier Compose run used a temporary runtime image. A follow-up source-build run on 2026-10-19 built through the checked-in `Dockerfile.build` from ChaptarrNG PR #131 head `7cfb5d87` and passed both scripts after the harness prepared its disposable `/books` volume as UID/GID `99:100`. Successful fulfillment, retries, availability/history, converted records, saved operator settings, and operator acceptance remain open. This proves the synthetic cancellation path only; successful fulfillment, retries, availability/history, converted-record behavior, unchanged production settings, and operator acceptance remain open.
> On 2026-10-19, unpublished candidate build `0.9.978.0` passed migration preview, explicit apply, rollback preview, and explicit rollback against a task-scoped copy of populated migration-158 SQLite data with `HARDCOVER=true`. The live BookshelfNG service remained running; candidate commands targeted only the separate copy, and network access was not blocked for those commands. The restored source matched its retained backup byte-for-byte, the converted database was retained separately, and integrity/foreign-key checks passed. Unresolved books were preserved in both catalogs as unmonitored with a private review sidecar; their media types still need review. Every migrated author, book, and edition retained its native Hardcover identity. This is one populated SQLite rehearsal, not approval to migrate installations; older schemas, PostgreSQL operator data, parity, and installation-channel acceptance remain open. No private library counts or identifiers are published. See the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/8b4c6e23/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md) and [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131).
> A separate copy-only rehearsal against populated operator SQLite data with native Hardcover mode passed preview, apply, restore preview, and rollback. Preview left the source copy unchanged; restore preview left the converted database and retained source backup unchanged; rollback restored the retained backup byte-for-byte and preserved the converted database separately. Integrity and foreign-key checks passed. This does not close ambiguous-media review, older-schema or PostgreSQL operator-data validation, feature parity, or installation-channel acceptance.
> The `.978` Linux app artifact from Build [39267876585](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876585) also started against a fresh converted schema-121 copy using the published `.977` runtime image, empty scratch mounts for configured media roots, and an internal-only network. `/ping` returned HTTP 200. This verifies app startup with converted data, not candidate image packaging or a live installation switch.
> The published ChaptarrNG `.977` importer maps bare numeric IDs to Goodreads even if BookshelfNG used native Hardcover mode. Do not apply `.977` to a native Hardcover database; its preview cannot detect this identity mismatch. The merged, unreleased source implementation uses explicit provider mode.
> At an earlier candidate checkpoint, BookshelfNG source snapshot 6e1a62e12 and ChaptarrNG code snapshot 8b4c6e23 included the Editions and Narrations tab and series narrator comparison. That checkpoint passed Build 39205452341, CodeQL 39205449712, dependency review, security, NuGet, and release-note checks. These are prior-head results; merged source status and latest exact-head validation are summarized above. Public ChaptarrNG .977 predates the catalog UI. BookshelfNG issue #114 is closed, and ChaptarrNG v0.9.974+ initializes new-author format paths from configured defaults.
> A local SeerrNG Compose smoke passed against ChaptarrNG PR #131 source head `ddec3e81` (application-code snapshot `2c0401fc`) and SeerrNG `10f06eab9`. It verified capability discovery, empty paged-library access, and restricted-key denials for administrative and unrelated commands. This is API/key evidence only; populated migrated data and end-to-end SeerrNG workflows remain open.
> Merged ChaptarrNG source includes format-aware, previewable single and bulk moves of registered media and linked book sidecars. It resolves sidecars from the linked book format root, rejects relative paths outside the author folders, stores moved paths relative to the destination format root, and leaves untracked files and author-wide extras in place. The media-move implementation passed Windows testing after commit 2c0401fc replaced POSIX-only fixture paths; application-code snapshot `0612cb4c` passed all platform suites on Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373). Representative-library, cross-device, and partial-failure acceptance remain open; the change is in merged source but not released.
> Provider settings are copied only when ChaptarrNG has a matching implementation, contract, and saved settings fields. Merged, unreleased ChaptarrNG source includes BookshelfNG's Hardcover public-list/reading-status provider and compatibility ports for Goodreads OAuth bookshelf and owned-book lists and write notifications. Complete existing OAuth settings are retained; preview blocks missing or partial credentials and does not print their values. Public shelves can remain unauthenticated when a valid numeric user ID is saved. Goodreads API acceptance with existing credentials is still unverified, and Goodreads no longer issues new developer keys. These changes are not in published ChaptarrNG `v0.9.977`; keep the release freeze and BookshelfNG service in place. See the [Goodreads API deprecation notice](https://www.goodreads.com/topic/show/21788520-api-deprecation) and the [operator migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md#provider-configuration-before-migration).

The ChaptarrNG PR #131 application-code snapshot `0612cb4c` also ports the native Hardcover provider, maps saved HardcoverAuth to HardcoverApiToken, preserves bare numeric IDs according to source HARDCOVER mode, and fails closed when mode is unset or invalid. The candidate includes provider-mode image targets for Bookshelf aliases, but no legacy alias bridge has been published or enabled. These changes are not in the published .71 helper or ChaptarrNG .977 image. Earlier exact-head run 39175250100 passed platform, PostgreSQL, security, and release-contract checks; its final Linux artifact passed synthetic provider-mode and rollback checks. Current-head results are listed above. Converted-data and installed rollback acceptance remain open. Keep the release freeze in place.

BookshelfNG's tagged image/release jobs, manual distribution retries, and the
ChaptarrNG legacy bridge are also fail-closed. They require the
`BOOKSHELFNG_RELEASE_READY=true` repository variable, which is unset. Keep it
unset until migration, parity, rollback, and channel acceptance are complete.

[![.NET 10 LTS](https://img.shields.io/badge/.NET-10%20LTS-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/en-us/platform/support/policy)

BookshelfNG is a self-hosted ebook and audiobook library manager descended
from Readarr. Follow authors and books, monitor indexers for new releases,
automatically grab downloads, and organize, rename, and upgrade files in your
library. BookshelfNG is a complete app on its own. It does not require SeerrNG
or a metadata proxy.

BookshelfNG is built on .NET 10 LTS.

Support BookshelfNG on [Ko-fi](https://ko-fi.com/snapetech).

Published containers and native release
archives include the required runtime; source builds require the .NET 10 SDK.

BookshelfNG `0.4.21.71` is the final source release. Existing Unraid
installations should follow the
[BookshelfNG-to-ChaptarrNG migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md)
and keep an independent appdata backup. The BookshelfNG Community Apps template
has not yet switched images. New Unraid installations should use the
[ChaptarrNG Unraid template](https://github.com/snapetech-org/chaptarrng-unraid),
which installs the standard maintained application.

BookshelfNG is for people who want Readarr-style book automation with a choice
of metadata providers. Goodreads-compatible metadata services and native
Hardcover remain available for primary library refreshes. Runtime catalog
search is independently selectable across those providers, Open Library, and
the other public catalogs. See [Metadata sources](#metadata-sources) for
provider behavior and settings.

For local MCP access, see the [SnapeTech MCP integration guide](docs/integrations/snapetech-mcp.md).

## One instance for ebooks and audiobooks

A single BookshelfNG instance and database can track ebooks and audiobooks on
the same author and book records. You do not need separate BookshelfNG
instances just to support both formats. When SeerrNG routes ebook and
audiobook requests separately, both service entries can point to this same
BookshelfNG URL and API key.

Each author keeps the existing `Path` as the default, with optional ebook and
audiobook folder overrides for future imports, upgrades, and renames. Changing
an override alone does not move existing files. In the author editor, use
**Move existing ebooks** or **Move existing audiobooks** to preview and queue a
move for one author. To move one format for several authors, open the author
library, choose **Author Editor**, select authors, then choose **Move selected
media**. Both workflows are also available through the
[API and CLI](docs/media-storage.md).

A move includes only media files and book sidecars registered in the current
instance. It does not sweep unknown files, move author-wide extras, or merge a
second instance's catalog or database. Bulk previews show each destination,
missing files, conflicts, and estimated copy space; any conflict prevents the
batch from being queued. A queued move runs in the background and is not an
all-or-nothing transaction, so review its progress in **Activity → Queue**.
Move actions require the instance's administrator API key. BookshelfNG has no
separate in-app administrator and regular-user roles.

For a legacy ebook/audiobook setup with two BookshelfNG instances, move each
instance's tracked format from that source instance, then import or rescan the
files in the instance you are keeping. Keep both source databases until the
files have been moved and verified: BookshelfNG does not merge their author,
book, profile, monitoring, or history records. The full
[legacy consolidation runbook](docs/media-storage.md#consolidating-a-legacy-two-instance-library)
covers destination mounts, backups, the UI/API/CLI steps, and follow-up import.
Quality and metadata profiles have optional ebook and audiobook overrides;
each format falls back to the author's shared profile when its override is
unset. Separate instances remain an option for isolated databases or settings.
See the [feature inventory and ChaptarrNG retirement
matrix](docs/maintainers/bookshelfng-parity-roadmap.md) for current parity and
migration status.

### ChaptarrNG consolidation status

The final BookshelfNG release includes a source-side helper that archives the
entire appdata directory before it calls the standard ChaptarrNG preview,
apply, or rollback command. ChaptarrNG `v0.9.977` remains the latest public
release. Its converter supports the final migration-158 SQLite schema and
bundles the BookshelfNG source migration chain, but rejects versions before
migration 14 because their table is still named `Blacklist`. PR #126 merged a
version-aware guard and migration-1 rollback fixture into ChaptarrNG `main`;
hosted Linux, macOS, Windows, and PostgreSQL migration checks passed. This
source fix is not available in `.977`. ChaptarrNG releases are frozen until
feature parity, representative data migration and rollback, and channel
acceptance are complete. Populated synthetic migration-22 tests cover
conversion and rollback, but older-schema behavior on real data is not
established. A separate private populated migration-158 SQLite snapshot also
passed preview, apply, and rollback with the public .977 Linux image. Preview
left the source unchanged, and both backups passed integrity and foreign-key
checks. Ambiguous media choices remain for human review, and this does not
establish older-schema, PostgreSQL, feature-parity, or channel acceptance.
PostgreSQL source conversion remains unsupported. If the source
does not identify a format, ChaptarrNG preserves the work in both catalogs
without monitoring and writes a private review file. This keeps conversion
moving without guessing which format to search.

ChaptarrNG PR #128 merged release and distribution workflows that fail closed
unless `CHAPTARRNG_RELEASE_READY=true`; the repository variable remains unset.
The current `.978` source version bump is not a published release. ChaptarrNG
PR #127 merged as `b3089a39` and adds selectable supplemental catalogs,
per-field metadata preferences, and exact-identity recovery for unmapped files.
Its cross-catalog fallback queues a reviewable pending-author import and never
attaches a file directly. Exact-head hosted validation passed; provider/settings
migration and behavior on converted operator data remain open.

ChaptarrNG PR #129 merged to `main` as `949ae3dd`. The source now includes the
opt-in BookshelfNG M4B merge settings, tagged track ordering and chapter
titles, original-track fallback, and source cleanup only after a successful
move-mode import; copy mode retains the originals. The clean head passed the
full hosted Linux, macOS, and Windows suites, PostgreSQL migration validation,
CodeQL, dependency/security, and release-note checks. A synthetic two-track
smoke using the `.977` image's m4b-tool preserved the supplied chapter titles
and offsets and produced AAC at 44.1 kHz stereo, about 128 kbps. It validates
the external tool and sidecar format. The then-draft ChaptarrNG PR #131 candidate at commit
`bdd7518f` added a six-case tool-enabled synthetic importer smoke that passed
locally in an isolated Linux container with `m4b-tool` 0.5.2, `mp4v2` 2.1.1,
and FFmpeg/FFprobe 6.1.1. Successful cases check tagged order, chapter titles
and offsets, metadata, registration, and Move/Copy source handling. Failure
cases check fallback to separate original-track imports in both modes when
FFprobe cannot read a source and when `m4b-tool` fails after a controlled
FFmpeg conversion error. Synthetic embedded-chapter tests pass on c4fa; representative M4B media and restart/resume remain open. The feature is not in public
`.977`; keep `BOOKSHELF_M4B_MERGE` unset after migration until the remaining
acceptance gates close and a release containing it is available.

ChaptarrNG PR #130 merged to `main` as `9f1ae60b`. When no explicit
`BookMatchingStrictness` exists, it maps BookshelfNG's numeric
`BookImportMinimumMatchPercent` to the closest mode: 50–66 to Aggressive,
67–82 to Balanced, and 83–99 to Strict. Explicit Chaptarr settings take
precedence; invalid legacy values fail closed; and the raw BookshelfNG row is
retained while the report calls out the lossy approximation. The matching
algorithms differ, so converted-library behavior still needs acceptance. This
source change is not in public `.977`.

The helper does not copy media or download folders mounted outside appdata,
translate every environment setting or external service, or update a pinned
image or package on its own. Keep the same media/download mounts where possible,
back up external settings separately, and follow the
[migration guide](docs/migrate-from-bookshelfng-to-chaptarrng.md). PostgreSQL,
full feature parity, and several package-channel upgrade and rollback paths
remain unverified. The disabled-by-default release bridge
does not change live tags or packages until its independent acceptance gates
pass. The [consolidation report](docs/maintainers/chaptarr-consolidation.md)
records current evidence and open gates. The
[ChaptarrNG retirement status](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md)
lists the current channel state and acceptance items.

The final source release also clears its frontend dependency audit. The local
`braces` toolchain patch and the full Yarn and .NET audit commands are
documented in [Dependency security](docs/maintainers/dependency-security.md).

Retiring BookshelfNG into ChaptarrNG is a separate gate from any later
ChaptarrNG retirement. Every BookshelfNG capability carried into ChaptarrNG
then joins the upstream blocker set alongside all features ChaptarrNG maintains
or is actively adding, including unpublished work in progress. That complete
union blocks ChaptarrNG retirement as a whole. Active ChaptarrNG branch and
pull-request features count before release; the matrix records the current
snapshot and individual gates. See the
[combined ChaptarrNG retirement matrix](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers).

## Capabilities

- **Choose how book metadata is served.** The `hardcover` image includes a
  native Hardcover GraphQL provider. Search, author, work, edition, series,
  ISBN, and ASIN lookups go from BookshelfNG directly to Hardcover. There is
  no proxy between them. When you need one, BookshelfNG can use a
  Readarr-compatible metadata endpoint instead, including a service you host
  yourself.
- **Keep old libraries usable.** The `softcover` image retains Goodreads
  compatible IDs and import behavior for existing Readarr/softcover databases.
  You can also choose a compatible metadata endpoint with `METADATA_URL`.
- **Identify ebooks from their own metadata.** BookshelfNG reads identifiers
  embedded in ebook files, strips ISBN formatting, validates ISBN-10 and
  ISBN-13 check digits, and prefers ISBN-13 when an ebook provides multiple
  valid identifiers. ISBN and ASIN are also used for direct metadata searches
  and edition matching.
- **Control catalog search timing.** The Add page waits for you to submit a
  search by default. Enable search-as-you-type when you want results as you
  enter a query; the preference is saved in the current browser.
- **Find and compare likely releases.** Import identification searches by
  ISBN, ASIN, and Goodreads ID before using author and title. If author
  information is missing, it can search by title alone. Candidate editions
  are ranked using identifiers and available edition details; ambiguous
  matches can still need review. Search result ordering is preserved.
- **Keep multiple formats for a book.** Different ebook formats and audiobook
  files can stay attached to the same book. Import and upgrade decisions only
  compare compatible formats; see [import matching and format support](docs/import-matching-and-formats.md).
- **Import common ebook and audiobook formats.** Recognized ebooks include
  EPUB, KEPUB, MOBI, AZW3, and PDF. Audiobooks include M4B, MP3, FLAC, AAC,
  M4A, OGG, and related formats; see the [complete extension list](docs/capabilities-and-compatibility.md#supported-file-formats).
- **Tune edition matching and series names.** Metadata profiles can rank
  edition title, format, and publisher terms, and choose preferred series for
  filenames and metadata. See [import matching and format support](docs/import-matching-and-formats.md).
- **Organize books for Jellyfin.** Jellyfin's Books library expects each book
  in its own folder. Enable **Rename Books** and use a book-title folder in
  **Standard Book Format**; see the [Jellyfin folder layout guide](docs/import-matching-and-formats.md#folder-layout-for-jellyfin-books-libraries).
- **Import books from the lists you use.** BookshelfNG supports Goodreads
  shelves, owned books, series, and Listopia lists, plus native Hardcover list
  imports. Hardcover imports honor the lists selected in configuration.
- **Search MyAnonamouse directly.** The native MyAnonamouse indexer lets you
  use the tracker without adding Prowlarr as an intermediary.
- **Connect current download clients.** BookshelfNG supports qBittorrent 5.2
  authentication alongside the download clients inherited from Readarr.
- **Build chaptered audiobook files when needed.** Completed downloads with
  multiple tracks for one edition can be merged into a single M4B when
  `BOOKSHELF_M4B_MERGE=true` and an FFmpeg executable is available. This is
  opt-in; the standard Docker image includes FFmpeg.
- **Keep the familiar automation.** Monitor authors and books, watch indexer
  RSS feeds for releases, search for missing monitored books, apply quality
  and metadata profiles, manage download clients, scan and import existing
  files, and rename or upgrade releases automatically. Optionally move
  configured extra files when author renaming moves books to a new folder; see
  [sidecar rename behavior](docs/capabilities-and-compatibility.md#renamed-book-sidecar-files).
- **Search and recover downloads.** Use interactive release search to choose
  an available release when an indexer supports it. BookshelfNG can search
  again after a failed download; automatic grabs and manually selected grabs
  have separate re-search settings. You can adopt a matching torrent already
  in a download client, and ignore an unmatched queue item without deleting
  the download. For supported ebook sources, add the built-in **Direct
  Download** indexer. It uses an API key when configured and can optionally
  resolve slow links in headless Chromium; its built-in client tracks the
  transfer without another download-client service. Direct search is
  interactive and does not provide RSS. See
  [search and download workflows](docs/search-and-downloads.md).
- **Use narrator credits to identify audiobooks.** Import matching compares
  narrator tags with edition metadata when both are present. Narrators stay
  separate from authors, appear in book search and filtering, and can be
  written to audio files when audio tag writing is enabled. See
  [audiobook metadata](docs/audiobookshelf-metadata.md).
- **Send imports to BookLore.** BookLore is an optional supported app. Add it
  as a notification destination to upload imported files to its BookDrop
  review queue; BookshelfNG runs without BookLore. See the
  [BookLore integration guide](docs/booklore-integration.md). During a
  ChaptarrNG migration, this saved connection remains configured for BookLore;
  it is not automatically rewritten to BookOrbit. See the
  [migration handoff](docs/migrate-from-bookshelfng-to-chaptarrng.md#booklore-and-bookorbit-handoff).
- **Connect a Calibre Content Server.** Configure a Calibre library as a root
  folder to add imported books to the library, sync metadata, and convert into
  configured output formats.
- **Keep library activity private.** BookshelfNG removes Servarr's Sentry
  analytics and exception-reporting integration. An independent diagnostics
  module is available for operators who explicitly install and enable it; the
  standard app image contains no reporting module or telemetry SDK.

BookshelfNG retains the Readarr-compatible API and the broader Readarr
library-management workflow. A book can keep multiple ebook formats and
audio files in one instance; import and upgrade checks keep those formats
separate. See [import matching and format support](docs/import-matching-and-formats.md).

Some capabilities are part of the Bookshelf and Readarr lineage rather than
unique BookshelfNG additions. The [capabilities and compatibility guide](docs/capabilities-and-compatibility.md)
compares those upstream features with BookshelfNG's maintained changes and
documents provider boundaries, migration limits, and implementation links.

Author and book metadata are persisted in BookshelfNG's application database.
Refreshing a book for an author already in the library reuses that local author
record when the provider IDs match, so a book refresh does not need to fetch the
author's full catalog again. Automatic author validation is age and activity
based; manual refreshes and metadata-profile changes can force an update. See
[Author metadata storage and refresh behavior](docs/author-metadata-refresh.md)
for the exact rules, Hardcover request caching and rate-limit behavior, failure
handling, troubleshooting logs, and source-code references.

## Quick start

For a normal Docker install, use the published image below. You do not need to
clone the source repository or run `build.sh`; the image already contains the
backend and web UI. Save the example as `compose.yaml` in an empty directory.

The web interface listens on port `8787`. Persist `/config`, and mount your
downloads and library paths so BookshelfNG and your download clients can
access them.

```yaml
services:
  bookshelf:
    image: ghcr.io/snapetech/bookshelfng:hardcover
    ports:
      - "127.0.0.1:8787:8787"
    volumes:
      - ./bookshelf-config:/config
      - /path/to/downloads:/downloads
      - /path/to/books:/books
    restart: unless-stopped
```

Run `docker compose pull` and `docker compose up -d`, then open
`http://localhost:8787` to set up your root folder, metadata source, indexers,
and download clients. The
`softcover` image is available for Goodreads-compatible libraries. Both
published Linux images support `amd64` and `arm64` hosts.

## Standalone app

BookshelfNG also runs directly on Windows, macOS, Linux, and FreeBSD. Native
release archives include the .NET runtime and web UI; they do not require
SeerrNG or a container runtime. Start an extracted Linux, macOS, or FreeBSD
archive with:

```sh
./Readarr -nobrowser -data="$HOME/.local/share/bookshelfng"
```

On Windows, run `Readarr.exe` and set a persistent data path under
`%LOCALAPPDATA%`, or use the Windows x64 setup installer attached to each
release. The installer registers BookshelfNG as a service and backs up the
existing Readarr-compatible data before upgrades. Then open
`http://localhost:8787`. The
[standalone installation guide](docs/standalone-install.md) covers platform
archives, data migration, system services, and package-specific setup.

The release pipeline builds `.deb`, RPM, Flatpak bundle, AppImage, and Helm
artifacts, and supports AUR, COPR, Ubuntu PPA, and Chocolatey publishing when
those publisher accounts are connected. See the
[distribution channels guide](docs/distribution.md) for package links,
repository setup, and release details.

## Optional audiobook M4B merging

To combine a multi-track audiobook download into a single chaptered M4B, set
`BOOKSHELF_M4B_MERGE=true`. This applies to completed downloads received from a
download client. BookshelfNG groups approved tracks by book and edition,
orders them using embedded disc and track numbers or filenames, creates a
chapter for each track, and reruns the normal import checks on the merged
file. If FFmpeg is unavailable, a merge fails, or the merged file fails import
checks, BookshelfNG keeps the original tracks and continues the normal import.

The standard Docker image includes FFmpeg. For native installs, provide an
executable named `ffmpeg` on BookshelfNG's `PATH`, or set
`BOOKSHELF_FFMPEG_PATH` to its path. The merge transcodes audio to stereo AAC
at 44.1 kHz and 128 kbps by default.
Set `BOOKSHELF_M4B_AAC_BITRATE_KBPS` to a value from 48 to 320 to choose a
different bitrate. When the merged file imports successfully in move mode,
the original tracks are removed; copy mode and downloads that cannot be moved
retain their source tracks. See the [capabilities and compatibility guide](docs/capabilities-and-compatibility.md#audiobook-m4b-merging)
for the exact behavior and implementation references.

ChaptarrNG's published `v0.9.977` does not honor these three BookshelfNG
variables. A source-only compatibility candidate is being validated; this
does not change the final BookshelfNG build or release. Keep the merge opt-in
disabled after migration until a tested ChaptarrNG build documents support.

## Metadata sources

### Hardcover: direct API access

The `hardcover` image uses BookshelfNG's native Hardcover GraphQL provider by
default. It searches Hardcover for books and authors and maps work, edition,
series, ISBN, and ASIN data into Bookshelf's existing metadata model. This
removes the extra metadata service from the normal request path.

Native access requires a Hardcover API token at runtime:

```env
HARDCOVER=true
HARDCOVER_AUTH=Bearer your-hardcover-api-token
```

`HARDCOVER_API_KEY` is accepted in place of `HARDCOVER_AUTH`. The default API
endpoint is `https://api.hardcover.app`; set `HARDCOVER_API_URL` to use a
compatible endpoint or test service. The Hardcover token can also be entered
in **Settings > Metadata > Primary Metadata Provider**. Environment credentials
take precedence over the saved setting; the settings API never returns the
saved token.

Native mode handles transient request failures and sparse or nullable metadata
responses, maps Hardcover work and edition records into Bookshelf's library
model, and caches responses in the BookshelfNG process for the lifetime of the
instance. Author responses are cached for 30 minutes, work responses for six
hours, and search responses for 10 minutes. These response caches are separate
from the author and book metadata stored in the library database. See the
[Hardcover API getting-started guide](https://github.com/hardcoverapp/hardcover-docs/blob/main/src/content/docs/api/Getting-Started.mdx)
and [Hardcover author schema](https://github.com/hardcoverapp/hardcover-docs/blob/main/src/content/docs/api/GraphQL/Schemas/Authors.mdx)
for Hardcover's API reference. BookshelfNG does not silently switch to another
metadata service after an API error.

When BookshelfNG creates the initial `Standard` metadata profile on a database
with no profiles, `HARDCOVER=true` selects a minimum popularity of 50; other
modes use 350. This lower default can keep more low-popularity catalog books
during refresh. Existing profiles are preserved and can be adjusted in the
metadata profile settings.

Text search fetches Hardcover's result IDs in one batched book query instead
of making a separate detail request for every result. ISBN/ASIN searches and
edition lookups fetch the parent work in the same GraphQL operation. API
requests are paced at one per second. BookshelfNG honors Hardcover's
`Retry-After` and exhausted rate-limit headers; when a limit is reached, it
stops sending further requests from this process until the reported reset and
returns an error for calls made during that cooldown instead of retrying into
the limit.

### Selectable runtime catalogs

Every provider used for runtime book discovery can be turned on or off
independently in **Settings > Metadata > Runtime Catalog Sources**. This
selection controls title, ISBN, ASIN, and import searches. It does not change
how existing library records refresh. Results from an alternate catalog retain
a provider-qualified ID and continue to resolve through that provider. Results
from the configured primary catalog keep its existing ID format so current
libraries continue to match them; older unqualified IDs also keep using the
configured primary provider.

The selectable sources are Hardcover, the configured Readarr-compatible
metadata API, Open Library, Google Books, Library of Congress, Gutendex,
Internet Archive, NDL Search, Europeana, and the Goodreads-compatible Apify
adapter. With no saved source selection, Bookshelf enables LOC, Gutendex, and
the currently configured primary provider. Open Library, Internet Archive,
NDL Search, and Apify are opt-in. Google Books and Europeana are enabled when
their keys are set. Hardcover needs its API token. All sources can be disabled,
including the configured primary provider's catalog search.

Field-level metadata preferences are configured separately from catalog
search. Choose an enabled supplemental catalog for a book's title,
description, publisher, language, release date, page count, cover, genres, or
author image. Edition details require a matching ISBN; work-level metadata
and images can also use an exact title-and-author match.
See [capabilities and compatibility](docs/capabilities-and-compatibility.md#per-field-metadata-source-preferences).
Use [catalog metadata composition and unmapped-file recovery](docs/catalog-metadata-and-unmapped-files.md)
to retry old no-match files in the UI, API, or CLI.

`BOOKSHELF_METADATA_SOURCES` accepts `hardcover`, `metadata-api`,
`openlibrary`, `googlebooks`, `loc`, `gutendex`, `internetarchive`, `ndl`,
`europeana`, and `apify-goodreads`. A custom value replaces the saved UI
selection; an empty value disables all runtime catalog searches. The
environment setting remains authoritative and disables catalog selection in
the UI. Saved credentials are stored in the BookshelfNG configuration database
and returned as presence flags only. Non-empty credential environment values
take precedence over saved values.

```env
HARDCOVER=true
HARDCOVER_AUTH=Bearer your-hardcover-api-token
GOOGLE_BOOKS_API_KEY=your-google-books-api-key
EUROPEANA_API_KEY=your-europeana-api-key
```

With these keys, Google Books and Europeana results are also queried alongside
the other selected sources. Library of Congress and Gutendex run without keys. Gutendex covers
Project Gutenberg's literature catalog, including multiple languages, and is
not a current commercial-book catalog. Google Books and Europeana are skipped
when their keys are absent. To keep only the default public catalogs, set
`BOOKSHELF_METADATA_SOURCES=loc,gutendex,openlibrary`; to disable all catalog
searches, set
`BOOKSHELF_METADATA_SOURCES=`.

Open Library can be enabled in **Settings > Metadata > Runtime Catalog
Sources**. It uses its public Search, Work, Edition, and Author APIs. Requests
identify BookshelfNG with its User-Agent, are paced to one per second, and are
cached for one day. Add a contact email in the same settings page or set
`OPEN_LIBRARY_CONTACT_EMAIL` so Open Library can identify the installation.
Open Library Work IDs and Author IDs stay namespaced in BookshelfNG, and its
edition mapping validates and normalizes ISBN-10 values to ISBN-13. Covers are
loaded from Open Library's Covers API when available. Read Open Library's
[API usage policy](https://openlibrary.org/developers/api),
[Search API](https://openlibrary.org/dev/docs/api/search), and
[Covers API](https://openlibrary.org/dev/docs/api/covers) documentation.

Internet Archive searches its text collection and resolves records by stable
item identifier. Catalog records and edition metadata vary, so treat it as an
optional fallback. NDL Search adds Japanese and partner-library metadata; it
does not provide artwork because NDL ended its thumbnail service on March 31,
2026. It is opt-in because requests are paced to one per second and usage
conditions vary by provider. Operators must show NDL Search API credit and
check the provider's licensing/application requirements, especially for
commercial or continuous use. See NDL's [thumbnail service notice](https://ndlsearch.ndl.go.jp/news/20260401_thumbnail).

To add a Goodreads-compatible Apify Actor:

```env
# Include only the providers you want; use metadata-api instead of hardcover
# when the Readarr-compatible metadata API should be searched.
BOOKSHELF_METADATA_SOURCES=hardcover,googlebooks,loc,gutendex,internetarchive,ndl,europeana,apify-goodreads
HARDCOVER_APIFY_GOODREADS_ACTOR=publisher~goodreads-scraper
HARDCOVER_APIFY_TOKEN=your-apify-token
# Override only when the Actor does not use searchQueries and maxItems:
HARDCOVER_APIFY_GOODREADS_INPUT_TEMPLATE={"searchQueries":[{{query}}],"maxItems":10}
```

Google Books public searches require a Google API key; user OAuth is not
needed. Europeana requires a free key from a registered account and searches
text records with open reuse status. It is a cultural heritage index rather
than a complete current-book catalog, and per-record metadata and cover
availability vary. See Europeana's [Search API documentation](https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812/Search+API+Documentation),
[Record API documentation](https://europeana.atlassian.net/wiki/spaces/EF/pages/2385674279/Record+API+Documentation),
and [API key registration](https://pro.europeana.eu/page/get-api). Library of
Congress search is public and rate limited. Requests are paced to one per 3.2
seconds per Bookshelf process and successful responses are cached for one day.
If multiple Bookshelf processes share an outbound IP, set a source list that
avoids querying LOC from every process. The optional Apify adapter runs a
user-selected Actor, whose schema, availability, terms, and pricing are
controlled by its publisher. The default Actor input is
`{"searchQueries":[{{query}}],"maxItems":10}`; a custom JSON template must
include the literal `{{query}}` placeholder, which Bookshelf replaces with a
JSON-escaped search string. Actor output is normalized from common Goodreads
scraper fields, and results missing a title or author are skipped.

Results from alternate providers receive a namespaced foreign ID such as
`hardcover:123`, `metadata-api:123`, `openlibrary:OL...W`,
`googlebooks:volume-id`, `loc:<encoded-record-url>`,
`europeana:<encoded-record-id>`, or `apify-goodreads:<encoded-record-key>`.
Bookshelf uses those same IDs for subsequent book and author metadata lookups;
it does not coerce them into numeric Goodreads IDs. The selected provider
names and credentials must remain
available when the library is refreshed. Search results are cached for 10
minutes; Open Library, Google Books, LOC, and Europeana responses and Apify
result sets are cached for one day. Provider failures are logged independently;
other configured sources continue to return results.

The source checkboxes and optional credentials are managed separately by each
BookshelfNG instance. If you choose to run separate ebook and audiobook
instances, configure each in its own **Settings > Metadata** page.
`HARDCOVER_NATIVE`,
`METADATA_URL`, and `HARDCOVER_API_URL` still select deployment mode or an API
endpoint and remain environment-level settings. SeerrNG's **Settings >
Metadata** page explains this boundary; its TMDB/TVDB selectors control video
metadata, not BookshelfNG catalogs. One-off SeerrNG migration-recovery adapters
also keep their own environment settings because they run outside BookshelfNG's
normal search process.

The source setting applies to the `hardcover` and `softcover` images. It does
not rewrite IDs already stored in the library, and it does not combine remote
catalog records into Hardcover itself.

### Goodreads-compatible metadata and proxies

The `softcover` image is intended for Goodreads-compatible metadata and
existing Readarr/softcover databases. Goodreads and Hardcover use different
foreign author, book, and edition IDs; those IDs cannot be converted by
changing an image tag or metadata URL.

BookshelfNG also supports the Readarr-compatible metadata API through
`METADATA_URL`. Use a hosted service such as rreading-glasses, preserve an
existing proxy or cache, or run your own compatible endpoint. In the
`hardcover` image, set `HARDCOVER_NATIVE=false` to select this compatibility
path instead of direct Hardcover GraphQL access. The choice is explicit, so
you can see which service is handling metadata requests.

`METADATA_URL` is a compatibility boundary, not an automatic multi-provider
aggregator. It can point to a service that itself translates or combines
providers, but BookshelfNG expects that service to return stable IDs and
compatible detail responses. Goodreads work and edition IDs, Hardcover IDs,
Google Books volume IDs, Open Library keys, and LOC identifiers are not
interchangeable. The optional runtime catalogs documented above provide
parallel search results and provider-specific detail lookups; they do not
rewrite IDs already stored in the library or silently replace a failed primary
provider.

## Moving an existing library to Hardcover

Do not switch an existing Goodreads/softcover database to Hardcover by changing
only the image tag or `METADATA_URL`. The two providers' foreign IDs are not
portable, and a direct switch can leave existing authors, books, and editions
that Hardcover cannot resolve.

Back up the ebook and audiobook configuration directories before migrating.
SeerrNG includes a migration helper that can inventory the source database,
rebuild strict matches against a temporary Hardcover BookshelfNG target, and
optionally use a softcover endpoint to recover metadata for stale IDs. Its
deterministic local database fallback can preserve books that Hardcover still
cannot import. Those fallback entries, such as `local:ebook:1076`, are local
Bookshelf records rather than native Hardcover records.

SeerrNG's migration helper can additionally search Google Books and the
Library of Congress and can optionally call a user-selected Apify Actor that
scrapes Goodreads-compatible catalogs. These sources are used to recover
candidate metadata and attempt strict remapping to Hardcover. Unmatched
metadata can enrich the optional local fallback. This tooling does not add
Google Books, LOC, or Apify results to BookshelfNG's ordinary search/detail
flows. Apify Actors are third-party services with Actor-specific schemas and
potential charges; Goodreads does not issue new public developer API keys.

## BookshelfNG with SeerrNG

SeerrNG can connect to BookshelfNG as a Readarr-compatible ebook or audiobook
service. That integration is optional; BookshelfNG can monitor, download, and
manage a library without SeerrNG.

Use one BookshelfNG instance and its existing database for both SeerrNG service
entries. New installations require Forms authentication for the web interface;
SeerrNG should use an API key in the `X-Api-Key` header. Legacy Readarr clients
that send `?apikey=` remain supported; set `BOOKSHELF_ALLOW_API_KEY_QUERY=false`
to require header credentials. To give SeerrNG a
separate restricted key, set `BOOKSHELF_SEERRNG_API_KEY` from a Docker/Kubernetes
secret. That credential can read library/search/profile/root-folder data and
add or update authors and books, but it cannot change system settings, reset
the administrator key, or run arbitrary commands. Replace the secret and
restart BookshelfNG to rotate it. Existing global API keys continue to work.

BookshelfNG advertises a versioned SeerrNG capability contract and accepts the
format-scoped routes `/readarr/{gr|hc}/ebook/api/v1` and
`/readarr/{gr|hc}/audiobook/api/v1`, where the dialect matches the configured
metadata provider. Both routes use the same BookshelfNG library and
database; a second instance or a database merge is not required. See the
[SeerrNG integration and security guide](docs/seerrng-integration.md) for
trusted proxy, allowed-origin, API credential, and upgrade details.

For compatible book-add requests, BookshelfNG's
`/api/v1/book/lookup` response includes nested author and edition metadata when
it can resolve the requested book. Use the `softcover` image when retaining a
Readarr-compatible Goodreads database, or use the Hardcover migration process
above when moving to Hardcover metadata.

## Releases

GitHub Actions publishes these rolling and versioned container tags:

- `softcover` and `softcover-v<release-version>` for the Readarr-compatible
  metadata mode
- `hardcover`, `latest`, and `hardcover-v<release-version>` for native
  Hardcover mode

Tagged `main-v*` builds also publish a GitHub Release with curated release
notes, platform archives, the Windows x64 setup installer, checksums, and native
Linux packages, then announce the release to Discord. The AUR, COPR, PPA,
Chocolatey, and Helm channels use the same verified tag flow. External
stores require publisher credentials and repository registration. The Flatpak is
attached as a GitHub Release bundle and is not published to Flathub. See the
[distribution setup and publisher requirements](docs/distribution.md) for
channel details. Pull requests require a release-note fragment for user-facing
changes; internal-only work must be marked `release-note: none`. See
[`release-notes/README.md`](./release-notes/README.md) for the format and
preview command.

If an anonymous pull returns `denied`, the GHCR package may not be public yet;
you can also authenticate with package read access.

## Documentation

- [Documentation index](docs/README.md)
- [Fork feature inventory, upstream comparison, and compatibility boundaries](docs/capabilities-and-compatibility.md)
- [Import matching and multiple formats](docs/import-matching-and-formats.md)
- [Search, direct downloads, torrent adoption, and queue workflows](docs/search-and-downloads.md)
- [Audiobook narrator tags and Audiobookshelf sidecars](docs/audiobookshelf-metadata.md)
- [BookLore import uploads](docs/booklore-integration.md)
- [Series pack search](docs/series-pack-search.md)
- [Optional audiobook M4B merging](docs/audiobook-m4b-merging.md)
- [Metadata providers and configuration](#metadata-sources)
- [Moving an existing library to Hardcover](#moving-an-existing-library-to-hardcover)
- [Author metadata storage, refresh policy, and troubleshooting](docs/author-metadata-refresh.md)
- [Reporting issues and collecting useful logs](docs/reporting-issues.md)
- [.NET 10 source builds, including the UI and Linux x86/FreeBSD packages](docs/dotnet-10-platform-builds.md)
- [Standalone installation and platform support](docs/standalone-install.md)
- [Release distribution channels and publisher setup](docs/distribution.md)
- [Optional diagnostics module](src/Bookshelf.Diagnostics/README.md)
- [Release-note format and preview](release-notes/README.md)
- [SeerrNG migration metadata source matrix](https://github.com/snapetech-org/seerrng/blob/main/docs/using-seerr/bookshelf-metadata-sources.md)

## Support and contributing

Please file a GitHub issue or start a discussion for help. Contributions are
welcome, especially fixes and quality-of-life improvements.

After cloning, maintainers can run `scripts/install-package-sync-hook.sh` to
install the post-commit and pre-push Unraid sync hooks. Commits on `main`, and
pushes targeting `main`, sync the full application source and Unraid package to
the companion repository; a failed sync blocks the push. Syncs use a clean
temporary worktree and leave other companion checkouts untouched. GitHub
workflows verify the Unraid package before release. Missing package sources or
the companion checkout are errors. Set `BOOKSHELFNG_UNRAID_REPO` if that
checkout is outside the sibling-repository layout.

BookshelfNG no longer maintains, publishes, or updates a YunoHost package.
Existing installations remain on their last published version; operators
should move to a supported deployment or maintain their own package updates.

## Optional diagnostics

The standard BookshelfNG image sends no analytics or exception reports. An
optional module can report aggregated application-start, book-grab, book-import,
and download-failure counts to an OTLP collector you configure. It requires the
module assembly, an explicit enable flag, an HTTPS endpoint, and a bearer token.
It sends no book or author metadata, paths, search terms, log messages,
exception details, or persistent installation identifier. The collector can
still see the source IP address of the HTTPS request. See the
[diagnostics module instructions](src/Bookshelf.Diagnostics/README.md) for the
data schema and installation steps.

## Upstream and license

BookshelfNG is derived from [Bookshelf](https://github.com/pennydreadful/bookshelf),
a revival of [Readarr](https://github.com/Readarr/Readarr), and
[Prowlarr](https://github.com/Prowlarr/Prowlarr). Those projects are licensed
under GPLv3, and BookshelfNG is distributed under the terms of GPLv3. See
[LICENSE](LICENSE.md).

BookshelfNG is maintained as a fork because its standalone library model and
SeerrNG integration go beyond the current Bookshelf parent API. The upstream
Bookshelf README describes one type of a book per instance; BookshelfNG can
keep ebooks and audiobooks on the same book in one database, and exposes
format-specific availability and restricted SeerrNG access. Its parent is
reviewed in the [capability and compatibility guide](docs/capabilities-and-compatibility.md),
which records what is shared, what this fork maintains, and what would need to
be available before SeerrNG could replace it.

Copyright 2025–2026.

## Security scanning

Run scripts/security-scan-local.sh for local Semgrep Community Edition and applicable Trivy scans. Public GitHub Actions workflows run these scans on changes and weekly, alongside any existing CodeQL workflow. See docs/security-scanning.md for offline setup and updates. Run scripts/install-security-hooks.sh once to enable the staged Semgrep pre-commit hook.
