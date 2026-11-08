# GridPulse — Streaming Schema and Validation Rules

**Event fields:** `event_id` (string), `meter_id` (string), `region` (string), `energy_usage_kwh` (double), `voltage` (double), `device_status` (string), `event_timestamp` (ISO timestamp string). Kafka key should equal the event `meter_id`.

## Implemented checks (from `scripts/py/spark_pipeline.py`)

| Field | Rule | Error |
|---|---|---|
| JSON payload | Must parse into expected struct | `malformed_json` |
| `event_id` | Non-null and non-empty | `missing_event_id` |
| `meter_id` | Non-null and non-empty | `missing_meter_id` |
| `region` | Non-null and non-empty after trim | `missing_region` |
| Kafka key | Must equal payload `meter_id` | `kafka_key_meter_mismatch` |
| Energy kWh | Number from 0 to 100 inclusive | `invalid_energy_usage_kwh` |
| Voltage V | Number from 190 to 250 inclusive | `invalid_voltage` |
| Device status | `ONLINE`, `OFFLINE`, `MAINTENANCE` | `unsupported_device_status` |
| Timestamp | Parsable by Spark `to_timestamp` | `invalid_event_timestamp` |

Multiple errors are joined with `; `. Region and status are uppercased; `usage_category` is `HIGH` when usage >= 10, else `NORMAL`; `voltage_status` is `NORMAL` for 210–240 V and `CHECK` for otherwise valid values outside this interval.

## Destination behavior

- Any invalid event is stored with raw JSON, topic, partition, offset and reasons in `quarantine_events`. Valid records are stored in `valid_events` with one row per `event_id`.
- Separately, the window query accepts validated events only, applies a two-minute event-time watermark and `dropDuplicatesWithinWatermark(["event_id"])`, then emits append-mode finalized windows.
- **Valid does not mean on-time:** a very late event can remain in `valid_events` but fail to contribute to window aggregates once the watermark has passed.

The three baseline bad-record reasons and the late-event test are documented with screenshot evidence in [test execution](test_execution_2026-11-08.md).
