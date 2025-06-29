$sourceRoot = Join-Path $PSScriptRoot 'metadata'
$destRoot = Join-Path $PSScriptRoot 'release/metadata'

# Find all description.txt files under metadata
Get-ChildItem -Path $sourceRoot -Filter 'description.txt' -Recurse | ForEach-Object {
    $relativeDir = Split-Path ($_.DirectoryName.Substring($sourceRoot.Length)) -NoQualifier
    $dirParts = $relativeDir -split '[\\/]' | Where-Object { $_ -ne '' }
    # If the last folder is media type 'E', move up one directory (to use the USA English as a failback).
    if ($dirParts.Count -gt 0 -and $dirParts[-1] -eq 'E') {
        $destDir = Join-Path $destRoot ( $dirParts[0..($dirParts.Count-2)] -join '/' )
    } else {
        $destDir = Join-Path $destRoot $relativeDir
    }
    if (-not (Test-Path $destDir)) {
        New-Item -Path $destDir -ItemType Directory | Out-Null
    }
    Copy-Item -Path $_.FullName -Destination (Join-Path $destDir 'description.txt') -Force
}