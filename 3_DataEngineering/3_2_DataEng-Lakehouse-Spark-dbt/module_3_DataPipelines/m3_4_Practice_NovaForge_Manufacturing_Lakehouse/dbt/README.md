# NovaForge dbt Core project

**Profile:** `novaforge` | **Database:** `manufacturing` | **Catalog:** `demo` (for Iceberg only).

- Source: `raw.*` (loaded by PySpark over JDBC)
- Staging: `staging.stg_*` (PostgreSQL views)
- Intermediate: `intermediate.int_production_enriched` (view)
- Marts: `marts.fact_*`, `marts.dim_*`, and `marts.mart_production_daily` (tables)

```powershell
# Execute from the project root after docker compose up -d:
docker compose exec dbt dbt debug --project-dir /usr/app --profiles-dir /usr/app
docker compose exec dbt dbt run --project-dir /usr/app --profiles-dir /usr/app
docker compose exec dbt dbt test --project-dir /usr/app --profiles-dir /usr/app
docker compose exec dbt dbt docs generate --project-dir /usr/app --profiles-dir /usr/app
docker compose exec dbt dbt docs serve --project-dir /usr/app --profiles-dir /usr/app --host 0.0.0.0 --port 8080
```

Documentation UI: <http://localhost:8085> while `dbt docs serve` is running. Lineage is visible in the documentation interface.
