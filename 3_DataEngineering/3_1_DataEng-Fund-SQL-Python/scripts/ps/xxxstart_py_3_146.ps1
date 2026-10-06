# Author: R.Lisovenko / 01-10-2026
# Description: Creates and activates the project virtual environment.

# Settings
#$BasePython = 'C:\dev_soft\Anaconda3_2023\python.exe'
$BasePython = 'C:\Users\rusla\AppData\Local\Programs\Python\Python314\python.exe'
echo $BasePython
$ProjectDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
echo $ProjectDir
$VenvPath = Join-Path $ProjectDir '.venv'
$VenvPython = Join-Path $VenvPath 'Scripts\python.exe'
$ActivateScript = Join-Path $VenvPath 'Scripts\Activate.ps1'

$PreviousErrorActionPreference = $ErrorActionPreference

try {
    $ErrorActionPreference = 'Stop'

    if (-not (Test-Path -LiteralPath $VenvPath)) {
        if (-not (Test-Path -LiteralPath $BasePython -PathType Leaf)) {
            throw "Base Python not found: $BasePython"
        }

        Write-Host "Creating virtual environment: $VenvPath"
        & $BasePython -m venv $VenvPath

        if ($LASTEXITCODE -ne 0) {
            throw "Virtual environment creation failed. Exit code: $LASTEXITCODE"
        }
    }

    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        throw "Virtual environment Python not found: $VenvPython"
    }

    if (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
        throw "Activation script not found: $ActivateScript"
    }

    & $VenvPython -c "import sys; sys.exit(0 if sys.prefix != sys.base_prefix else 1)"

    if ($LASTEXITCODE -ne 0) {
        throw 'Virtual environment validation failed.'
    }

    Set-Location -LiteralPath $ProjectDir
    . $ActivateScript

    Write-Host ''
    Write-Host "Virtual environment activated: $VenvPath"
    & $VenvPython --version
    Write-Host "Python executable: $VenvPython"
}
finally {
    $ErrorActionPreference = $PreviousErrorActionPreference
}