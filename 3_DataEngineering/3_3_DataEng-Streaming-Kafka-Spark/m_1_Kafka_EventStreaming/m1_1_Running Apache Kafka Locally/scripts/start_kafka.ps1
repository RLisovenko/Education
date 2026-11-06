# Optional helper: start the single-broker Kafka lab. Run from PowerShell.
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    docker info --format '{{.ServerVersion}}'
    if ($LASTEXITCODE -ne 0) { throw 'Docker Engine unavailable. Open Docker Desktop and wait for Engine running.' }
    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw 'Invalid docker-compose.yml.' }
    docker compose up -d
    if ($LASTEXITCODE -ne 0) { throw 'Kafka startup failed. Check Docker Compose logs.' }
    docker compose ps
} finally {
    Pop-Location
}
