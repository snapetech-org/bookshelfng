# BookshelfNG to ChaptarrNG distribution bridge

## Current status — 2026-10-21

**Update (2026-10-21):** BookshelfNG `0.4.21.71` remains the final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` is [`ac9d0f67`](https://github.com/snapetech-org/chaptarrng/commit/ac9d0f675ccf8b58e649f0b1c8128bfd8d3e1358), and its Build workflow is [39582456911](https://github.com/snapetech-org/chaptarrng/actions/runs/39582456911). Standalone no-publication validation [39582093706](https://github.com/snapetech-org/chaptarrng/actions/runs/39582093706) on candidate `d71ec42e` passed nine archive targets and the focused runtime-pack permission regression; the combined Linux x86 and FreeBSD runtime-pack job is still running. The prior attempt [39573719493](https://github.com/snapetech-org/chaptarrng/actions/runs/39573719493) failed in those two jobs; GNU tar now preserves existing shared .NET directory metadata with `--no-overwrite-dir`. No release, package, image, installer, or migration bridge has been published. The legacy Chocolatey bridge gate remains off, and the Unraid template still points to BookshelfNG. AUR and RPM legacy recipes are mapped to ChaptarrNG templates, but their local rehearsals do not validate live feeds or real-systemd transactions. Issue [#144](https://github.com/snapetech-org/bookshelfng/issues/144) remains open for representative data, rollback, parity, installed-channel handoff, and operator acceptance.

BookshelfNG `0.4.21.71` remains the final published release; ChaptarrNG
`v0.9.977` remains the latest public release. ChaptarrNG PR [#131](https://github.com/snapetech-org/chaptarrng/pull/131)
merged to `main` as `d2bcba7953a14d2d726f47005a660314cc5e4c26`. Exact-head
Build [39374140961](https://github.com/snapetech-org/chaptarrng/actions/runs/39374140961)
passed Linux, macOS, Windows, PostgreSQL migration, release-note, and runner
receipt checks, including the synthetic Windows Bookshelf service upgrade and
rollback round trip. CodeQL, dependency review, Semgrep CE, Trivy, NuGet, and
Helm resource-identity validation passed. The separate GHAS Semgrep OSS check
remains failed with reviewed SQL-format and fixed-test-path findings; see PR
#131 for the manual review and focused local scan results.

The source merge does not redirect or publish any BookshelfNG identity. Keep
both publication gates closed, keep the migration bridge disabled, and keep
BookshelfNG in service until issue #144's representative-data, rollback,
feature-parity, provider, and update-channel acceptance gates close. Unraid
transition PR #5 remains draft until real-data rollback and Community
Applications UI acceptance.

ChaptarrNG AUR `0.9.977-1` is published. A local BookshelfNG-identity AUR
candidate passed a network-disabled pacman upgrade from the published
`0.4.21.71-1` package and downgrade back, preserving an environment override
and synthetic data canary. The installed candidate also passed preview,
conversion, and restore against a synthetic populated migration-158 database.
In a second rehearsal, systemd stopped the active `.71` service for upgrade,
started ChaptarrNG, and then started BookshelfNG again after restore and
downgrade. The fixture passed SQLite integrity and foreign-key checks. The
network-online wait was masked only in the network-isolated test container;
representative operator data and host-specific settings remain open. The
standard COPR package `chaptarrng 0.9.977-1` built successfully for Fedora 43,
44, 45, and Rawhide x86_64. The legacy COPR trigger remains disabled.
Chocolatey `.977` passed package-transition smoke validation, but its push
returned HTTP 403 and the live feed has no `chaptarrng` entry. The
BookshelfNG AUR identity remains on its own `0.4.21.71-1` payload; the
published Chocolatey `bookshelfng` package remains at `0.4.21.70`, while the
latest GitHub release is `0.4.21.71`. Feature and channel acceptance
gates are still open. An isolated 2026-10-18 Docker image-switch and rollback
smoke passed on an empty migration-158 database; the old image started again
on port 8787. The Unraid Community Apps template update remains untested. Use
this channel matrix as a gate inventory, not a report of completed redirects.

The bridge workflow is present in the BookshelfNG repository, but publishing
requires both `BOOKSHELFNG_RELEASE_READY=true` and
`CHAPTARRNG_MIGRATION_BRIDGE_ENABLED=true`; both variables are unset. The first
gate also blocks BookshelfNG tag-triggered images/releases and manual package
retries. Its half-hour schedule and manual dispatch only run publishing logic
from `main`. It waits for a stable ChaptarrNG release
with checksummed Linux x64, Linux arm64, Windows x64, and both new and legacy
RPM source packages. Every publish path uses the ordinary ChaptarrNG release
payload; there is no compatibility image or second ChaptarrNG build.

The ChaptarrNG release workflows use the same variable as a second gate before
publishing legacy BookshelfNG AUR and Docker Hub identities. Docker Hub, COPR,
Chocolatey, and Helm work runs through the BookshelfNG bridge workflow. GHCR
aliases are dispatched directly by the gated ChaptarrNG release to a separate
personal-account bridge because the legacy GHCR package is owned by
`snapetech`; the organization-owned workflow cannot write that package with
its own `GITHUB_TOKEN`. Normal releases still publish the standard ChaptarrNG
image and package identities while the flag is unset.

Repository variables are scoped per repository. After every acceptance gate
below passes, prefer one organization Actions variable named
`CHAPTARRNG_MIGRATION_BRIDGE_ENABLED` scoped to both repositories. If that is
not available, set the same bridge variable in both ChaptarrNG and BookshelfNG;
setting it in only one repository bridges only that repository's release
paths. Set `BOOKSHELFNG_RELEASE_READY=true` only in BookshelfNG, and set
`CHAPTARRNG_RELEASE_READY=true` only in ChaptarrNG, after the full retirement
acceptance is complete.

The stable container identity is `ghcr.io/snapetech/chaptarrng`. The GitHub
repository now lives at `snapetech-org/chaptarrng`, while both public package
names remain under the original `snapetech` account namespace. The standard
publisher remains responsible for the ChaptarrNG package. Legacy
`bookshelfng:{latest,hardcover,softcover}` tags are written only by
`snapetech/bookshelfng-ghcr-release-bridge`, using that personal repository's
`GITHUB_TOKEN`; setup still requires package write access on the existing
`bookshelfng` package and a narrowly scoped GitHub App installation that lets
the ChaptarrNG release dispatch to the bridge repository. The bridge reads
the public ChaptarrNG image by immutable digest and never builds another
image. Do not derive image names from the repository owner's name.

The BookshelfNG workflow records one marker tag per channel and target release
for the channels it publishes. A marker is written only after that channel's
publisher accepts the update. GHCR is dispatched separately to the personal
account bridge and is not written by this organization workflow. A Chocolatey
upload still needs moderation, and a COPR trigger still needs a successful
downstream build before either channel is considered verified. Workflow
summaries report publisher outcomes, not completed retirement gates.

| Existing BookshelfNG channel | Candidate continuity path | What it does not move or prove |
| --- | --- | --- |
| GHCR image tags | A separately scoped personal-account bridge retags the exact multi-architecture ChaptarrNG release image digest as `ghcr.io/snapetech/bookshelfng:latest`, `:hardcover`, and `:softcover`. | Bridge repository/App setup, package write access, pinned digests, other tags, registry caches, already-running containers, and a successful populated-library startup on each platform. |
| Docker Hub image tags | Mirrors the standard ChaptarrNG image to `snapetech/chaptarrng:<version>` and updates the moving ChaptarrNG and BookshelfNG aliases when the existing Docker Hub credentials are configured. | Pinned digests, cached images, and existing containers until their operator pulls/recreates them. |
| COPR `slskdn/bookshelfng` | Sends the ChaptarrNG tag to the existing package-scoped COPR webhook. COPR downloads and verifies the legacy `bookshelfng` source RPM built from the same ChaptarrNG archive. | The external COPR custom-source bootstrap must first accept `vMAJOR.MINOR.PATCH` tags. A successful webhook response does not prove that COPR built or published the package. |
| Chocolatey `bookshelfng` | Builds both `chaptarrng` and `bookshelfng` packages from the checksummed standard Windows archive, then submits each identity with the existing Chocolatey credential. The legacy package keeps the existing service and `%ProgramData%\BookshelfNG\data` path while converting supported database data at normal startup. | Chocolatey moderation/approval, unsupported database inputs, and upgrade/rollback behavior outside the hosted Windows release test. |
| BookshelfNG Helm OCI chart | Publishes a new chart version under the existing BookshelfNG OCI chart identity and pins it to the exact standard ChaptarrNG multi-architecture image digest while preserving the chart's resource names, PVC, labels, and port. | Existing releases do not upgrade themselves. Operators must apply a chart update, and pinned charts or image digests stay pinned. |
| AUR `bookshelfng-bin` | The ChaptarrNG release workflow builds and submits both the new and legacy package identities using the ChaptarrNG AUR credential. | The synthetic active-systemd migration/restore rehearsal passed; representative operator data and host-specific service settings remain open. |
| Unraid Community Apps | A running BookshelfNG template that pulls a mutable BookshelfNG GHCR tag can receive the standard ChaptarrNG image after that alias moves. | The catalog listing, pinned image references, cached tags, template-specific volume/environment compatibility, and automatic rollout. |
| Debian/PPA, AppImage, Flatpak, native archives, Windows setup, macOS, FreeBSD, YunoHost, and third-party catalogs | No universal redirect is implemented here. | Each package identity, feed, updater, signing key, and manual download path needs its own tested migration or a clear operator handoff. |

## COPR one-time update

The existing `slskdn/bookshelfng` custom-source bootstrap must accept both
the BookshelfNG release tag format and the ChaptarrNG `vMAJOR.MINOR.PATCH`
format before this bridge can run. The checked-in
`packaging/rpm/copr-source.sh` already accepts both forms and verifies the
source RPM; update the external bootstrap to fetch that script from the current
BookshelfNG `main` branch:

```bash
tag="$(tr -d '\r\n' < hook_payload)"
[[ "$tag" =~ ^(main-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|v[0-9]+\.[0-9]+\.[0-9]+)$ ]]
curl --fail --location --silent --show-error \
  "https://raw.githubusercontent.com/snapetech-org/bookshelfng/main/packaging/rpm/copr-source.sh" \
  | bash -s -- "$tag"
```

The COPR webhook URL must remain the package-scoped custom endpoint for
`bookshelfng`. It is used as a secret and must not be printed in workflow logs.

As of 2026-10-18, the public
[new ChaptarrNG COPR project](https://copr.fedorainfracloud.org/coprs/slskdn/chaptarrng/)
exists for Fedora 43/44/45 and Rawhide x86_64. The standard
chaptarrng 0.9.977-1 package built successfully for those targets. The legacy
BookshelfNG trigger was skipped while the bridge is disabled, so its
old-identity package upgrade remains untested.

The checked-in BookshelfNG script at packaging/rpm/copr-source.sh accepts both
the old main-vMAJOR.MINOR.PATCH.BUILD tags and ChaptarrNG vMAJOR.MINOR.PATCH
tags, then verifies the source RPM checksum and expected payload. The external
slskdn/bookshelfng custom-source bootstrap still needs a confirmed update and
a successful legacy-identity build; a checked-in script does not prove that
the external COPR configuration uses it. The new ChaptarrNG COPR webhook and
the package-scoped BookshelfNG webhook are configured, but the disabled
legacy trigger has not tested the old package path. This new-project setup is
not a package publication or retirement-continuity proof.

## Enablement gates

Keep `BOOKSHELFNG_RELEASE_READY` and `CHAPTARRNG_MIGRATION_BRIDGE_ENABLED`
unset or `false` until all of these are true:

- The cumulative BookshelfNG feature set and all active ChaptarrNG features
  remain represented in the retirement matrices, with implementation and
  required tests merged into ChaptarrNG.
- The standard ChaptarrNG startup converter has passed supported-schema,
  populated-database, rollback, restart, and platform checks. Ambiguous source
  media relationships have a safe operator path and do not silently choose a
  wrong type.
- The ordinary stable ChaptarrNG release publishes all assets and checksums
  this workflow requires, and its standard image has the required platforms.
- The existing COPR source bootstrap is updated and a real legacy-identity
  build succeeds; the Chocolatey package is approved and its hosted upgrade
  test passes; the Helm chart is rendered and the existing release upgrade is
  exercised on disposable data.
- The bridge's GHCR, Docker Hub, AUR, and Chocolatey credentials and package
  permissions are confirmed by the relevant publisher jobs without exposing
  credential values. GHCR Actions write access is explicitly granted for both
  the standard `chaptarrng` package and the legacy `bookshelfng` package.
- Remaining manual, pinned, offline, native, and third-party channels have
  explicit release notes and a migration path. Mutable tags are not described
  as automatic updates for installations that never pull or apply updates.

Until these checks pass, this is implementation and test tooling, not a live
redirect and not permission to announce BookshelfNG retirement.
