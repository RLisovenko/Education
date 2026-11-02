# Architecture and Engineering Decisions

## Data flow

`CSV + JSONL + Parquet → Spark Clean/Validate → PostgreSQL raw → dbt staging → dbt intermediate → dbt marts → dbt tests → Spark JDBC → Iceberg (demo.manufacturing) → MinIO warehouse → Spark SQL validation`

Airflow orchestrates seven dependency-ordered tasks. Database transformations occur in PostgreSQL, not inside Spark. This separation demonstrates both distributed ETL and SQL-first transformation engineering.

## Data ownership

- `raw`: Spark-managed, initialized as stable PostgreSQL relations.
- `staging`: simple dbt views over the validated Spark output.
- `intermediate`: aggregates machine events and inspections to order grain before joining to avoid double counting.
- `marts`: tested dimensional/fact/reporting PostgreSQL tables.
- `demo.manufacturing`: Iceberg catalog namespace; the authoritative curated open lakehouse target for this exercise.
- `warehouse/iceberg`: MinIO S3A path containing Iceberg data and metadata.

## Reproducibility

A separate Docker Compose project isolates containers and volumes. The PostgreSQL init SQL pre-creates raw schemas and source tables to prevent a later PySpark `.mode('overwrite')` from dropping dbt dependencies. The DAG truncates *rows*, then Spark appends a fresh source batch. The Iceberg writer uses `MERGE` on `order_id` for idempotent updates to previously published orders.

## Caveats

This is a single-host demonstration with Spark `local[2]` and Docker socket access from Airflow. Scheduling and industrial-scale data volumes are not benchmarked. Transactional consistency across independent PostgreSQL refreshes and Iceberg publishes would require stronger production controls, lineage and monitored retries.
