echo Author: R.Lisovenko / 02-10-2026
# Creates a project structure and copies the three helper scripts.
# Place this file beside the helper scripts in universal_scripts.

$ErrorActionPreference = 'Stop'
$ParentDir = Read-Host 'Parent folder path'
$ProjectName = Read-Host 'New project name'

if ([string]::IsNullOrWhiteSpace($ParentDir) -or
    [string]::IsNullOrWhiteSpace($ProjectName) -or
    $ProjectName.IndexOfAny([IO.Path]::GetInvalidFileNameChars()) -ge 0 -or
    $ProjectName -in '.', '..' -or $ProjectName -match '[. ]$') {
    throw 'Enter a valid parent path and project folder name.'
}

$ProjectDir = Join-Path $ParentDir $ProjectName
if (Test-Path -LiteralPath $ProjectDir) {
    throw "Folder already exists: $ProjectDir"
}

$Helpers = 'setup_unbl_scr.cmd', 'start_cur_venv.ps1', 'check_PATH.cmd'
foreach ($File in $Helpers) {
    if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $File) -PathType Leaf)) {
        throw "Place $File beside this script first."
    }
}

foreach ($Folder in 'data', 'notebooks', 'output', 'docs', 'scripts\ps', 'scripts\sql', 'scripts\py') {
    New-Item -ItemType Directory -Path (Join-Path $ProjectDir $Folder) -Force | Out-Null
}

foreach ($File in $Helpers) {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $File) -Destination (Join-Path $ProjectDir 'scripts\ps')
}

@'
# Python
.venv/
venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/

# Local secrets
.env
.env.*
!.env.example

# Logs and OS files
*.log
Thumbs.db
.DS_Store
'@ | Set-Content -LiteralPath (Join-Path $ProjectDir '.gitignore') -Encoding UTF8

@'
numpy              # Numerical arrays and calculations
pandas             # Tables and data processing
openpyxl           # Excel .xlsx files
requests           # HTTP requests and APIs
python-dotenv      # Load settings from .env
psycopg[binary]     # PostgreSQL connection
pyodbc             # ODBC connections (requires a database ODBC driver)
'@ | Set-Content -LiteralPath (Join-Path $ProjectDir 'requirements.txt') -Encoding UTF8

@"
# $ProjectName

1. Run scripts\ps\setup_unbl_scr.cmd if PowerShell scripts are blocked.
2. In PowerShell, run .\scripts\ps\start_cur_venv.ps1 and select 1.
3. Install packages: python -m pip install -r requirements.txt
4. Check the environment: .\scripts\ps\check_PATH.cmd

Folders: data, notebooks, output, docs, scripts/ps, scripts/sql, scripts/py.
"@ | Set-Content -LiteralPath (Join-Path $ProjectDir 'README.md') -Encoding UTF8

Write-Host "Created: $ProjectDir"
Write-Host 'Next: run scripts\ps\start_cur_venv.ps1 and select 1.'
