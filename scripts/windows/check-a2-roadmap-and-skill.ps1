$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$node = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if (-not (Test-Path -LiteralPath $node -PathType Leaf)) { throw "Bundled Node.js not found: $node" }
& $node (Join-Path $root "scripts\verify-a2-roadmap.mjs")
if ($LASTEXITCODE -ne 0) { throw "Roadmap verifier failed" }
& $node (Join-Path $root "scripts\verify-a2-study-skill.mjs")
if ($LASTEXITCODE -ne 0) { throw "Study-skill verifier failed" }
Write-Output "A2 roadmap and skill checks passed"
