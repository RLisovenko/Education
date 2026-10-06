@echo off
setlocal

REM Author: R.Lisovenko
REM Checks Python, Git and PostgreSQL.
REM Offers to add PostgreSQL to the permanent USER PATH.

echo === PATH ===
powershell -NoProfile -Command "$env:Path -split ';'"
echo.

echo === Python ===
python --version
where python
echo.

echo === Git ===
git --version
where git
echo.

echo === PostgreSQL ===
where psql >nul 2>&1

if not errorlevel 1 (
    psql --version
    where psql
    goto finish
)

echo psql is not in PATH. Checking installed versions...
echo.

set "FOUND_PSQL="

for /d %%D in ("C:\Program Files\PostgreSQL\*") do (
    if exist "%%D\bin\psql.exe" (
        set "FOUND_PSQL=1"
        "%%D\bin\psql.exe" --version
        echo Found: %%D\bin
        echo.

        choice /C YN /N /M "Add this PostgreSQL to permanent USER PATH? [Y/N]: "

        if errorlevel 2 (
            echo PATH was not changed.
        ) else if errorlevel 1 (
            set "PG_BIN=%%D\bin"

            powershell -NoProfile -Command ^
                "$ErrorActionPreference = 'Stop';" ^
                "$UserPath = [string][Environment]::GetEnvironmentVariable('Path', 'User');" ^
                "$PostgresPath = $env:PG_BIN;" ^
                "if (($UserPath -split ';') -notcontains $PostgresPath) {" ^
                "    $NewPath = ($UserPath.TrimEnd(';') + ';' + $PostgresPath).TrimStart(';');" ^
                "    [Environment]::SetEnvironmentVariable('Path', $NewPath, 'User');" ^
                "}"

            if errorlevel 1 (
                echo ERROR: Could not update USER PATH.
            ) else (
                echo PostgreSQL is now in permanent USER PATH.
                echo Restart your terminal. For VS Code, restart the whole app.
                goto finish
            )
        )
        echo.
    )
)

if not defined FOUND_PSQL (
    echo PostgreSQL was not found in C:\Program Files\PostgreSQL.
)

:finish
echo.
pause
endlocal