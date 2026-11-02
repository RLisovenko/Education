# Troubleshooting — NovaForge Manufacturing Demo

| Symptom | Likely cause | Check / corrective action |
|---|---|---|
| `Bind ... port is already allocated` | Other labs use 8080, 8083, 9000–9003 | Use the NovaForge host ports 8084, 8085, 9004, 9005; check `docker ps`. |
| Docker Compose YAML error | Incorrect indentation or duplicate YAML mapping | `docker compose config --quiet` |
| MinIO image pull denied | `minio/minio:latest` registry unavailable | This project uses `cgr.dev/chainguard/minio:latest` as in the verified prior lab. |
| `minio-init` failed | MinIO not ready or credentials wrong | `docker compose logs minio-init minio`; script retries startup automatically. |
| `docker.from_env()` permission denied | Airflow Worker lacks Docker-socket group access | Check socket group and `DOCKER_GID` in `.env`; use only in a trusted local environment. |
| Airflow shows 0 DAGs | DAG processor stopped or import error | `docker compose exec airflow-dag-processor airflow dags list-import-errors` |
| DAG import fails | Syntax error or missing Python docker package | `python -m py_compile dags/novaforge_manufacturing_lakehouse.py`; check Airflow Dockerfile build. |
| CSV/JSON/Parquet path not found | Incorrect bind mount or Parquet bootstrap not run | Check `/opt/project/data/raw/` inside `novaforge-spark`; Airflow prepares Parquet first. |
| Spark says `Invalid database name: demo.manufacturing` | Iceberg catalog not registered | Check `spark/conf/spark-defaults.conf`, ensure the Spark packages loaded. |
| S3A `path must be absolute` | HadoopCatalog warehouse points to bucket root | Keep `spark.sql.catalog.demo.warehouse=s3a://warehouse/iceberg`, not `s3a://warehouse/`. |
| `NoSuchNamespaceException` | Namespace not created yet | `CREATE NAMESPACE IF NOT EXISTS demo.manufacturing;` |
| `NoSuchBucket` | MinIO bucket initialization missing | Inspect `http://localhost:9005`; rerun `docker compose up -d minio-init`. |
| PostgreSQL `relation ... does not exist` | Database init or Spark stage not executed | Inspect postgres-init and `raw` schema; run full Airflow pipeline in order. |
| `cannot drop table ... because other objects depend on it` | Spark overwrote a PostgreSQL raw table | Use stable raw tables with pre-ingest TRUNCATE + Spark append (implemented). |
| dbt test fails | Data quality or relationship discrepancy | `docker compose exec dbt dbt test --project-dir /usr/app --profiles-dir /usr/app` |
| Iceberg row count unexpected | Bad source filtering or incomplete upstream models | Check `marts.fact_production` and Iceberg count, DAG task logs. |
| dbt docs not available | `dbt docs serve` not running | `docker compose exec dbt dbt docs serve --project-dir /usr/app --profiles-dir /usr/app --host 0.0.0.0 --port 8080` |

## Diagnostic commands

```powershell
docker compose config --quiet
docker compose ps -a
docker compose logs --tail 80 spark postgres minio airflow-worker airflow-dag-processor

docker compose exec airflow-worker python -c "import docker; print(docker.from_env().ping())"
docker compose exec airflow-dag-processor airflow dags list-import-errors

docker compose exec dbt dbt debug --project-dir /usr/app --profiles-dir /usr/app
```

Avoid unnecessary `docker compose down -v`, because it deletes this project's named PostgreSQL and MinIO volumes.
