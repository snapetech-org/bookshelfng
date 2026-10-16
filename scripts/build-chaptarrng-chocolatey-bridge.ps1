param(
  [Parameter(Mandatory = $true)] [string] $SourceRoot,
  [Parameter(Mandatory = $true)] [string] $Version,
  [Parameter(Mandatory = $true)] [string] $ArchivePath,
  [Parameter(Mandatory = $true)] [string] $OutputDirectory
)

$ErrorActionPreference = 'Stop'

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
  throw 'Version must be MAJOR.MINOR.PATCH.'
}
if (-not (Test-Path -LiteralPath $ArchivePath -PathType Leaf)) {
  throw 'The checksummed ChaptarrNG Windows archive is missing.'
}

$SourceRoot = (Resolve-Path -LiteralPath $SourceRoot).Path
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$archiveHash = (Get-FileHash -LiteralPath $ArchivePath -Algorithm SHA256).Hash.ToLowerInvariant()

function Build-Package {
  param(
    [Parameter(Mandatory = $true)] [string] $PackageName,
    [Parameter(Mandatory = $true)] [string] $PackageId,
    [Parameter(Mandatory = $true)] [string] $NuspecTemplate,
    [Parameter(Mandatory = $true)] [string] $InstallTemplate,
    [Parameter(Mandatory = $true)] [string] $UninstallScript
  )

  $packageDir = Join-Path $OutputDirectory $PackageName
  $toolsDir = Join-Path $packageDir 'tools'
  New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
  Copy-Item -LiteralPath $NuspecTemplate -Destination (Join-Path $packageDir "$PackageName.nuspec")
  Copy-Item -LiteralPath $InstallTemplate -Destination (Join-Path $toolsDir 'chocolateyinstall.ps1')
  Copy-Item -LiteralPath $UninstallScript -Destination (Join-Path $toolsDir 'chocolateyuninstall.ps1')

  $nuspecPath = Join-Path $packageDir "$PackageName.nuspec"
  $nuspecText = (Get-Content -LiteralPath $nuspecPath -Raw).Replace('__VERSION__', $Version)
  [System.IO.File]::WriteAllText($nuspecPath, $nuspecText, [System.Text.UTF8Encoding]::new($false))

  $installPath = Join-Path $toolsDir 'chocolateyinstall.ps1'
  $installText = (Get-Content -LiteralPath $installPath -Raw).
    Replace('__VERSION__', $Version).
    Replace('__ARCHIVE_SHA256__', $archiveHash)
  if ($installText -match '__[A-Z_]+__') {
    throw "$PackageName install script has an unresolved release placeholder."
  }
  $tokens = $null
  $parseErrors = $null
  [System.Management.Automation.Language.Parser]::ParseInput($installText, [ref]$tokens, [ref]$parseErrors) | Out-Null
  if ($parseErrors.Count -gt 0) { throw ($parseErrors | Out-String) }
  [System.IO.File]::WriteAllText($installPath, $installText, [System.Text.UTF8Encoding]::new($false))

  [xml] $parsedNuspec = Get-Content -LiteralPath $nuspecPath -Raw
  $ns = [System.Xml.XmlNamespaceManager]::new($parsedNuspec.NameTable)
  $ns.AddNamespace('n', 'http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd')
  $actualId = $parsedNuspec.SelectSingleNode('/n:package/n:metadata/n:id', $ns).InnerText
  $actualVersion = $parsedNuspec.SelectSingleNode('/n:package/n:metadata/n:version', $ns).InnerText
  if ($actualId -ne $PackageId -or $actualVersion -ne $Version) {
    throw "$PackageName package identity/version is $actualId/$actualVersion, expected $PackageId/$Version."
  }

  choco pack $nuspecPath --outputdirectory $OutputDirectory
  if ($LASTEXITCODE -ne 0) { throw "Chocolatey could not pack $PackageName." }
  $packagePath = Join-Path $OutputDirectory "$PackageId.$Version.nupkg"
  if (-not (Test-Path -LiteralPath $packagePath -PathType Leaf)) {
    throw "Chocolatey did not create $PackageId.$Version.nupkg."
  }
}

$chocolateyRoot = Join-Path $SourceRoot 'packaging/chocolatey'
$legacyRoot = Join-Path $SourceRoot 'packaging/legacy/chocolatey'

Build-Package `
  -PackageName 'chaptarrng' `
  -PackageId 'chaptarrng' `
  -NuspecTemplate (Join-Path $chocolateyRoot 'chaptarrng.nuspec.in') `
  -InstallTemplate (Join-Path $chocolateyRoot 'tools/chocolateyinstall.ps1.in') `
  -UninstallScript (Join-Path $chocolateyRoot 'tools/chocolateyuninstall.ps1')

Build-Package `
  -PackageName 'bookshelfng' `
  -PackageId 'bookshelfng' `
  -NuspecTemplate (Join-Path $legacyRoot 'bookshelfng.nuspec.in') `
  -InstallTemplate (Join-Path $legacyRoot 'tools/chocolateyinstall.ps1.in') `
  -UninstallScript (Join-Path $legacyRoot 'tools/chocolateyuninstall.ps1')

Write-Output "Built both Chocolatey package identities from the standard ChaptarrNG $Version archive."
