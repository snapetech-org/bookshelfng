#!/usr/bin/env bash
set -euo pipefail

readonly runtime_tag="v10.0.15"
readonly runtime_sdk="10.0.111"
readonly aspnet_sdk="10.0.112"
readonly app_sdk="${DOTNETVERSION:-10.0.404}"
readonly cross_image="mcr.microsoft.com/dotnet-buildtools/prereqs:azurelinux-3.0-net10.0-cross-x86@sha256:ecc9c107cd33f8303cba2280eb1537f045acaa88fc0f00780ea6232d19e942b8"
readonly freebsd_cross_image="mcr.microsoft.com/dotnet-buildtools/prereqs:azurelinux-3.0-net10.0-cross-freebsd-14-amd64@sha256:4ca96ef731e1466924d62d0fb6d2649cfc117bd98faedede5879ba98530e219b"
readonly linux_x86_runtime_version="10.0.15"
readonly freebsd_runtime_version="10.0.15"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work_root="${PLATFORM_RUNTIME_WORK_DIR:-$repo_root/_temp/dotnet10-platform-runtime-build}"
output_root="${PLATFORM_RUNTIME_PACKS_OUTPUT:-${BUILD_ARTIFACTSTAGINGDIRECTORY:-$repo_root/_temp/platform-runtime-packs}}"
dotnet_root="${DOTNET_ROOT:-$(dirname "$(readlink -f "$(command -v dotnet)")")}"
runtime_repo="$work_root/runtime"
aspnet_repo="$work_root/aspnetcore"
runtime_shipping="$runtime_repo/artifacts/packages/Release/Shipping"

die() {
    echo "$*" >&2
    exit 1
}

get_official_build_id() {
    local build_id="${DOTNET_OFFICIAL_BUILD_ID:-}"
    if [[ "$build_id" =~ ^20[0-9]{6}\.[0-9]+$ ]]; then
        printf '%s\n' "$build_id"
    else
        printf '%s.1\n' "$(date -u +%Y%m%d)"
    fi
}

require_sdk() {
    local version="$1"
    [ -x "$dotnet_root/dotnet" ] || die "dotnet was not found at $dotnet_root/dotnet"
    [ -f "$dotnet_root/sdk/$version/Microsoft.NETCoreSdk.BundledVersions.props" ] || die ".NET SDK $version must be installed under $dotnet_root"
}

patch_sdk_runtime_ids() {
    local sdk_version="$1"
    local sdk_root="${2:-$dotnet_root}"
    local props="$sdk_root/sdk/$sdk_version/Microsoft.NETCoreSdk.BundledVersions.props"
    python3 - "$props" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
content = path.read_text(encoding="utf-8-sig")

def patch(match):
    block = match.group(0)
    if 'TargetFramework="net10.0"' not in block:
        return block
    include = re.search(r'Include="([^"]+)"', block)
    if not include:
        return block
    package = include.group(1)
    attributes = []
    if package in ("Microsoft.NETCore.App", "Microsoft.AspNetCore.App"):
        attributes.append("RuntimePackRuntimeIdentifiers")
    if package == "Microsoft.NETCore.App":
        attributes.append("AppHostRuntimeIdentifiers")
    for attribute in attributes:
        attr = re.search(rf'{attribute}="([^"]*)"', block)
        if attr:
            values = attr.group(1).split(";")
            for rid in ("linux-x86", "freebsd-x64"):
                if rid not in values:
                    values.append(rid)
            block = block[:attr.start(1)] + ";".join(values) + block[attr.end(1):]
    return block

pattern = re.compile(r'<(?:KnownFrameworkReference|KnownAppHostPack)\s+Include="[^"]+"[\s\S]*?/>')
updated = pattern.sub(patch, content)
for framework in ("Microsoft.NETCore.App", "Microsoft.AspNetCore.App"):
    for rid in ("linux-x86", "freebsd-x64"):
        if not re.search(rf'<KnownFrameworkReference\s+Include="{re.escape(framework)}"[\s\S]*?TargetFramework="net10\.0"[\s\S]*?RuntimePackRuntimeIdentifiers="[^"]*{re.escape(rid)}', updated):
            raise SystemExit(f"SDK metadata is missing the .NET 10 {rid} runtime identifier for {framework}")
path.write_text(updated, encoding="utf-8")
PY
}

clone_sources() {
    mkdir -p "$work_root"
    git clone --depth 1 --branch "$runtime_tag" https://github.com/dotnet/runtime.git "$runtime_repo"
    git clone --depth 1 --branch "$runtime_tag" --recurse-submodules https://github.com/dotnet/aspnetcore.git "$aspnet_repo"
    git -C "$aspnet_repo" submodule update --init --depth 1
}

remove_source_checkouts() {
    docker run --rm --user 0:0 \
        --mount "type=bind,source=$work_root,target=/work" \
        "$cross_image" \
        bash -lc 'rm -rf /work/runtime /work/aspnetcore'
}

clear_previous_build_sources() {
    mkdir -p "$work_root"
    docker run --rm --user 0:0 \
        --mount "type=bind,source=$work_root,target=/work" \
        "$cross_image" \
        bash -lc 'rm -rf /work/runtime /work/aspnetcore /work/aspnet-shared'
}

patch_runtime_package_version() {
    python3 - "$runtime_repo/eng/Versions.props" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
old = "<PatchVersion>13</PatchVersion>"
new = "<PatchVersion>15</PatchVersion>"
if text.count(old) != 1:
    raise SystemExit("Expected the v10.0.15 runtime source tag to declare PatchVersion 13")
path.write_text(text.replace(old, new, 1))
PY
}

patch_runtime_sources() {
    python3 - "$runtime_repo" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])

def edit(relative, transform):
    path = root / relative
    original = path.read_text()
    updated = transform(original)
    if updated == original:
        return
    path.write_text(updated)

def add_rid_attributes(content):
    def update(match):
        tag = match.group(0)
        for name in ("RuntimePackRuntimeIdentifiers", "AppHostRuntimeIdentifiers"):
            attribute = re.search(rf'{name}="([^"]*)"', tag)
            if attribute and "linux-x86" not in attribute.group(1).split(";"):
                values = attribute.group(1).split(";")
                values.insert(values.index("linux-x64") if "linux-x64" in values else len(values), "linux-x86")
                tag = tag[:attribute.start(1)] + ";".join(values) + tag[attribute.end(1):]
        return tag
    return re.sub(r'<(?:KnownFrameworkReference|KnownAppHostPack)\s+Include="Microsoft\.NETCore\.App"[\s\S]*?/>', update, content)

edit("eng/targetingpacks.targets", add_rid_attributes)
edit("eng/Subsets.props", lambda s: re.sub(r'^.*crossgen-corelib\.proj.*\n', "", s, flags=re.MULTILINE))
edit("eng/Subsets.props", lambda s: s.replace(
    "Condition=\"'$(RuntimeFlavor)' != 'Mono' and ('$(TargetsMobile)' != 'true' and '$(TargetsLinuxBionic)' != 'true')\" Include=\"$(InstallerProjectRoot)pkg\\sfx\\Microsoft.NETCore.App\\Microsoft.NETCore.App.Crossgen2.sfxproj\"",
    "Condition=\"'$(RuntimeFlavor)' != 'Mono' and '$(TargetArchitecture)' != 'x86' and ('$(TargetsMobile)' != 'true' and '$(TargetsLinuxBionic)' != 'true')\" Include=\"$(InstallerProjectRoot)pkg\\sfx\\Microsoft.NETCore.App\\Microsoft.NETCore.App.Crossgen2.sfxproj\""))
for project in ("src/coreclr/tools/aot/crossgen2/crossgen2_publish.csproj", "src/coreclr/tools/aot/ILCompiler/ILCompiler_publish.csproj"):
    edit(project, lambda s: s.replace(
        '<RuntimeIdentifier>$(PortableOS)-$(TargetArchitecture)</RuntimeIdentifier>',
        '<RuntimeIdentifier Condition="\'$(CrossBuild)\' == \'true\'">$(NETCoreSdkRuntimeIdentifier)</RuntimeIdentifier>\n    <RuntimeIdentifier Condition="\'$(CrossBuild)\' != \'true\'">$(PortableOS)-$(TargetArchitecture)</RuntimeIdentifier>'))
edit("src/installer/pkg/sfx/Microsoft.NETCore.App/Microsoft.NETCore.App.Runtime.props", lambda s: s.replace(
    "<IncludeFallbacksInDepsFile>true</IncludeFallbacksInDepsFile>",
    "<IncludeFallbacksInDepsFile>true</IncludeFallbacksInDepsFile>\n    <PublishReadyToRun>false</PublishReadyToRun>", 1))
edit("src/installer/pkg/sfx/Microsoft.NETCore.App/Microsoft.NETCore.App.Runtime.CoreCLR.sfxproj", lambda s: s.replace(
    "</Project>",
    "  <PropertyGroup Condition=\"'$(TargetArchitecture)' == 'x86'\">\n    <NoWarn>$(NoWarn);NU5118</NoWarn>\n  </PropertyGroup>\n</Project>", 1))

subsets = (root / "eng/Subsets.props").read_text()
if "TargetArchitecture)' != 'x86'" not in subsets or "crossgen-corelib.proj" in subsets:
    raise SystemExit("Failed to apply the Linux x86 runtime subset adjustments")
PY
    sed -i '/dnceng\/internal/d' "$runtime_repo/NuGet.config"
}

build_linux_x86_runtime() {
    local official_build_id
    official_build_id="$(get_official_build_id)"
    docker run --rm --init \
        -e DOTNET_INSTALL_DIR=/usr/share/dotnet \
        -e DOTNET_ROOT=/usr/share/dotnet \
        -e DOTNET_SDK_VERSION="$runtime_sdk" \
        -e ROOTFS_DIR=/crossrootfs/x86 \
        -v "$dotnet_root:/usr/share/dotnet" \
        -v "$runtime_repo:/runtime" \
        -w /runtime \
        "$cross_image" \
        bash -lc "export PATH=/usr/share/dotnet:\$PATH; ./eng/build.sh -ci -c Release -cross -os Linux -arch x86 /m:1 /p:OfficialBuildId=$official_build_id /p:SdkVersion=$runtime_sdk /p:AppHostSourcePath=/runtime/artifacts/obj/linux-x86.Release/apphost/standalone/apphost /p:SelfContained=false /p:UseAppHost=false /p:PublishTrimmed=false /p:UseNativeAotForComponents=false /p:PublishAot=false /p:PublishReadyToRun=false /p:PublishSingleFile=false /p:StabilizePackageVersion=true -subset clr.native+clr.corelib+libs.native+libs.sfx+libs.oob+host.native+host.pkg+packs.product -pack"
}

build_freebsd_runtime() {
    local official_build_id
    official_build_id="$(get_official_build_id)"
    sed -i '/dnceng\/internal/d' "$runtime_repo/NuGet.config"
    docker run --rm --init \
        -e DOTNET_INSTALL_DIR=/usr/share/dotnet \
        -e DOTNET_ROOT=/usr/share/dotnet \
        -e DOTNET_SDK_VERSION="$runtime_sdk" \
        -e ROOTFS_DIR=/crossrootfs/x64 \
        -v "$dotnet_root:/usr/share/dotnet" \
        -v "$runtime_repo:/runtime" \
        -w /runtime \
        "$freebsd_cross_image" \
        bash -lc "export PATH=/usr/share/dotnet:\$PATH; ./build.sh -ci -c Release -cross -os freebsd -arch x64 /m:1 /p:OfficialBuildId=$official_build_id /p:SdkVersion=$runtime_sdk /p:SelfContained=false /p:UseAppHost=false /p:PublishTrimmed=false /p:UseNativeAotForComponents=false /p:PublishAot=false /p:PublishReadyToRun=false /p:PublishSingleFile=false /p:StabilizePackageVersion=true -subset clr.native+clr.corelib+libs.native+libs.sfx+libs.oob+host.native+host.pkg+packs.product -pack"
}

patch_aspnet_sources() {
    local rid="$1"
    python3 - "$aspnet_repo" "$rid" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
rid = sys.argv[2]
if rid not in ("linux-x86", "freebsd-x64"):
    raise SystemExit(f"Unsupported ASP.NET Core runtime identifier: {rid}")

versions = root / "eng/Versions.props"
text = versions.read_text()
old = "<AspNetCorePatchVersion>14</AspNetCorePatchVersion>"
new = "<AspNetCorePatchVersion>15</AspNetCorePatchVersion>"
if text.count(old) != 1:
    raise SystemExit("Expected the v10.0.15 ASP.NET Core source tag to declare patch version 14")
versions.write_text(text.replace(old, new, 1))

details = root / "eng/Version.Details.props"
text = details.read_text()
old = "<MicrosoftNETCoreAppRefPackageVersion>10.0.14</MicrosoftNETCoreAppRefPackageVersion>"
new = "<MicrosoftNETCoreAppRefPackageVersion>10.0.15</MicrosoftNETCoreAppRefPackageVersion>"
if text.count(old) != 1:
    raise SystemExit("Expected the v10.0.15 ASP.NET Core source tag to reference .NET runtime 10.0.14")
details.write_text(text.replace(old, new, 1))

props = root / "Directory.Build.props"
text = props.read_text()
supported = re.search(r'<SupportedRuntimeIdentifiers>([^<]*)</SupportedRuntimeIdentifiers>', text)
if not supported:
    raise SystemExit("Could not find ASP.NET Core supported runtime identifiers")
values = supported.group(1).split(";")
if rid not in values:
    values.append(rid)
text = text[:supported.start(1)] + ";".join(values) + text[supported.end(1):]
props.write_text(text)

dependencies = root / "eng/Dependencies.props"
text = dependencies.read_text()
anchor = '<_LatestRuntimePackageReference Include="Microsoft.NETCore.App.Runtime.linux-x64" />'
if anchor not in text:
    raise SystemExit("Could not find the linux-x64 runtime package in ASP.NET Core dependency metadata")
package = f'<_LatestRuntimePackageReference Include="Microsoft.NETCore.App.Runtime.{rid}" />'
if package not in text:
    text = text.replace(anchor, anchor + "\n    " + package, 1)
dependencies.write_text(text)
PY
    sed -i '/dnceng\/internal/d' "$aspnet_repo/NuGet.config"
    dotnet nuget add source "$runtime_shipping" --name bookshelf-linux-x86-runtime --configfile "$aspnet_repo/NuGet.config"
}

build_linux_x86_aspnetcore() {
    local official_build_id
    official_build_id="$(get_official_build_id)"
    (
        cd "$aspnet_repo"
        DOTNET_INSTALL_DIR="$dotnet_root" DOTNET_ROOT="$dotnet_root" DOTNET_SDK_VERSION="$aspnet_sdk" \
            DOTNET_MULTILEVEL_LOOKUP=0 PATH="$dotnet_root:$PATH" ./eng/build.sh --only-build-repo-tasks \
            "/p:SdkVersion=$aspnet_sdk"
    )
    patch_sdk_runtime_ids "$aspnet_sdk" "$aspnet_repo/.dotnet"
    (
        cd "$aspnet_repo"
        DOTNET_INSTALL_DIR="$dotnet_root" DOTNET_ROOT="$dotnet_root" DOTNET_SDK_VERSION="$aspnet_sdk" \
            DOTNET_MULTILEVEL_LOOKUP=0 PATH="$dotnet_root:$PATH" ./eng/build.sh -c Release -ci -arch x86 -pack \
            --projects "$aspnet_repo/src/Framework/App.Runtime/src/Microsoft.AspNetCore.App.Runtime.sfxproj" /m:1 \
            "/p:OfficialBuildId=$official_build_id" \
            "/p:SdkVersion=$aspnet_sdk" \
            /p:StabilizePackageVersion=true \
            /p:CrossgenOutput=false \
            /p:PublishReadyToRun=false
    )
}

build_freebsd_aspnetcore() {
    local official_build_id
    official_build_id="$(get_official_build_id)"
    sed -i '/dnceng\/internal/d' "$aspnet_repo/NuGet.config"
    dotnet nuget add source "$runtime_shipping" --name bookshelf-freebsd-runtime --configfile "$aspnet_repo/NuGet.config"
    mkdir -p "$aspnet_repo/artifacts/obj/Microsoft.AspNetCore.App.Runtime"
    cp "$runtime_shipping/dotnet-runtime-$freebsd_runtime_version-freebsd-x64.tar.gz" \
        "$aspnet_repo/artifacts/obj/Microsoft.AspNetCore.App.Runtime/"
    (
        cd "$aspnet_repo"
        DOTNET_INSTALL_DIR="$dotnet_root" DOTNET_ROOT="$dotnet_root" DOTNET_SDK_VERSION="$aspnet_sdk" \
            DOTNET_MULTILEVEL_LOOKUP=0 PATH="$dotnet_root:$PATH" ./eng/build.sh --only-build-repo-tasks \
            "/p:SdkVersion=$aspnet_sdk"
    )
    patch_sdk_runtime_ids "$aspnet_sdk" "$aspnet_repo/.dotnet"
    (
        cd "$aspnet_repo"
        DOTNET_INSTALL_DIR="$dotnet_root" DOTNET_ROOT="$dotnet_root" DOTNET_SDK_VERSION="$aspnet_sdk" \
            DOTNET_MULTILEVEL_LOOKUP=0 PATH="$dotnet_root:$PATH" ./eng/build.sh -c Release -ci --os-name freebsd -pack \
            --projects "$aspnet_repo/src/Framework/App.Runtime/src/Microsoft.AspNetCore.App.Runtime.sfxproj" /m:1 \
            "/p:OfficialBuildId=$official_build_id" \
            "/p:SdkVersion=$aspnet_sdk" \
            /p:StabilizePackageVersion=true \
            /p:CrossgenOutput=false \
            /p:PublishReadyToRun=false
    )
}

stage_platform_artifacts() {
    local rid="$1"
    local runtime_version="$2"
    local runtime_archive
    local aspnet_package
    local package

    mkdir -p "$output_root/packages" "$output_root/runtimes"
    for package in \
        "Microsoft.NETCore.App.Host.$rid.$runtime_version.nupkg" \
        "Microsoft.NETCore.App.Runtime.$rid.$runtime_version.nupkg"; do
        [ -s "$runtime_shipping/$package" ] || die "The .NET runtime build did not produce $package"
        cp "$runtime_shipping/$package" "$output_root/packages/"
    done

    aspnet_package="$(find "$aspnet_repo/artifacts/packages/Release/Shipping" -maxdepth 1 -type f -name "Microsoft.AspNetCore.App.Runtime.$rid.$runtime_version.nupkg" -print -quit)"
    [ -n "$aspnet_package" ] || die "ASP.NET Core did not produce the $rid runtime pack"
    cp "$aspnet_package" "$output_root/packages/"

    runtime_archive="$(find "$runtime_shipping" -maxdepth 1 -type f -name "dotnet-runtime-$runtime_version-$rid.tar.gz" -print -quit)"
    [ -n "$runtime_archive" ] || die "The .NET runtime build did not produce the $rid runtime archive"
    cp "$runtime_archive" "$output_root/runtimes/$rid-runtime.tar.gz"

    local shared_folder="$work_root/aspnet-shared/$rid"
    mkdir -p "$shared_folder"
    unzip -q -j "$aspnet_package" "runtimes/$rid/lib/net10.0/*" -d "$shared_folder"
    tar -czf "$output_root/runtimes/$rid-aspnetcore-shared.tar.gz" -C "$shared_folder" .
}

collect_platform_artifacts() {
    mkdir -p "$output_root/sdk/sdk" "$output_root/sdk/packs"
    cp -a "$dotnet_root/sdk/$app_sdk" "$output_root/sdk/sdk/"
    for pack in Microsoft.NETCore.App.Ref Microsoft.AspNetCore.App.Ref; do
        [ -d "$dotnet_root/packs/$pack/$linux_x86_runtime_version" ] || die "SDK $app_sdk is missing $pack/$linux_x86_runtime_version"
        mkdir -p "$output_root/sdk/packs/$pack"
        cp -a "$dotnet_root/packs/$pack/$linux_x86_runtime_version" "$output_root/sdk/packs/$pack/"
    done
    if [ -d "$dotnet_root/sdk-manifests/10.0.400" ]; then
        mkdir -p "$output_root/sdk/sdk-manifests"
        cp -a "$dotnet_root/sdk-manifests/10.0.400" "$output_root/sdk/sdk-manifests/"
    fi

    printf 'Linux x86 and FreeBSD runtime packs built from .NET %s and ASP.NET Core %s sources.\n' "$runtime_tag" "$runtime_tag" > "$output_root/BUILD-INFO.txt"
    cp "$repo_root/scripts/install-dotnet10-platform-runtime.sh" "$output_root/"
}

require_sdk "$runtime_sdk"
require_sdk "$aspnet_sdk"
require_sdk "$app_sdk"
command -v docker >/dev/null || die "Docker is required to cross-build the Linux x86 and FreeBSD runtimes"
command -v python3 >/dev/null || die "Python 3 is required to patch the pinned .NET build metadata"
command -v unzip >/dev/null || die "unzip is required to assemble the ASP.NET shared runtime"

clear_previous_build_sources
rm -rf "$output_root"
clone_sources
patch_sdk_runtime_ids "$runtime_sdk"
patch_sdk_runtime_ids "$aspnet_sdk"
patch_sdk_runtime_ids "$app_sdk"
patch_runtime_package_version
patch_runtime_sources
build_linux_x86_runtime
patch_aspnet_sources linux-x86
build_linux_x86_aspnetcore
stage_platform_artifacts linux-x86 "$linux_x86_runtime_version"

# Build FreeBSD from the same Microsoft servicing sources using the pinned
# FreeBSD cross-build image. Keep this phase clean of the Linux x86 source edits.
remove_source_checkouts
clone_sources
patch_runtime_package_version
build_freebsd_runtime
patch_aspnet_sources freebsd-x64
build_freebsd_aspnetcore
stage_platform_artifacts freebsd-x64 "$freebsd_runtime_version"
collect_platform_artifacts
