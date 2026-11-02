# Local Execution Checklist — to be completed during testing

**Status: PENDING.** This project was packaged before Docker end-to-end testing.

- [ ] `docker compose config --quiet` has no errors.
- [ ] Images build and all long-running containers are Up/healthy.
- [ ] Init containers finish with code 0.
- [ ] Airflow available on http://localhost:8084.
- [ ] MinIO Console available on http://localhost:9005, bucket `warehouse` exists.
- [ ] `novaforge_manufacturing_lakehouse` appears without import errors.
- [ ] `prepare_parquet_source` produces real Parquet files.
- [ ] Spark processes and validates 12 production orders and related records.
- [ ] dbt `run` creates staging, intermediate and mart relations.
- [ ] dbt `test` succeeds.
- [ ] Iceberg table `demo.manufacturing.manufacturing_production_metrics` exists.
- [ ] Spark SQL returns 12 production metrics records after first full run.
- [ ] Iceberg snapshot query succeeds.
- [ ] All **7 Airflow tasks** show Success.
- [ ] dbt Docs lineage view can be opened on http://localhost:8085.
- [ ] Optional history/schema evolution script succeeds on demo table.
- [ ] Optional compaction script behavior recorded (including zero-file rewrite).
- [ ] Date-scoped replay tested (`batch_date=2026-10-30`).
- [ ] Screenshots saved in `pic/`.

## Evidence

Record actual timestamps, commands, row counts, snapshot IDs and environment-specific fixes here after testing. Do not mark items complete before verification.
