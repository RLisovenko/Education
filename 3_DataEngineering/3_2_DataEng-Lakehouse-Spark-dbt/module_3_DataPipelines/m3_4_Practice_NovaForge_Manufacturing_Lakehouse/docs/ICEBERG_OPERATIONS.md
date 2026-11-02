# Iceberg Operations: History, Schema Evolution and Small Files

## Main table

- Catalog: `demo` (Spark Iceberg HadoopCatalog)
- Namespace: `manufacturing`
- Table: `manufacturing_production_metrics`
- Storage: `s3a://warehouse/iceberg/manufacturing/manufacturing_production_metrics/`
- Merge key: `order_id`

## Safe demo table

`iceberg_operations_demo.py` creates/replaces only `demo.manufacturing.production_quality_events_demo`, updates one row, adds `machine_temperature_avg DOUBLE`, and inspects snapshots. This illustrates changing data and table schema **without altering the main published fact table**.

## SQL inspection

```sql
SELECT COUNT(*) FROM demo.manufacturing.manufacturing_production_metrics;
SELECT snapshot_id, operation, committed_at
FROM demo.manufacturing.manufacturing_production_metrics.snapshots;
DESCRIBE TABLE EXTENDED demo.manufacturing.manufacturing_production_metrics;
```

## Small-file strategy

Monitor number/size of Iceberg Parquet data files. Small batches may create many tiny files; each has metadata and object-store request overhead. Consider coarse partitioning only with evidence of query patterns and record volume, then compact periodically. Optional `compact_iceberg.py` calls `demo.system.rewrite_data_files` on the **separate demo table**. For a small sample it may rewrite zero files; this is not a failure.

Avoid manual deletion of Iceberg metadata/Parquet files from MinIO. Use Iceberg maintenance operations and snapshot expiration policies, retaining enough history for recovery.
