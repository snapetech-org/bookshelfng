# BookshelfNG feature inventory and ChaptarrNG retirement matrix

**Reviewed:** 2026-10-13. **Status:** the BookshelfNG-to-ChaptarrNG
consolidation is in progress; BookshelfNG is not ready to retire. The candidate
has no populated-library converter or release bridge. This is a feature-level
matrix, not a claim that similarly named features are equivalent.

**Confidence:** high for the listed BookshelfNG behavior at the pinned
released source; moderate for whether ChaptarrNG contains a related
implementation; unknown for semantic equivalence until the listed acceptance
checks pass.

## Retirement rule

Every capability BookshelfNG added or materially extended is a blocker to
retiring BookshelfNG until ChaptarrNG contains the behavior or a tested,
documented replacement. The set is conjunctive: closing one row does not close
the others. The whole enhanced BookshelfNG feature set blocks retirement, and
each row remains an independent blocker until its own evidence passes. A row
does not become optional because upstream documentation is silent or ChaptarrNG
has a feature with a similar name.

The default is to retain every capability. Calling a feature obsolete does not
close its blocker; any proposed removal requires an explicit maintainer
decision about the user impact.

This gate is separate from the later ChaptarrNG-to-Chaptarr gate. Once a
BookshelfNG capability is retained in the consolidated ChaptarrNG product, it
also joins ChaptarrNG's cumulative upstream-retirement blocker set. Every
ChaptarrNG feature it maintains or is actively adding—including work not yet
in a published release—joins that same set. The union blocks retirement as a
whole, with each capability and channel as an individual gate. Active
ChaptarrNG branches and open feature PRs count before release; the combined
[ChaptarrNG retirement matrix](https://github.com/snapetech/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers)
pins the current snapshot and tracks those blockers.

The current ChaptarrNG feature snapshot is pinned at `22078e0`: it records 315
commits ahead and zero behind `origin/main` at `a6be38d`, across 703 changed
paths. Later branch commits only update documentation. Draft PR #73 contains
the separate metadata-preference port; PR #72 adds Indonesian and Traditional
Chinese choices, AudioBookShelf mapping and audiobook-mode translations, and
locale direction metadata; PR #74 proposes removing YunoHost publishing. Each
capability and proposed distribution change is individually tracked in the
ChaptarrNG matrix, including work that has not merged or shipped.

## Feature matrix

“Present” means the target code has a related implementation. It does not
close the row until behavior, data, configuration, and client compatibility
are tested. The current code-level findings and acceptance cases are recorded
in the [consolidation report](chaptarr-consolidation.md); the linked inventory
is the commit/path audit that must be fully dispositioned.

| BookshelfNG capability | BookshelfNG has | ChaptarrNG candidate has | Retirement disposition and status |
| --- | --- | --- | --- |
| One instance for ebooks and audiobooks; multiple compatible formats per book | Single book records can retain multiple ebook and audiobook files | Media-specific book and edition models exist | **Open blocker.** Convert records and all relationships; prove format isolation, monitoring, upgrades, and existing client behavior. |
| Format-specific author paths, quality profiles, and metadata profiles | Optional per-format paths and profile overrides, with author defaults as fallback | Native media roots and profiles exist | **Open blocker.** Preserve override/fallback rules and prove imports, upgrades, renames, scans, and moves for both formats. |
| Native Hardcover metadata and request controls | Direct GraphQL provider, per-process pacing/cache, batched lookups, rate-limit recovery, and identity routing | Chaptarr has a separate resolver and consensus pipeline | **Open blocker.** Keep the configured behavior and identity boundaries or provide a tested replacement; a provider name alone is not parity. |
| Selectable supplemental catalogs and per-field source preferences | Hardcover, Readarr-compatible API, Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and optional Apify adapters | No matching Bookshelf catalog set or source-selection model identified | **Open blocker.** Port adapters, settings, qualified identities, field choices, and fallback rules, or replace each with tested behavior. |
| Cross-catalog recovery and import matching | Retry unmapped files across configured catalogs; ISBN/ASIN/provider-ID and normalized-name matching; configurable title threshold | Different resolver, FTS, and matching architecture | **Open blocker.** Port the observed cases and no-false-match/no-delete guarantees; do not transplant the old matching engine blindly. |
| Weighted edition terms, preferred series, and narrator-aware matching | Profile terms and series preferences; narrator tags and edition evidence affect audiobook ranking | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; stronger match evidence remains authoritative | **Partial candidate port; retirement blocker remains open.** Preserve weights and series choices, neutral handling of missing data, tie behavior, and manual-review boundaries; test the full Bookshelf edge-case set after profile/database conversion. |
| Audiobook M4B merge and chapter metadata | Opt-in multi-track merge with track ordering and chapter creation | Native conversion and multipart workflows exist | **Open blocker.** Verify opt-in policy, chapter offsets and source chapters, part order, tags, failure recovery, and source retention. |
| Vendored TagLibSharp MPEG-4 `chpl` handling | Patch includes byte-preserving chapter-list writes | Chaptarr uses a different TagLibSharp package | **Open blocker.** Compare exact patch behavior and prove chapter preservation on representative files before selecting a native patch or dependency update. |
| Existing torrent adoption and safe seeding | Can adopt tracked torrent data without removing the seed | Native adoption/continuation work exists | **Open blocker.** Prove same-category, wrong-category, completed-download, and seeding-data preservation cases. |
| Direct Download with ordered sources and browser-assisted links | Ebook search, API-key downloads, optional browser fallback, durable transfer state, and redirect validation | A built-in direct-download implementation exists | **Open blocker.** Preserve URL order, configuration aliases, staged-state recovery, architecture limits, and redirect/private-network protections. |
| BookLore BookDrop uploads | Uploads imported books through BookLore's BookDrop API | Ported in the current ChaptarrNG candidate | **Open blocker.** Core tests pass; convert stored notification settings and verify a service-level upload and recovery path. |
| Calibre, MyAnonamouse, Audiobookshelf sidecars, and SeerrNG integration | These standalone service and metadata workflows are present | Some native integrations and the SeerrNG contract exist; the full set is not proven equivalent | **Open blocker.** Disposition each integration and preserve its settings, API behavior, and stored associations. |
| Previewable media moves, bulk moves, and extra-file handling | Preview, collision checks, registered sidecars, and format-aware paths | Chaptarr has different folder and organization behavior | **Open blocker.** Prove equivalent previews, collision and cross-device behavior, and that unknown/external files remain untouched. |
| Optional privacy-preserving diagnostics | Separate module, explicit opt-in, aggregate-only event schema | No equivalent optional module identified | **Open blocker.** Retain its install/opt-in and data-minimization contract or record a reviewed replacement with the same operator choice. |
| Scoped SeerrNG access, API aliases, proxy and request controls | Restricted key, compatibility routes, format-specific availability, and hardened proxy/auth boundaries | ChaptarrNG has its own facade and scoped key | **Open blocker.** Preserve existing permissions and configuration semantics; test unchanged SeerrNG settings, IDs, keys, and proxy deployments. |
| Encrypted backups and restore | Passphrase-protected portable archives and per-format profiles | ChaptarrNG has encrypted backup support | **Open blocker.** Prove legacy archive recovery, secret handling, rollback, and profile conversion; never expose secrets in logs. |
| .NET 10, dependency/security fixes, and platform builds | .NET 10 releases, broad native/package matrix, and maintained security/dependency patches | ChaptarrNG uses .NET 10 and has a different dependency/build matrix | **Open blocker.** Review every patch and supported platform; retain compatible fixes and run the target's required build and security checks. |
| Release, package, and update channels | Containers, Unraid, Debian/RPM, AUR, PPA, Windows, macOS/Linux/FreeBSD, AppImage, Flatpak, Chocolatey, and Helm; YunoHost publishing retired | ChaptarrNG has its own release and package identities | **Open blocker.** Preserve old channel identities with tested bridge packages/images and migration instructions; no universal automatic redirect exists. |
| All other fork changes | 402 reachable post-fork commits and 1,036 net-changed paths at the pinned audit revisions | Code paths differ across the two projects | **Open blocker.** Account for every inventory path as retained, ported, or proven equivalent. Any proposed removal remains blocked until an explicit maintainer decision. The feature rows above do not replace this audit. |

## Evidence and limits

The [consolidation report](chaptarr-consolidation.md) records exact source and
target revisions, current implementation findings, the data-conversion
contract, release-channel matrix, test results, and open gates. At the reviewed
revisions, ChaptarrNG's Core suite passes, but the following decisive evidence
does not exist yet: populated BookshelfNG conversion, full feature-by-feature
semantic acceptance, SeerrNG before/after probes, and a tested old-channel
bridge. The real BookshelfNG `.69` databases inspected were empty; they prove
schema lineage only.

The BookshelfNG and ChaptarrNG databases have different schemas and identity
models. Never point ChaptarrNG at a BookshelfNG database and assume startup will
convert it. The current ChaptarrNG lineage guard rejects the inspected
BookshelfNG databases before migration. A separate converter must preserve the
source and produce a new native ChaptarrNG database.

Retirement also has a separate distribution gate. BookshelfNG's installed
updater checks the Readarr-owned update service, so changing Snapetech release
assets cannot redirect every existing installation. Pinned images, disabled
updaters, offline hosts, and manual archives also need an explicit upgrade
action. A channel-by-channel compatibility bridge can reduce effort, but a
frictionless automatic update for every historical install cannot be promised.
