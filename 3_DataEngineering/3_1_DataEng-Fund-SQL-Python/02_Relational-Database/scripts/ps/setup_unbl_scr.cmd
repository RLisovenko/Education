@echo off
setlocal

REM Author: R.Lisovenko / 01-10-2026
REM Description: Configures PowerShell and unblocks the environment script.

set "START_SCRIPT=%~dp0start_cur_venv.ps1"

powershell.exe -NoProfile -Command ^
"$ErrorActionPreference = 'Stop'; ^
try { ^
    if (-not (Test-Path -LiteralPath $env:START_SCRIPT -PathType Leaf)) { ^
        throw ('Script not found: ' + $env:START_SCRIPT); ^
    }; ^
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force; ^
    Unblock-File -LiteralPath $env:START_SCRIPT; ^
    Write-Host ('CurrentUser policy: ' + (Get-ExecutionPolicy -Scope CurrentUser)); ^
    Write-Host ('Effective policy: ' + (Get-ExecutionPolicy)); ^
    Write-Host ('Unblocked: ' + $env:START_SCRIPT); ^
    exit 0; ^
} catch { ^
    Write-Host ('ERROR: ' + $_.Exception.Message) -ForegroundColor Red; ^
    exit 1; ^
}"

set "SETUP_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %SETUP_EXIT%