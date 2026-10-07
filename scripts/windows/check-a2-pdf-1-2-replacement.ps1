$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$oldPdf = Join-Path $root "output\pdf\A2\Module_01\Slovak_A2_Tema_1_2_Nastoyashchee_vremya.pdf"
$newPdf = Join-Path $root "output\pdf\A2\Module_01\Slovak_A2_Tema_1_2_Vid_glagola.pdf"
$roadmap = Join-Path $root "course-content\slovak-a2\learning\learning_roadmap.md"

if (Test-Path -LiteralPath $oldPdf) { throw "Rejected present-tense PDF still exists" }
if (-not (Test-Path -LiteralPath $newPdf)) { throw "Replacement aspect PDF is missing" }

$roadmapText = Get-Content -LiteralPath $roadmap -Raw
if ($roadmapText -match "PDF 1\.2.+Настоящее время") { throw "Roadmap still assigns present tense to PDF 1.2" }
if ($roadmapText -notmatch "PDF 1\.2.+Вид глагола") { throw "Roadmap does not assign aspect to PDF 1.2" }
if ($roadmapText -notmatch "PDF 4\.1.+Вид в связном рассказе") { throw "Roadmap does not distinguish the later advanced aspect lesson" }

Write-Output "A2 PDF 1.2 replacement verified"
