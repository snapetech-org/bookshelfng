# BookshelfNG to ChaptarrNG distribution bridge

## Current status — 2026-10-18

BookshelfNG `0.4.21.71` is the published final source release and includes an
appdata handoff helper. Issue #114 is closed. ChaptarrNG `v0.9.977` is
published with the migration tools, the bundled BookshelfNG SQLite chain, and
an unmonitored dual-catalog fallback for records whose formats cannot be
inferred. Its pre-upgrade table guard rejects source versions before migration
14 because they still use `Blacklist`; a version-aware fix is under hosted
validation for a follow-up release. The bridge described below remains
disabled; no BookshelfNG package identity or image alias has been redirected.
ChaptarrNG AUR `0.9.977-1` is published. The standard COPR package
`chaptarrng 0.9.977-1` built successfully for Fedora 43, 44, 45, and Rawhide
x86_64. Chocolatey `.977` passed package-transition smoke validation, but its
push returned HTTP 403 and the live feed has no `chaptarrng` entry. The
BookshelfNG AUR identity remains on its own `0.4.21.71-1` payload; the public
Chocolatey identity remains at `0.4.21.70`. Feature and channel acceptance
gates are still open. Use this channel matrix as a gate inventory,
not a report of completed redirects.

The bridge workflow is a candidate for the BookshelfNG repository. It is
disabled unless the `CHAPTARRNG_MIGRATION_BRIDGE_ENABLED` repository variable
is explicitly set to `true`. Its half-hour schedule and manual dispatch only
run publishing logic from `main`. It waits for a stable ChaptarrNG release
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
not available, set the same repository variable in both ChaptarrNG and
BookshelfNG; setting it in only one repository bridges only that repository's
release paths.

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
| AUR `bookshelfng-bin` | The ChaptarrNG release workflow builds and submits both the new and legacy package identities using the ChaptarrNG AUR credential. | AUR review/build state and an installed-machine upgrade with real operator data. |
| Unraid Community Apps | A running BookshelfNG template that pulls a mutable BookshelfNG GHCR tag can receive the standard ChaptarrNG image after that alias moves. | The catalog listing, pinned image references, cached tags, template-specific volume/environment compatibility, and automatic rollout. |
| Debian/PPA, AppImage, Flatpak, native archives, Windows setup, macOS, FreeBSD, YunoHost, and third-party catalogs | No universal redirect is implemented here. | Each package identity, feed, updater, signing key, and manual download path needs its own tested migration or a clear operator handoff. |

## COPR one-time update

The existing COPR package's custom-source bootstrap currently accepts the
BookshelfNG release tag format. Before enabling this bridge, update that COPR
script so it accepts both the old and ChaptarrNG tag forms and passes the value
to the current `packaging/rpm/copr-source.sh` from the BookshelfNG `main`
branch:

```bash
tag="$(tr -d '\r\n' < hook_payload)"
[[ "$tag" =~ ^(main-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|v[0-9]+\.[0-9]+\.[0-9]+)$ ]]
curl --fail --location --silent --show-error \
  "https://raw.githubusercontent.com/snapetech/bookshelfng/main/packaging/rpm/copr-source.sh" \
  | bash -s -- "$tag"
```

The COPR webhook URL must remain the package-scoped custom endpoint for
`bookshelfng`. It is used as a secret and must not be printed in workflow logs.

As of 2026-10-14, the public [new ChaptarrNG COPR project](https://copr.fedorainfracloud.org/coprs/slskdn/chaptarrng/)
exists for Fedora 43/44/45 and Rawhide x86_64. Its `chaptarrng` custom-source
package uses the checked-in bootstrap with `bash curl cpio rpm` build
dependencies and auto-rebuild enabled. The package-scoped webhook is stored
in ChaptarrNG Actions as `COPR_WEBHOOK_URL`. The package has no builds yet;
the public ChaptarrNG `v0.9.969` release has no assets, including the SRPM and
checksum the bootstrap requires. ChaptarrNG Actions now has the
`BOOKSHELFNG_COPR_WEBHOOK_URL` for the legacy identity, and BookshelfNG's
`COPR_WEBHOOK_URL` was rotated to the matching package-scoped endpoint. Neither
hook has been tested by submitting a COPR build. The existing
`slskdn/bookshelfng` COPR bootstrap must still be updated and proven before
the bridge is enabled. This new-project setup is not a package publication
or retirement-continuity proof.

## Enablement gates

Keep the repository variable unset or `false` until all of these are true:

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
