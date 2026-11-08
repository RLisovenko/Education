# GridPulse — Scenario Requirements & Evidence Matrix

**Date:** 2026-11-08  
**Final test cycle:** T01–T10 complete within test-specific scopes. The [source scenario](../Scenario.md) was not edited. See [test execution](test_execution_2026-11-08.md) and [final report](final_test_report_2026-11-08.md).

| # | Scenario area | Implementation / observed evidence | Status |
|---:|---|---|---|
| 1 | Streaming architecture | [Architecture](architecture.md), Kafka → Spark → SQLite | Documented |
| 2 | Smart-meter event design | JSON event schema, producer modes | Implemented |
| 3 | Kafka partitions | 3 partitions verified on existing broker | Verified |
| 4 | Produce meter readings | Baseline, late, advance, burst 100 | Verified |
| 5 | Consume/inspect Kafka | T07: 15 events, offsets/keys/partitions across 0/1/2 | Verified (single inspector) |
| 6 | Spark read from Kafka | Streaming driver, event sink batches 1, 6, 7, 8 observed | Verified |
| 7 | Filter/enrich events | Uppercase region, usage/voltage categories | Verified via samples |
| 8 | Window aggregation | 5-min tumbling windows; 15 final rows at end | Verified |
| 9 | Late events/watermark | 2-minute watermark, recent late included; very late excluded from earlier finalized window | Verified for supplied case |
| 10 | Data quality | Quarantine reasons; final 12 invalid records | Verified |
| 11 | Checkpoint recovery | T08: confirmed stopped interval, 12 buffered events, recovery lag 12 → 0 | Verified (event sink) |
| 12 | Reliable outputs / retries | T09: SQLite transactional rollback, event-sink idempotent retry | Verified for tested failure |
| 13 | Monitoring | T10: 135 valid / 12 quarantine / 15 windows / lag 0 / HEALTHY | Verified snapshot |
| 14 | Burst/backpressure | T10: 100-event burst at 41.2 rows/s, eventual lag 0; longer overload limit not measured | Partially verified: 100-event burst; sustained overload not tested |
| 15 | Failure and clean restart | T09: forced exception at P0 offset 9 + `last_failure.json` + successful replay | Verified |
| 16 | End-to-end validation | Baseline, late/advance, checkpoint restore, rollback/retry, burst | Verified within demonstrated scope |

**Important qualifications:** Event and window sinks have separate checkpoints/transactions; global atomic exactly-once behaviour was not tested. T10 actual volume was 100, whereas an earlier planned procedure mentioned 200. The raw consumer inspection used one group member; rebalancing with multiple concurrent inspector consumers was not demonstrated.
