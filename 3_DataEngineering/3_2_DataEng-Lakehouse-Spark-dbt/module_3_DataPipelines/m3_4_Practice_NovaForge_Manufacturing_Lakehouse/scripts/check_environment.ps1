# Run from the project root in Windows PowerShell.
$ErrorActionPreference = 'Stop'
Write-Host 'Checking Docker Compose configuration...'
docker compose config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Invalid Compose configuration.' }
docker compose ps -a
Write-Host 'Checking source files...'
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Source tests failed.' }
Write-Host 'Open Airflow: http://localhost:8084'
Write-Host 'Open MinIO:  http://localhost:9005'
