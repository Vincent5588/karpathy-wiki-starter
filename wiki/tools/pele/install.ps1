# Install the pinned Pele version used by vault rule W, outside the vault.
# Usage: powershell -ExecutionPolicy Bypass -File wiki\tools\pele\install.ps1
# Location: %LOCALAPPDATA%\pele-render by default; override with env var PELE_RENDER_HOME.
# Re-running reinstalls exactly the version pinned in package-lock.json.
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = if ($env:PELE_RENDER_HOME) { $env:PELE_RENDER_HOME } else { Join-Path $env:LOCALAPPDATA 'pele-render' }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { Write-Error '[pele-install] npm not found; install Node.js 22+ first'; exit 1 }
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item (Join-Path $here 'package.json'), (Join-Path $here 'package-lock.json') -Destination $dest -Force
Push-Location $dest
try {
  npm ci --omit=dev --no-audit --no-fund
  if ($LASTEXITCODE -ne 0) { throw "npm ci failed ($LASTEXITCODE)" }
  $v = (Get-Content (Join-Path $dest 'node_modules\pele\package.json') -Raw | ConvertFrom-Json).version
  Write-Output "[pele-install] installed pele $v -> $dest"
} finally {
  Pop-Location
}
