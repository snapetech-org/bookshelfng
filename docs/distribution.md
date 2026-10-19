# Distribution channels

Stable releases are tagged `main-vMAJOR.MINOR.PATCH.BUILD`. The release
workflow runs only after the tag is verified as reachable from `main` and the
normal BookshelfNG build succeeds. It prepares the GitHub Release as a draft,
builds platform archives and packages, attaches checksums, then publishes the
release and sends the existing Discord announcement.

Publication is frozen while BookshelfNG retirement acceptance remains open.
Tagged image and release jobs, manual package-distribution retries, and the
ChaptarrNG legacy bridge fail closed unless the BookshelfNG repository variable
`BOOKSHELFNG_RELEASE_READY` is exactly `true`. It is unset. PR #148 merged the BookshelfNG fail-closed gate to `main` as `c6b4642`, and the merge run skipped its publisher jobs. Set it only after
migration, feature parity, rollback, and every supported channel pass
acceptance; a normal CI or manual build does not enable publishing.

**Migration decision: keep BookshelfNG in service; preview only.** Do not
apply the converter, install a bridge package, or start ChaptarrNG against
BookshelfNG appdata. Normal ChaptarrNG startup converts supported source data
automatically, and the public `.977` converter is not approved for cutover.

BookshelfNG `0.4.21.71` is the published final source release. Its
source-side helper takes a full appdata archive, then invokes the standard
ChaptarrNG preview, apply, and rollback commands. ChaptarrNG `v0.9.977` remains
the latest published release; it supports the exact BookshelfNG migration-158
SQLite schema and bundles the source migration chain. The `.977` table guard
rejects versions before migration 14 until the chain renames `Blacklist` to
`Blocklist`. PR #126 merged a version-aware fix and migration-1 rollback
fixture into `main`; hosted Linux, macOS, Windows, and PostgreSQL migration
checks passed, but that fix is not in `.977`.
BookshelfNG PR #154's empty-file selection fix is on BookshelfNG source `main`
but is not in the published `.71` helper. The `.71` helper can print a
zero-byte `readarr.db` beside a populated `audioarr.db`; ChaptarrNG `.977`
resolves the non-empty database independently. See the
[migration guide](migrate-from-bookshelfng-to-chaptarrng.md) for the limits of
each version.
ChaptarrNG PR #131's code head `2c0401fc` passed exact-head hosted run
[39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646):
Linux, macOS, and Windows build/tests, PostgreSQL migration fixtures,
release-note validation, CodeQL, dependency review, dependency/secret scans,
NuGet submission, and runner-receipt reconciliation. Four Windows media-move
fixtures failed on the preceding run because they assumed POSIX paths; the
native temporary-path follow-up passes. Docs-only checkpoint `898b72fd` passed hosted run [39198708193](https://github.com/snapetech-org/chaptarrng/actions/runs/39198708193). Docs-only checkpoint `ddec3e81` also passed [run 39199730309](https://github.com/snapetech-org/chaptarrng/actions/runs/39199730309). Earlier docs-only head `353aeba1` passed exact-head validation in [run 39201211634](https://github.com/snapetech-org/chaptarrng/actions/runs/39201211634); CodeQL, dependency/security, dependency-review, and NuGet checks passed too. Fifty-two focused importer, catalog, and capability
tests pass locally. These are candidate checks, not operator-data or
installation-channel acceptance. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131) and the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/8b4c6e23/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md).
The integrated candidate snapshot `8b4c6e23` also includes current ChaptarrNG
`main`'s Editions tab and series narrator comparison. Translation, TypeScript,
targeted ESLint/Stylelint, and release-note preview checks pass locally. Its
release-note contract, dependency review, security scan, and NuGet checks pass.
CodeQL [39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712)
passes; cross-platform Build
[39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks.

ChaptarrNG releases are frozen until the retirement feature, data, rollback,
and install-channel acceptance gates close. No image or legacy alias will be
updated during this freeze. Ambiguous book formats are kept in both catalogs,
unmonitored, with a private review file; an operator-supplied media map is
optional. On 2026-10-19, candidate build `0.9.978.0` passed preview, apply,
restore preview, and rollback against a task-scoped copy of populated
migration-158 SQLite data with `HARDCOVER=true`. The live BookshelfNG service
remained running; candidate commands targeted only the separate copy, and
network access was not blocked for those commands. The source snapshot remained
unchanged, integrity and foreign-key checks passed, and rollback restored a
byte-identical source backup while preserving the converted database
separately. This is one candidate SQLite rehearsal, not
production approval. Do not use published `.977` for native Hardcover data:
it maps bare numeric IDs to Goodreads regardless of `HARDCOVER`. Older-schema
behavior on real data, PostgreSQL source conversion, ambiguous-media review,
full provider/settings behavior, feature parity, and rollback on every real
deployment remain unverified. An isolated 2026-10-18 Docker image-switch and
rollback smoke passed using the published `.71` and `.977` images with an empty
database; it does not validate the Unraid Community Apps update flow.

The helper does not copy media or download folders outside appdata or update
an installation channel. The migration bridge additionally requires
`CHAPTARRNG_MIGRATION_BRIDGE_ENABLED=true`; that flag alone cannot bypass
`BOOKSHELFNG_RELEASE_READY`. Mutable tags, pinned digests, native packages,
offline installers, and third-party catalogs need their own upgrade steps.
See the [BookshelfNG-to-ChaptarrNG handoff guide](migrate-from-bookshelfng-to-chaptarrng.md)
for the operator procedure and the
[distribution bridge matrix](maintainers/chaptarr-consolidation.md#distribution-bridge-matrix)
for channel requirements and open acceptance gates.

## Published artifacts

| Channel | Distribution | Notes |
| --- | --- | --- |
| GitHub Releases | Self-contained Windows, macOS, Linux, and FreeBSD archives; Windows x64 setup installer | Every asset has a SHA-256 file. Linux x86 and FreeBSD use the pinned .NET 10 runtime pack process. |
| Debian / Ubuntu | `.deb` package | Installs a systemd service and `/var/lib/bookshelfng` data directory. |
| Fedora / RPM | `.rpm` asset in the GitHub release; COPR repository `slskdn/bookshelfng` | The final `.71` release includes a service RPM. Current COPR metadata has no package entries for Fedora 43, 44, 45, or Rawhide x86_64; the old-identity bridge has not been published. |
| Arch Linux | `bookshelfng-bin` on AUR | Binary package with systemd service files. |
| Ubuntu PPA | Signed source package | Requires the Launchpad PPA and signing key configured in repository Actions secrets. |
| Flatpak | `.flatpak` bundle on GitHub Releases | Uses Freedesktop Platform 26.08. This bundle is not a Flathub publication. |
| AppImage | Linux x64 `.AppImage` | Portable launcher; data stays in the user's XDG data directory. |
| Chocolatey | `bookshelfng` Windows package | Downloads the checksummed x64 release asset and registers a Windows service. |
| Helm | OCI chart in GHCR | Chart is versioned with each stable BookshelfNG release. |
| Containers | GHCR and Docker Hub | Multi-architecture `amd64` and `arm64`. `:latest` and `:hardcover` are moving aliases of the Hardcover image; `:softcover` tracks the Readarr-compatible image. |
| Unraid | Community application template | Uses the moving `ghcr.io/snapetech/bookshelfng:latest` tag by default. `:hardcover` remains an equivalent alias; use `:softcover` to keep Readarr-compatible database lineage. |

The distribution workflow reports publisher channels that lack credentials as
skipped. It does not claim an upload succeeded unless the publisher command
returns success. Configure the publisher settings and credentials listed below
before expecting an external package store to receive a release.

## Publisher credentials and settings

| Secret or variable | Used by |
| --- | --- |
| `BOOKSHELFNG_RELEASE_READY` | Required as exactly `true` by tag publication, manual distribution retries, and the migration bridge; keep unset or `false` until all retirement acceptance gates close. |
| `AUR_SSH_KEY` | Pushes the `bookshelfng-bin` package to AUR. Add the matching public key to the AUR account. |
| `COPR_WEBHOOK_URL` | Package-scoped COPR custom webhook URL for the `bookshelfng` package. |
| `GPG_PRIVATE_KEY` | Signs source packages before upload to Launchpad. |
| `LAUNCHPAD_PPA` | Existing PPA target (`ppa:<owner>/<archive>`), set as an Actions secret or repository variable. |
| `CHOCOLATEY_API_KEY` | Pushes `bookshelfng` packages to Chocolatey Community Repository. |
| `DISCORD_RELEASE_WEBHOOK` | Required. Sends the curated release notes and image digests to the BookshelfNG release channel. |

Before making a GitHub Release public, the workflow validates configured
optional publishers. It skips malformed AUR, COPR, Launchpad, or Chocolatey
settings and records the reason in the workflow summary. Missing optional
credentials are also reported and skipped. The required Discord webhook is
validated before the release draft is created, so malformed settings do not
leave a public release without its announcement.

The Launchpad upload runs only when `GPG_PRIVATE_KEY` contains an importable
private signing key and `LAUNCHPAD_PPA` names an existing public PPA. Set
`LAUNCHPAD_PPA` as a repository variable or Actions secret; the publisher
account must have permission to upload to it.

The COPR build uses a custom webhook URL rather than a COPR API token. Use the
package-scoped URL from the `bookshelfng` package settings, in this form:
`https://copr.fedorainfracloud.org/webhooks/custom/<ID>/<UUID>/bookshelfng/`.
The workflow skips the COPR channel if the URL does not match this route. Treat
the URL as a secret because anyone who obtains it can request a build. COPR's
[custom webhook documentation](https://docs.copr.fedorainfracloud.org/user_documentation.html#custom-webhook)
describes this endpoint and the package-specific URL segment. The release
workflow calls it only after the GitHub Release is public. COPR then downloads
the versioned source RPM and its SHA-256 file from that release, verifies the
checksum, and extracts the spec and sources for its build. The source
preparation script is [`packaging/rpm/copr-source.sh`](../packaging/rpm/copr-source.sh).

Build output from `main` is not sent to third-party package stores; store
updates are tied to verified stable release tags.

## First publication setup

Before the first external upload, register `bookshelfng` on the Chocolatey
Community Repository, add the AUR SSH public key to the publisher account, and
create a Launchpad PPA for the publisher account. For COPR, create the public
`slskdn/bookshelfng` project with Fedora 44 and Rawhide x86_64 chroots, then add
a custom source package named `bookshelfng`. Configure its custom source script
to bootstrap the script from the release tag:

```bash
#!/usr/bin/env bash
set -euo pipefail
tag="$(tr -d '\r\n' < hook_payload)"
[[ "$tag" =~ ^(main-v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|v[0-9]+\.[0-9]+\.[0-9]+)$ ]]
curl --fail --location --silent --show-error \
  "https://raw.githubusercontent.com/snapetech-org/bookshelfng/main/packaging/rpm/copr-source.sh" \
  | bash -s -- "$tag"
```

Configure the script build dependencies as `bash curl cpio rpm`. In the COPR
project settings, create a custom webhook for the `bookshelfng` package and save
its URL as the `COPR_WEBHOOK_URL` Actions secret in `snapetech-org/bookshelfng`.
COPR's custom webhook sends the request body to the source script in
`hook_payload`; the release workflow sends the verified release tag after
publishing its assets. This setup does not need `COPR_LOGIN` or `COPR_TOKEN`.
Rotate the webhook URL in COPR and update the GitHub secret if it is exposed.

Add the remaining account credentials above to the repository's Actions
secrets. Package identifiers are reserved by their respective services, so
confirm ownership before the first publish. Flatpak is provided as a GitHub
Release bundle; Flathub hosting is a separate, maintainer-reviewed publication
path.
