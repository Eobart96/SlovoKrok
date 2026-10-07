$ErrorActionPreference = "Continue"
$PSNativeCommandUseErrorActionPreference = $false
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$python = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw "Bundled Python not found: $python" }

& $python (Join-Path $root "scripts\verify-a2-pdf-collection.py")
if ($LASTEXITCODE -ne 0) { throw "Collection integrity checker failed" }

$generic = Join-Path $root "scripts\verify-a2-pdf.py"
$first = Get-ChildItem -LiteralPath (Join-Path $root "output\pdf\A2\Module_01") -Filter "Slovak_A2_Tema_1_1_*.pdf" -File
if ($first.Count -ne 1) { throw "Expected one PDF 1.1, found $($first.Count)" }
& $python $generic $first[0].FullName
if ($LASTEXITCODE -ne 0) { throw "Generic verifier failed for PDF 1.1" }

$verifiers = Get-ChildItem -LiteralPath (Join-Path $root "scripts") -Filter "verify-a2-pdf-*.py" -File |
    Where-Object { $_.Name -ne "verify-a2-pdf-collection.py" } |
    Sort-Object Name
$passed = 1
foreach ($verifier in $verifiers) {
    if ($verifier.BaseName -notmatch '^verify-a2-pdf-(\d+)-(\d+)$') { continue }
    $module = [int]$Matches[1]
    $topic = [int]$Matches[2]
    $moduleDir = "Module_{0:D2}" -f $module
    $pattern = "Slovak_A2_Tema_{0}_{1}_*.pdf" -f $module, $topic
    $pdf = Get-ChildItem -LiteralPath (Join-Path $root "output\pdf\A2\$moduleDir") -Filter $pattern -File
    if ($pdf.Count -ne 1) { throw "Expected one PDF $module.$topic, found $($pdf.Count)" }
    $source = Get-Content -LiteralPath $verifier.FullName -Raw
    if ($source.Contains('modes.add_argument("--structure"') -and $source.Contains('modes.add_argument("--content"')) {
        foreach ($mode in @("--structure", "--content")) {
            $output = & $python $verifier.FullName $mode 2>&1
            if ($LASTEXITCODE -ne 0) { throw "$($verifier.Name) $mode failed:`n$($output -join [Environment]::NewLine)" }
        }
    } else {
        $arguments = @($verifier.FullName)
        if ($source.Contains('parser.add_argument("--pdf"')) {
            $arguments += @("--pdf", $pdf[0].FullName)
        } elseif ($source.Contains("sys.argv[1]")) {
            $arguments += $pdf[0].FullName
        }
        $output = & $python @arguments 2>&1
        if ($LASTEXITCODE -ne 0) { throw "$($verifier.Name) failed:`n$($output -join [Environment]::NewLine)" }
    }
    $passed += 1
}
if ($passed -ne 72) { throw "Expected 72 topic checks, ran $passed" }
Write-Output "topic_verifiers=$passed"
Write-Output "A2 PDF verifier suite passed"
