REM ./check_path.cmd

@echo off
echo Author: R.Lisovenko / 02-10-2026
echo Description: Check development environment.
echo.

powershell -NoProfile -Command "$i=1; $env:Path -split ';' | ForEach-Object { Write-Output ($i.ToString() + '. ' + $_); $i++ }"

python --version
where python
echo.

git --version
where git
echo.

REM set PATH=%PATH%;C:\Program Files\PostgreSQL\17\bin


where psql >nul 2>&1
if errorlevel 1 (
    echo psql is not in PATH. Checking installed versions...
    for /d %%D in ("C:\Program Files\PostgreSQL\*") do (
        if exist "%%D\bin\psql.exe" (
            "%%D\bin\psql.exe" --version
            echo Found: %%D\bin
            echo To add to PATH in CMD, run:
            echo set "PATH=%%D\bin;%%PATH%%"
            echo.
        )
    )
) else (
    psql --version
    where psql
)


pause