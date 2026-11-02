# Manual Historical Reprocessing, Catchup and Retries

## Lab implementation

- DAG `novaforge_manufacturing_lakehouse` has `schedule=None`, `catchup=False`.
- Each task retries once after 2 minutes on failure.
- Trigger without conf to process both sample days.
- Trigger with `{"batch_date":"2026-10-30"}` to process one production date.
- The DAG replaces PostgreSQL raw **rows** before Spark appends selected source data. dbt marts are therefore rebuilt from that selected batch.
- Iceberg publishing performs a `MERGE` by `order_id` and retains already published data from other batches. Reprocessing an order updates its current Iceberg row; an Iceberg snapshot records changes.

## Limitations and production improvements

- This simple project **does not implement scheduled Airflow backfill**. To enable it, introduce a daily timetable and a stable partition date from each DAG run. Decide whether `catchup=True` is appropriate before activation.
- Filtering only orders by `batch_date` is a scoped demonstration. Historical corrections in master data (machines, lines and products) would need effective dating and independent snapshots.
- Deletions from source are not propagated automatically by the Iceberg upsert; production pipelines must define delete semantics.
- Use per-period staging tables or partition-aware datasets to avoid temporary loss of other dates in PostgreSQL reporting marts during reprocessing.
- Audit each DAG run and capture source versions, operation counts, errors, retry numbers and snapshot IDs.
- Never trigger overlapping batch runs against the shared PostgreSQL raw tables without serialization or partition isolation.

## Example

An inspection for 2026-10-30 is corrected. Update the synthetic JSON seed and trigger the DAG with `batch_date=2026-10-30`; Spark regenerates Parquet, dbt rebuilds that day's marts, and the Iceberg table merges changed order-level records. Verify the affected rows and new snapshot before accepting results.
