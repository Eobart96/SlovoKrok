[CmdletBinding()]
param([switch]$CheckOnly)

$ErrorActionPreference = 'Stop'
$ProjectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$Api = 'https://api.github.com/repos/Eobart96/SlovoKrok/releases/latest'

function Invoke-Launcher([string]$Root, [string]$Mode) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root 'scripts\windows\platform.ps1') -Mode $Mode -NoBrowser
    if ($LASTEXITCODE -ne 0) { throw "Launcher failed: $Mode. Previous files are preserved." }
}

function Test-Listening([int]$Port) {
    $client = New-Object Net.Sockets.TcpClient
    try {
        $pending = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        if (-not $pending.AsyncWaitHandle.WaitOne(500)) { return $false }
        $client.EndConnect($pending)
        return $true
    } catch { return $false } finally { $client.Dispose() }
}

$lock = $null
try {
    # Distributed ZIP installations only. Never overwrite a developer checkout.
    if (Test-Path -LiteralPath (Join-Path $ProjectRoot '.git')) {
        throw 'This is a Git working copy. Automatic ZIP updates are disabled here.'
    }
    if ($env:SLOVOKROK_DATA_DIR) {
        if (-not [IO.Path]::IsPathRooted($env:SLOVOKROK_DATA_DIR)) { throw 'Data directory must be absolute.' }
        $dataRoot = [IO.Path]::GetFullPath($env:SLOVOKROK_DATA_DIR)
    } else {
        if (-not $env:LOCALAPPDATA) { throw 'LOCALAPPDATA is unavailable.' }
        $dataRoot = Join-Path $env:LOCALAPPDATA 'SlovoKrok'
    }
    New-Item -ItemType Directory -Force -Path $dataRoot | Out-Null
    $lock = [IO.File]::Open((Join-Path $dataRoot 'update.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Write-Host 'Checking the latest stable SlovoKrok release...'
    try { $release = Invoke-RestMethod -Uri $Api -Headers @{'User-Agent'='SlovoKrok-Updater'; Accept='application/vnd.github+json'} -TimeoutSec 30 }
    catch {
        if ($_.Exception.Response -and [int]$_.Exception.Response.StatusCode -eq 404) {
            Write-Host 'No stable release is published yet. Your installation is unchanged.'
            exit 0
        }
        throw 'Could not check GitHub releases. Check your internet connection and try again.'
    }
    if ($release.draft -or $release.prerelease -or $release.tag_name -notmatch '^v?\d+\.\d+\.\d+$') { throw 'Unsupported release version.' }
    $asset = @($release.assets | Where-Object { $_.name -ceq 'SlovoKrok-windows.zip' })
    if ($asset.Count -ne 1 -or $asset[0].digest -notmatch '^sha256:[a-fA-F0-9]{64}$') {
        throw 'The release needs SlovoKrok-windows.zip with a GitHub SHA-256 digest.'
    }
    $asset = $asset[0]
    if (-not $asset.browser_download_url.StartsWith('https://github.com/Eobart96/SlovoKrok/releases/download/')) { throw 'Unexpected download address.' }
    $marker = Join-Path $ProjectRoot 'installed-release.json'
    if (Test-Path -LiteralPath $marker) {
        $installed = Get-Content -LiteralPath $marker -Raw | ConvertFrom-Json
        if ([version]($installed.tag -replace '^v','') -ge [version]($release.tag_name -replace '^v','')) {
            Write-Host 'This installation is already up to date.'
            exit 0
        }
    }
    Write-Host "Available version: $($release.tag_name)"
    if ($CheckOnly) { exit 0 }
    $parent = Split-Path -Parent $ProjectRoot
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $work = Join-Path $parent ("SlovoKrok-update-" + $stamp + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
    New-Item -ItemType Directory -Path $work | Out-Null
    $archive = Join-Path $work 'release.zip'
    Invoke-WebRequest -UseBasicParsing -Uri $asset.browser_download_url -OutFile $archive -TimeoutSec 180
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ine ($asset.digest.Substring(7))) { throw 'Download checksum mismatch. Nothing was installed.' }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [IO.Compression.ZipFile]::OpenRead($archive)
    $unpack = Join-Path $work 'unpacked'
    try {
        $names = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
        foreach ($entry in $zip.Entries) {
            $name = $entry.FullName.Replace('\','/')
            if ($name -notmatch '^SlovoKrok/' -or $name -match '(^|/)(\.\.|\.git|\.env|data|node_modules|\.venv)(/|$)' -or $name.Contains(':') -or -not $names.Add($name)) { throw 'Unsafe release archive.' }
            $target = [IO.Path]::GetFullPath((Join-Path $unpack $name))
            if (-not $target.StartsWith($unpack + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe archive path.' }
        }
    } finally { $zip.Dispose() }
    [IO.Compression.ZipFile]::ExtractToDirectory($archive, $unpack)
    $newRoot = Join-Path $unpack 'SlovoKrok'
    foreach ($required in @('install.cmd','start.cmd','stop.cmd','update.bat','scripts/windows/platform.ps1','scripts/windows/update.ps1','backend/app/main.py','backend/requirements.lock.txt','frontend/package-lock.json')) {
        if (-not (Test-Path -LiteralPath (Join-Path $newRoot $required) -PathType Leaf)) { throw "Incomplete release: $required" }
    }
    # No dependencies or user data are transferred into the new source tree.
    foreach ($relative in @('.env','backend/.env','frontend/.env.local')) {
        $source = Join-Path $ProjectRoot $relative
        if (Test-Path -LiteralPath $source -PathType Leaf) { Copy-Item -LiteralPath $source -Destination (Join-Path $newRoot $relative) }
    }
    $destination = Join-Path $parent ("SlovoKrok-" + $release.tag_name + '-' + $stamp)
    if (Test-Path -LiteralPath $destination) { throw 'Destination already exists.' }
    Move-Item -LiteralPath $newRoot -Destination $destination
    Invoke-Launcher $destination 'Install'
    Invoke-Launcher $ProjectRoot 'Stop'
    if ((Test-Listening 3000) -or (Test-Listening 8000)) { throw 'Application ports are still occupied. Close the application before updating.' }
    $backup = Join-Path $work 'data-backup'
    New-Item -ItemType Directory -Path $backup | Out-Null
    if ($work.StartsWith([IO.Path]::GetFullPath($dataRoot).TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Backup must be outside the data directory.' }
    # All writers must be stopped; retain SQLite sidecars together with the database.
    Get-ChildItem -LiteralPath $dataRoot -Force | Where-Object { $_.Name -ne 'update.lock' } | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $backup -Recurse -Force
    }
    try { Invoke-Launcher $destination 'Start' }
    catch {
        Invoke-Launcher $destination 'Stop'
        throw "New version could not start. Previous installation: $ProjectRoot . Data snapshot: $backup . Do not restore older code against migrated data without restoring the snapshot."
    }
    @{tag=$release.tag_name; asset_sha256=$asset.digest; previous=$ProjectRoot; data_backup=$backup} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $destination 'installed-release.json') -Encoding UTF8
    Write-Host "Update completed. Use start.cmd and update.bat from: $destination"
    Write-Host "Previous version preserved: $ProjectRoot"
    Write-Host "Data snapshot preserved: $backup"
    Start-Process 'http://127.0.0.1:3000/'
} catch {
    Write-Host "Update stopped: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    if ($lock) { $lock.Dispose() }
}
