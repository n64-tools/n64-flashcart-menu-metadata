# Requires: Windows PowerShell (not PowerShell Core), .NET Framework
Add-Type -AssemblyName System.Drawing

$metadataDir = "metadata"
$releaseDir = "release"

$sizes = @{
    "boxart_front.png" = [System.Drawing.Size]::new(158,112)
    "boxart_back.png" = [System.Drawing.Size]::new(158,112)
    "boxart_spine.png" = [System.Drawing.Size]::new(158,112)
    "gamepak_front.png" = [System.Drawing.Size]::new(158,112)
}

function Resize-Image($inPath, $size, $outPath) {
    $img = [System.Drawing.Image]::FromFile($inPath)
    $bmp = New-Object System.Drawing.Bitmap $size.Width, $size.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.DrawImage($img, 0, 0, $size.Width, $size.Height)
    $bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $img.Dispose()
    $bmp.Dispose()
}

Get-ChildItem -Path $metadataDir -Recurse -File | ForEach-Object {
    $fileName = $_.Name
    if ($sizes.ContainsKey($fileName)) {
        $relPath = $_.DirectoryName.Substring($metadataDir.Length)
        $outFolder = Join-Path $releaseDir $relPath
        if (!(Test-Path $outFolder)) { New-Item -ItemType Directory -Path $outFolder | Out-Null }
        $outPath = Join-Path $outFolder $fileName
        Resize-Image $_.FullName $sizes[$fileName] $outPath
    }
}
