# Coverage of the 12 Course Practice Tasks

This maps the practical assignment to project files. **Provided** means source code/doc is included; **verification remains pending** until local execution.

| Course task | Implementation / evidence location |
|---|---|
| 1 Architecture | `README.md` Section 2; `docs/ARCHITECTURE.md` |
| 2 PySpark CSV/JSON/Parquet transformations | `spark/jobs/bootstrap_quality_parquet.py`, `ingest_manufacturing.py`; `data/` |
| 3 Spark plans/partitions/cache | `spark/jobs/analyze_spark.py` |
| 4 dbt staging/intermediate/marts | `dbt/models/`, `dbt/dbt_project.yml` |
| 5 Fact and dimension models | `dbt/models/marts/`, `docs/DATA_DICTIONARY.md` |
| 6 dbt tests/documentation/lineage | dbt YAML, `dbt/tests/`, `dbt docs generate` |
| 7 Airflow DAG & retries | `dags/novaforge_manufacturing_lakehouse.py` |
| 8 Historical reprocessing/backfill strategy | Optional `batch_date` filtering and `docs/BACKFILL.md`; scheduled backfill not implemented |
| 9 MinIO/Iceberg table, updates/snapshots | `spark/jobs/export_to_iceberg.py`, `iceberg_operations_demo.py` |
| 10 Schema evolution | `spark/jobs/iceberg_operations_demo.py` |
| 11 Small-file management | `spark/jobs/compact_iceberg.py`, `docs/ICEBERG_OPERATIONS.md` |
| 12 E2E validation and evidence | `spark/jobs/validate_lakehouse.py`, `docs/EXECUTION_CHECKLIST.md` |

Engineering constraints: a small local synthetic dataset is **not** evidence of production scalability; the Airflow schedule is deliberately manual; historical Airflow-native catchup/backfill is described but not deployed.
