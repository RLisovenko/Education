# GridPulse — Executed Test Plan and Final Status

**Date:** 2026-11-08  
**Final status:** **T01–T10 PASS within stated acceptance scopes**. See [execution log](test_execution_2026-11-08.md) and [final report](final_test_report_2026-11-08.md).

| ID | Test | Observed acceptance | Status |
|---|---|---|---|
| T01 | Environment/topic | Kafka broker, Spark connectivity, 3 partitions | PASS |
| T02 | Baseline producer/Spark | 12 messages published; Spark processed event sink | PASS |
| T03 | Validation and quarantine | 8 new valid and 3 invalid with explanations | PASS |
| T04 | Event sink duplicate handling | Repeated event ID did not create second trusted row | PASS (observed) |
| T05 | Late data and watermark | 2 late + 1 future advance, 6 finalized windows | PASS |
| T06 | Lag monitoring | Event-sink lag 0, HEALTHY | PASS |
| T07 | Independent consumer inspection | 15 raw events with partition/key/offset, partitions 0,1,2 | PASS |
| T08 | Checkpoint recovery | Confirm Spark stopped; queue 12 (lag 12); restart; lag 0 | PASS |
| T09 | Controlled failure + clean replay | RuntimeError offset 9, failure JSON, unchanged sink progress, clean restart 35/12, lag 0 | PASS |
| T10 | Burst/catch-up | **100** messages; batch 2.43s / 41.2 rows/s; 135/12, lag 0 | PASS for 100-event burst |

## Actual execution commands

Host commands require an activated `.venv` in the project root; Spark runs in Docker.

```powershell
# Inspect existing raw Kafka records
python .\scripts\py\consumer.py --max-messages 20 --timeout-ms 5000

# T08/T09: stop the actual Spark container; keep Kafka and checkpoints
# Ctrl+C alone did not stop the container Spark processes on the first try.
docker top gridpulse-spark
docker stop gridpulse-spark
docker inspect -f "{{.State.Running}}" gridpulse-spark

# Queue records while the container is confirmed stopped
python .\scripts\py\producer.py --mode baseline
python .\scripts\py\monitor.py --once

# Start container and ONE Spark application without failure flag
docker start gridpulse-spark
docker exec -it gridpulse-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/scripts/py/spark_pipeline.py

# T09 controlled-failure test (separate test run: ONLY after a fresh unconsumed offset is queued):
# append --fail-on-offset 9 to the same spark-submit command;
# monitor rollback and inspect logs/last_failure.json;
# restart normally WITHOUT this flag using unchanged checkpoints.

# T10 actual burst count (100, not the previous draft's 200)
python .\scripts\py\producer.py --mode burst --count 100 --interval 0
python .\scripts\py\monitor.py --once
python .\scripts\py\inspect_results.py
```

## Interpretation and boundaries

- The actual T08 run required `docker stop` after discovering `Ctrl+C` left Spark processes active inside the container.
- `--fail-on-offset 9` was executed when a *new, unprocessed* P0 offset 9 was available. Offsets must be rechecked before replaying this test in a different state.
- Kafka retention and source offsets were preserved; the SQLite event sink transaction was rolled back on injected failure. No checkpoint directories were deleted.
- End-of-test monitoring compares event sink committed SQLite offsets with Kafka end offsets. It does not measure window-stream lag.
- **Backpressure limitation:** The original plan called for 200 burst records and expected possible lag growth; the test actually executed used **100** and established correct processing/catch-up, **not** saturation or long-term overload response.
- Multi-consumer group rebalance and production performance/SLO benchmarking are outside the demonstrated test evidence.

**Safety:** Do not delete `data/`, `checkpoints/` or Kafka topic data; do not use `docker compose down -v` while maintaining these results.
