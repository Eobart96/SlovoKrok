$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
& powershell -ExecutionPolicy Bypass -File (Join-Path $root "scripts\windows\check-repository.ps1")
if ($LASTEXITCODE -ne 0) { throw "Repository audit failed" }
& git -C $root diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }
$checkpoint = Join-Path $root "PROJECT_CHECKPOINT.md"
$lines = (Get-Content -LiteralPath $checkpoint).Count
$bytes = (Get-Item -LiteralPath $checkpoint).Length
if ($lines -gt 250 -or $bytes -gt 20480) { throw "Checkpoint limits exceeded: lines=$lines bytes=$bytes" }
Write-Output "checkpoint_lines=$lines checkpoint_bytes=$bytes"
Write-Output "A2 organization repository checks passed"
