$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.IO.Compression.FileSystem

$verifier = Join-Path $PSScriptRoot 'verify-chocolatey-package.ps1'
$pwsh = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("bookshelfng-package-verifier-{0}" -f [guid]::NewGuid().ToString('N'))

if (-not (Test-Path -LiteralPath $verifier -PathType Leaf)) {
  throw 'The Chocolatey package verifier is missing.'
}

$validInstaller = @'
$service = Get-Service -Name 'BookshelfNG' -ErrorAction SilentlyContinue
if ($service) {
  Stop-Service -Name 'BookshelfNG' -Force
  Set-BookshelfServiceSetting 'Application' $exePath
  Set-BookshelfServiceSetting 'AppDirectory' $binDir
  Set-BookshelfServiceSetting 'AppParameters' "/nobrowser -data=$dataDir"
  Start-Service -Name 'BookshelfNG'
} else {
  & $nssm.Source install BookshelfNG $exePath
}
'@

function New-TestPackage {
  param(
    [Parameter(Mandatory = $true)] [string] $Path,
    [Parameter(Mandatory = $true)] [string] $PackageId,
    [Parameter(Mandatory = $true)] [string] $Installer,
    [Parameter(Mandatory = $true)] [bool] $IncludeCopyright
  )

  $copyright = if ($IncludeCopyright) { '<copyright>Test copyright.</copyright>' } else { '' }
  $nuspec = @"
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd"><metadata><id>$PackageId</id><version>1.2.3</version>$copyright</metadata></package>
"@

  $archive = [System.IO.Compression.ZipFile]::Open($Path, [System.IO.Compression.ZipArchiveMode]::Create)
  try {
    $entries = [ordered]@{
      'bookshelfng.nuspec' = $nuspec
      'tools/chocolateyinstall.ps1' = $Installer
    }
    foreach ($name in $entries.Keys) {
      $entry = $archive.CreateEntry($name)
      $writer = [System.IO.StreamWriter]::new($entry.Open(), [System.Text.UTF8Encoding]::new($false))
      try { $writer.Write($entries[$name]) } finally { $writer.Dispose() }
    }
  } finally {
    $archive.Dispose()
  }
}

function Invoke-PackageVerifier {
  param(
    [Parameter(Mandatory = $true)] [string] $Path,
    [Parameter(Mandatory = $true)] [string] $PackageId,
    [switch] $RequireServiceUpgrade,
    [switch] $Quiet
  )

  $arguments = @(
    '-NoProfile',
    '-File', $verifier,
    '-PackagePath', $Path,
    '-PackageId', $PackageId,
    '-Version', '1.2.3'
  )
  if ($RequireServiceUpgrade) { $arguments += '-RequireBookshelfNGServiceUpgrade' }

  try {
    $output = & $pwsh @arguments 2>&1
    $exitCode = $LASTEXITCODE
    if (-not $Quiet) { foreach ($line in $output) { Write-Host $line } }
    return [int]$exitCode
  } catch {
    if (-not $Quiet) { Write-Host $_.Exception.Message }
    return 1
  }
}

New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
try {
  $validChaptarrPackage = Join-Path $tempRoot 'chaptarrng.nupkg'
  New-TestPackage -Path $validChaptarrPackage -PackageId 'chaptarrng' -Installer $validInstaller -IncludeCopyright $true
  if ((Invoke-PackageVerifier -Path $validChaptarrPackage -PackageId 'chaptarrng') -ne 0) {
    throw 'The verifier rejected a valid ChaptarrNG package.'
  }

  $validLegacyPackage = Join-Path $tempRoot 'bookshelfng.nupkg'
  New-TestPackage -Path $validLegacyPackage -PackageId 'bookshelfng' -Installer $validInstaller -IncludeCopyright $true
  if ((Invoke-PackageVerifier -Path $validLegacyPackage -PackageId 'bookshelfng' -RequireServiceUpgrade) -ne 0) {
    throw 'The verifier rejected a valid BookshelfNG upgrade package.'
  }

  $missingCopyrightPackage = Join-Path $tempRoot 'missing-copyright.nupkg'
  New-TestPackage -Path $missingCopyrightPackage -PackageId 'bookshelfng' -Installer $validInstaller -IncludeCopyright $false
  if ((Invoke-PackageVerifier -Path $missingCopyrightPackage -PackageId 'bookshelfng' -RequireServiceUpgrade -Quiet) -eq 0) {
    throw 'The verifier accepted a package without copyright metadata.'
  }

  $badUpgradePackage = Join-Path $tempRoot 'missing-service-upgrade.nupkg'
  $badInstaller = [regex]::Replace($validInstaller, '(?m)^.*Set-BookshelfServiceSetting ''AppDirectory'' \$binDir.*(?:\r?\n)?', '')
  New-TestPackage -Path $badUpgradePackage -PackageId 'bookshelfng' -Installer $badInstaller -IncludeCopyright $true
  if ((Invoke-PackageVerifier -Path $badUpgradePackage -PackageId 'bookshelfng' -RequireServiceUpgrade -Quiet) -eq 0) {
    throw 'The verifier accepted a legacy package without the service directory upgrade.'
  }

  Write-Output 'Chocolatey package verifier tests passed.'
  # The expected-rejection cases leave a nonzero native exit code behind.
  # Clear it so PowerShell action wrappers do not report this successful test
  # script as failed when they propagate the last native process status.
  $global:LASTEXITCODE = 0
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}
