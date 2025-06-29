$sourceRoot = Join-Path $PSScriptRoot 'metadata'
$destRoot = Join-Path $PSScriptRoot 'release\metadata'

# Find all description.txt files under metadata
Get-ChildItem -Path $sourceRoot -Filter 'description.txt' -Recurse | ForEach-Object {
    $relativeDir = Split-Path ($_.DirectoryName.Substring($sourceRoot.Length)) -NoQualifier
    $destDir = Join-Path $destRoot $relativeDir
    if (-not (Test-Path $destDir)) {
        New-Item -Path $destDir -ItemType Directory | Out-Null
    }
    Copy-Item -Path $_.FullName -Destination (Join-Path $destDir 'description.txt') -Force
}