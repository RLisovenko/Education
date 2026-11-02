# Manufacturing sample sources

- `production_orders.csv` — 12 orders (two batch dates, deliberately mixed status capitalization).
- `machine_operations.jsonl` — 12 machine events in JSON Lines format.
- `quality_inspections.parquet/` — generated from `../seed/quality_inspections.jsonl` automatically by the Airflow `prepare_parquet_source` task. Apache Spark writes a real Parquet dataset directory, not a renamed JSON file.
- `maintenance_records.csv`, `production_lines.csv`, `facilities.csv`, `machines.csv`, `products.csv` — reference and maintenance datasets.

All data is synthetic. Batch dates are **2026-10-30** and **2026-10-31**.
