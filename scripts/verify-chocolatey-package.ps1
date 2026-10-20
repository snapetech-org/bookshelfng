param(
  [Parameter(Mandatory = $true)] [string] $PackagePath,
  [Parameter(Mandatory = $true)] [string] $PackageId,
  [Parameter(Mandatory = $true)] [string] $Version,
  [switch] $RequireBookshelfNGServiceUpgrade
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $PackagePath -PathType Leaf)) {
  throw "Chocolatey package does not exist: $PackagePath"
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$packagePath = (Resolve-Path -LiteralPath $PackagePath).Path
$archive = [System.IO.Compression.ZipFile]::OpenRead($packagePath)

function Read-PackageEntryText {
  param(
    [Parameter(Mandatory = $true)] [System.IO.Compression.ZipArchive] $Archive,
    [Parameter(Mandatory = $true)] [string] $Name
  )

  $entry = $Archive.Entries | Where-Object { $_.FullName -ieq $Name } | Select-Object -First 1
  if (-not $entry) { throw "Chocolatey package is missing $Name." }
  $reader = [System.IO.StreamReader]::new($entry.Open())
  try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
}

try {
  $nuspecEntries = @($archive.Entries | Where-Object { $_.Name -match '\.nuspec$' })
  if ($nuspecEntries.Count -ne 1) {
    throw "Chocolatey package must contain exactly one nuspec; found $($nuspecEntries.Count)."
  }

  $reader = [System.IO.StreamReader]::new($nuspecEntries[0].Open())
  try { $nuspecText = $reader.ReadToEnd() } finally { $reader.Dispose() }
  [xml] $nuspec = $nuspecText
  if ($nuspec.DocumentElement.LocalName -ne 'package') {
    throw 'Chocolatey package nuspec has no package root element.'
  }
  $metadata = $nuspec.SelectSingleNode("/*[local-name()='package']/*[local-name()='metadata']")
  if (-not $metadata) { throw 'Chocolatey package nuspec has no metadata element.' }
  $idNode = $metadata.SelectSingleNode("*[local-name()='id']")
  $versionNode = $metadata.SelectSingleNode("*[local-name()='version']")
  $copyrightNode = $metadata.SelectSingleNode("*[local-name()='copyright']")
  if (-not $idNode -or $idNode.InnerText -ine $PackageId) {
    throw "Chocolatey package ID must be '$PackageId'."
  }
  if (-not $versionNode -or $versionNode.InnerText -ne $Version) {
    throw "Chocolatey package version must be '$Version'."
  }
  if (-not $copyrightNode -or [string]::IsNullOrWhiteSpace($copyrightNode.InnerText)) {
    throw "Chocolatey package '$PackageId' is missing a non-empty copyright field."
  }
  if ($copyrightNode.InnerText -match '(?i)__[A-Z0-9_]+__|^\s*(?:TODO|TBD)\s*$') {
    throw "Chocolatey package '$PackageId' has an unresolved copyright placeholder."
  }

  $installer = Read-PackageEntryText -Archive $archive -Name 'tools/chocolateyinstall.ps1'
  if ($installer -match '__[A-Z0-9_]+__') {
    throw "Chocolatey package '$PackageId' contains an unresolved installer placeholder."
  }
  $tokens = $null
  $parseErrors = $null
  [System.Management.Automation.Language.Parser]::ParseInput($installer, [ref]$tokens, [ref]$parseErrors) | Out-Null
  if ($parseErrors.Count -gt 0) {
    throw "Chocolatey package '$PackageId' has a PowerShell installer syntax error: $($parseErrors[0].Message)"
  }

  if ($RequireBookshelfNGServiceUpgrade) {
    if ($PackageId -ine 'bookshelfng') {
      throw 'The BookshelfNG service upgrade contract can only be checked for package ID bookshelfng.'
    }

    $requiredPatterns = [ordered]@{
      'existing service detection' = '(?im)Get-Service\s+-Name\s+[''\"]?BookshelfNG[''\"]?'
      'existing service stop' = '(?im)Stop-Service\s+-Name\s+[''\"]?BookshelfNG[''\"]?'
      'NSSM Application update' = '(?im)Set-BookshelfServiceSetting\s+[''\"]Application[''\"]\s+\$exePath|&\s*\$nssm\.Source\s+set\s+BookshelfNG\s+Application\s+\$exePath'
      'NSSM AppDirectory update' = '(?im)Set-BookshelfServiceSetting\s+[''\"]AppDirectory[''\"]\s+\$[A-Za-z_]\w*|&\s*\$nssm\.Source\s+set\s+BookshelfNG\s+AppDirectory\s+\$[A-Za-z_]\w*'
      'NSSM AppParameters update' = '(?im)Set-BookshelfServiceSetting\s+[''\"]AppParameters[''\"]|&\s*\$nssm\.Source\s+set\s+BookshelfNG\s+AppParameters'
      'service start path' = '(?im)Start-Service\s+-Name\s+[''\"]?BookshelfNG[''\"]?|&\s*\$nssm\.Source\s+start\s+BookshelfNG'
    }
    foreach ($check in $requiredPatterns.GetEnumerator()) {
      if ($installer -notmatch $check.Value) {
        throw "Chocolatey package '$PackageId' is missing its $($check.Key) logic."
      }
    }

    $installCall = '(?im)&\s*\$nssm\.Source\s+install\s+BookshelfNG\b'
    if ([regex]::Matches($installer, $installCall).Count -ne 1) {
      throw "Chocolatey package '$PackageId' must install the service only when it is absent."
    }
    $conditionalInstall = '(?is)if\s*\(\s*\$service\s*\)\s*\{.*?\}\s*else\s*\{\s*&\s*\$nssm\.Source\s+install\s+BookshelfNG'
    $conditionalFirstInstall = '(?is)if\s*\(\s*-not\s+\$hadService\s*\)\s*\{.*?&\s*\$nssm\.Source\s+install\s+BookshelfNG'
    if ($installer -notmatch $conditionalInstall -and $installer -notmatch $conditionalFirstInstall) {
      throw "Chocolatey package '$PackageId' has an unconditional or unrecognized NSSM service install."
    }
  }
}
finally {
  $archive.Dispose()
}

Write-Output "Verified Chocolatey package $PackageId $Version."
