# Run from the project root in PowerShell. Keeps older labs untouched.
docker compose config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Invalid docker-compose.yml' }
docker compose up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Docker Compose startup failed' }
docker compose ps -a
