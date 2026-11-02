# dbt must have been run successfully before documentation generation.
docker compose exec dbt dbt docs generate --project-dir /usr/app --profiles-dir /usr/app
if ($LASTEXITCODE -ne 0) { throw 'dbt docs generate failed' }
Write-Host 'Run: docker compose exec dbt dbt docs serve --project-dir /usr/app --profiles-dir /usr/app --host 0.0.0.0 --port 8080'
Write-Host 'Then open: http://localhost:8085'
