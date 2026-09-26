# Export the selected Imagegen artwork for Starbound without repainting it.
# Run on Windows. Preserve the transparent source; use nearest-neighbor sampling.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$sourcePath = Join-Path $PSScriptRoot 'art_sources/ebrar-rose/source.png'
$assetRoot = Join-Path $PSScriptRoot 'custom_assets/objects/decorative/futrebrarstar'
$sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
try {
    foreach ($export in @(
        @{Name='ebrarstar.png'; Size=[System.Drawing.Size]::new(24,40); Rect=[System.Drawing.Rectangle]::new(0,0,24,40)},
        @{Name='ebrarstaricon.png'; Size=[System.Drawing.Size]::new(16,16); Rect=[System.Drawing.Rectangle]::new(3,0,10,16)}
    )) {
        $bitmap = [System.Drawing.Bitmap]::new($export.Size.Width, $export.Size.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.Clear([System.Drawing.Color]::Transparent)
            $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
            $graphics.DrawImage($sourceImage, $export.Rect, 326, 115, 600, 1020, [System.Drawing.GraphicsUnit]::Pixel)
            $bitmap.Save((Join-Path $assetRoot $export.Name), [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally { $graphics.Dispose(); $bitmap.Dispose() }
    }
}
finally { $sourceImage.Dispose() }
