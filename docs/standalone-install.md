# Standalone installation

**Final release:** BookshelfNG `0.4.21.71` is published. This guide remains
for existing installations; new installations should use the maintained
[ChaptarrNG releases](https://github.com/snapetech-org/chaptarrng/releases).
ChaptarrNG `v0.9.977` remains the latest public release. Its converter supports
the exact BookshelfNG migration-158 SQLite schema and bundles the source
migration chain, but rejects versions before migration 14. Upgrade BookshelfNG
to `.71` before switching a database with an earlier schema.
The `.71` helper is not the same as the current BookshelfNG source `main`
helper: PR #154's empty-database selection fix was merged after `.71` and has
not been released. The `.977` ChaptarrNG resolver independently ignores
zero-byte legacy files; see the
[migration guide](migrate-from-bookshelfng-to-chaptarrng.md) for the exact
behavior.

Until retirement acceptance closes, keep BookshelfNG in service. The public
`.977` converter is for read-only preview only; do not install a bridge or
start ChaptarrNG against BookshelfNG appdata because normal startup can convert
the source database automatically.

PR #126 merged the version-aware table guard and synthetic migration-1 rollback fixture into ChaptarrNG `main`; that source fix is not in published `.977`. ChaptarrNG releases remain frozen while migration, parity, populated-data rollback, and installer/channel acceptance are open. The helper archives appdata but does not copy external media or downloads or update a package, image, native installer, or Helm deployment. ChaptarrNG PR #131 code head `2c0401fc` passed exact-head run [39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646): Linux, macOS, Windows, all four PostgreSQL fixture cases, release-note and receipt checks, CodeQL, dependency review, secret scan, and NuGet submission. Docs-only checkpoint `898b72fd` passed hosted run [39198708193](https://github.com/snapetech-org/chaptarrng/actions/runs/39198708193). Docs-only checkpoint `ddec3e81` also passed [run 39199730309](https://github.com/snapetech-org/chaptarrng/actions/runs/39199730309). Earlier docs-only head `353aeba1` passed exact-head validation in [run 39201211634](https://github.com/snapetech-org/chaptarrng/actions/runs/39201211634); CodeQL, dependency/security, dependency-review, and NuGet checks passed too. Disposable-fork validation was skipped by its gate. Retirement candidate code snapshot `8b4c6e23` integrates current ChaptarrNG `main`, including the Editions and Narrations tab and series narrator comparison, and carries the migration, rollback, provider-identity, and media-move work. Local translation, TypeScript, targeted ESLint/Stylelint, and release-note preview pass. Its release-note contract, dependency review, security scan, and NuGet checks pass. CodeQL run [39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712) passes; exact-head cross-platform Build [39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. Operator-data and channel acceptance remain open. These checks do not establish operator-data or installer/channel acceptance; see the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/8b4c6e23/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md) and [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131). BookshelfNG’s fail-closed publisher gate merged as `c6b4642`; its readiness variable remains unset and `.71` remains the final release.

BookshelfNG is a web application that can run directly on a supported host. It
does not need SeerrNG or another service to launch, search catalogs, manage a
library, or provide its web interface. The container edition remains available
for Docker and Kubernetes deployments.

## Release assets

Each stable `main-v*` release publishes checksummed, self-contained archives for
Windows x64 and x86, macOS x64 and ARM64, Linux x64, x86 and ARM, Linux ARM64,
glibc and musl Linux variants, and FreeBSD x64. The platform pack workflow
builds the Linux x86 and FreeBSD .NET 10 runtimes from the pinned sources
documented in [the platform build notes](./dotnet-10-platform-builds.md).

Archives contain the app, web UI, license, and this installation guide. They
include the .NET runtime. Linux packages may still need the host's ICU, OpenSSL,
SQLite, and C library packages. `ffmpeg` is optional and is only needed for
chaptered audiobook generation.

Download the archive matching the host from the
[BookshelfNG releases](https://github.com/snapetech-org/bookshelfng/releases). Check
the adjacent `.sha256` file before extracting it. Then start the app from its
extracted directory:

```sh
./Readarr -nobrowser -data="$HOME/.local/share/bookshelfng"
```

On Windows, use `Readarr.exe` and a data directory under `%LOCALAPPDATA%`:

```powershell
.\Readarr.exe -nobrowser "-data=$env:LOCALAPPDATA\BookshelfNG"
```

Each release also includes a Windows x64 setup installer. Run it as
administrator to install BookshelfNG as a Windows service. Before upgrading, it
backs up the existing Readarr-compatible installation and can restore that
backup if the new service does not start.

Open `http://localhost:8787` in a browser. Keep the data directory on persistent
storage and back it up before replacing an installation. To migrate a Docker
library, stop the container and copy its `/config` contents into the chosen
native data directory before starting BookshelfNG.

## Linux packages and service

The `.deb`, RPM, and AUR packages install the app under `/usr/lib/bookshelfng`,
create the `bookshelfng` service account, and install a systemd unit. The
service stores configuration and its database under `/var/lib/bookshelfng`.
After installing a package, assign the service account access to any book,
audiobook, download, or completed-download directories it must use, then start
the service:

```sh
sudo systemctl enable --now bookshelfng
```

Install a downloaded Debian package with:

```sh
sudo apt install ./bookshelfng_*.deb
```

Install a downloaded RPM package with:

```sh
sudo dnf install ./bookshelfng-*.rpm
```

External package repositories are optional for each release. If the release
lists the `slskdn/bookshelfng` COPR project, enable it with
`sudo dnf copr enable slskdn/bookshelfng`, then run `sudo dnf install bookshelfng`.
If `bookshelfng-bin` is published to AUR, install it with an AUR helper such as
`paru -S bookshelfng-bin`. A Launchpad PPA is published only when an existing
PPA and signing key are configured; use the target named in the release.
When the Chocolatey package channel is enabled, install it from an elevated
PowerShell prompt with `choco install bookshelfng`.

Configuration overrides can be placed in
`/etc/bookshelfng/bookshelfng.env`. Package upgrades leave this file and
`/var/lib/bookshelfng` in place.

## AppImage

The AppImage is a portable Linux x64 launcher. Make it executable and run it;
its default data directory is `$XDG_DATA_HOME/bookshelfng` or
`~/.local/share/bookshelfng`:

```sh
chmod +x BookshelfNG-*.AppImage
./BookshelfNG-*.AppImage
```

## Flatpak bundle

The `.flatpak` file is a single-file bundle for direct installation. It uses
the Freedesktop 26.08 runtime, which Flatpak installs from Flathub if it is not
already present. Grant access only to the directories that contain your book
and download libraries; for example:

```sh
flatpak install --user ./BookshelfNG-main-v*.flatpak
flatpak run com.snapetech.BookshelfNG
flatpak override --user --filesystem=/path/to/books:rw com.snapetech.BookshelfNG
```

The bundle is attached to GitHub Releases; it is not currently published to
Flathub.

## Chocolatey

On Windows, install with Chocolatey:

```powershell
choco install bookshelfng
Start-Service BookshelfNG
```

Chocolatey installs the self-contained Windows x64 build and registers the
BookshelfNG service. Its data is stored under `%ProgramData%\BookshelfNG\data`.

## Helm and containers

BookshelfNG images are multi-architecture (`amd64`, `arm64`) and published to
GHCR and Docker Hub. The Helm chart uses the same images and includes a
persistent volume claim for `/config`. See the [container and Helm guide](../README.md#install).

## Metadata and edition behavior

Standalone installs use the same settings and catalog selection as the
container image. Hardcover and Open Library can each be enabled or disabled in
Settings; selecting a catalog is independent of SeerrNG. The `softcover` and
`hardcover` container tags only select the default metadata profile. Native
packages use the same BookshelfNG application and default catalog settings.

For package sources, publisher repositories, checksums, and release workflow
details, see [distribution channels](./distribution.md).
