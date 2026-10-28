# Author: R.Lisovenko / 01-10-2026
# Description: Creates and activates the project virtual environment.
# Location: ...Project\scripts\ps\start_cur_venv.ps1
#Путь/НазваниеПроекта/
#├── .venv/
#└── scripts/
#    └── ps/
#        ├── start_cur_venv.ps1
#        ├── check_PATH.cmd
#        └── setup_unbl_scr.cmd
# -----------------------------
# Project paths
# -----------------------------
# -------------------- $ProjectDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Write-Host '1. Scripts are in <Project>\scripts\ps'
Write-Host '2. Scripts are in <Project>\scripts'

$Choice = Read-Host 'Select location (1 or 2)'

$ProjectDir = switch ($Choice) {
    '1' { Split-Path -Parent (Split-Path -Parent $PSScriptRoot) }
    '2' { Split-Path -Parent $PSScriptRoot }
    default { throw 'Invalid selection. Enter 1 or 2.' }
}
# ----------------------------------------------------------------
$VenvPath = Join-Path $ProjectDir '.venv'
$VenvPython = Join-Path $VenvPath 'Scripts\python.exe'
$ActivateScript = Join-Path $VenvPath 'Scripts\Activate.ps1'

Set-Location $ProjectDir

Write-Host ""
Write-Host "Project directory:"
Write-Host $ProjectDir
Write-Host ""

# -----------------------------
# If .venv already exists
# -----------------------------

if (Test-Path $VenvPython) {

    Write-Host "Existing virtual environment found:"
    Write-Host $VenvPath
    Write-Host ""

    Write-Host "Python version:"
    & $VenvPython --version

    Write-Host ""
    Write-Host "Activating .venv..."
    . $ActivateScript

    Write-Host ""
    Write-Host "Virtual environment activated."
    exit
}

# -----------------------------
# Find Python interpreters
# -----------------------------

$Pythons = @()

function Add-PythonInterpreter {
    param (
        [string]$Path
    )

    if (
        $Path -and
        (Test-Path $Path) -and
        ($Path -notmatch 'WindowsApps') -and
        ($Pythons -notcontains $Path)
    ) {
        $script:Pythons += $Path
    }
}

# Python from PATH
try {
    $PythonCmd = (Get-Command python.exe -ErrorAction Stop).Source
    Add-PythonInterpreter $PythonCmd
}
catch {}

# Python Launcher
try {
    $PyLauncher = (Get-Command py.exe -ErrorAction Stop).Source

    $PyVersions = & $PyLauncher -0p 2>$null

    foreach ($Line in $PyVersions) {
        if ($Line -match '([A-Za-z]:\\.+python\.exe)') {
            Add-PythonInterpreter $Matches[1]
        }
    }
}
catch {}

# Common local Python installations
$LocalPythonDir = Join-Path $env:LOCALAPPDATA 'Programs\Python'

if (Test-Path $LocalPythonDir) {
    Get-ChildItem $LocalPythonDir -Recurse -Filter python.exe -ErrorAction SilentlyContinue |
        ForEach-Object {
            Add-PythonInterpreter $_.FullName
        }
}

# Common Anaconda installations
$AnacondaPaths = @(
    'C:\dev_soft\Anaconda3_2023\python.exe',
    'C:\ProgramData\Anaconda3\python.exe',
    "$env:USERPROFILE\anaconda3\python.exe"
)

foreach ($Path in $AnacondaPaths) {
    Add-PythonInterpreter $Path
}

# -----------------------------
# No Python found
# -----------------------------

if ($Pythons.Count -eq 0) {
    Write-Host "ERROR: Python interpreter not found."
    Write-Host "Install Python and run this script again."
    exit 1
}

# -----------------------------
# Show available interpreters
# -----------------------------

Write-Host "Available Python interpreters:"
Write-Host ""

for ($i = 0; $i -lt $Pythons.Count; $i++) {

    $Version = & $Pythons[$i] --version 2>&1

    Write-Host "$($i + 1). $Version"
    Write-Host "   $($Pythons[$i])"
    Write-Host ""
}

# -----------------------------
# Select Python
# -----------------------------

if ($Pythons.Count -eq 1) {

    $SelectedPython = $Pythons[0]

    Write-Host "Only one Python interpreter found."
    Write-Host "Selected automatically:"
    Write-Host $SelectedPython
}
else {

    $Choice = Read-Host "Select Python number"

    if ($Choice -notmatch '^\d+$') {
        Write-Host "ERROR: Invalid selection."
        exit 1
    }

    $Index = [int]$Choice - 1

    if ($Index -lt 0 -or $Index -ge $Pythons.Count) {
        Write-Host "ERROR: Invalid selection."
        exit 1
    }

    $SelectedPython = $Pythons[$Index]
}

Write-Host ""
Write-Host "Selected Python:"
Write-Host $SelectedPython

Write-Host ""
Write-Host "Version:"
& $SelectedPython --version

# -----------------------------
# Create virtual environment
# -----------------------------

Write-Host ""
Write-Host "Creating virtual environment:"
Write-Host $VenvPath

& $SelectedPython -m venv $VenvPath

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to create virtual environment."
    exit 1
}

# -----------------------------
# Activate virtual environment
# -----------------------------

if (-not (Test-Path $ActivateScript)) {
    Write-Host ""
    Write-Host "ERROR: Activate.ps1 was not created."
    exit 1
}

Write-Host ""
Write-Host "Activating .venv..."

. $ActivateScript

Write-Host ""
Write-Host "Virtual environment activated."

Write-Host ""
Write-Host "Active Python:"
python --version

Write-Host ""
Write-Host "Python executable:"
where.exe python

Write-Host ""