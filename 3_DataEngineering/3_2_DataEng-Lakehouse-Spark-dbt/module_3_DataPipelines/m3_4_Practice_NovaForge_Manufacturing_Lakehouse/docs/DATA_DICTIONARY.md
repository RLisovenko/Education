# Data Dictionary

All input values are **synthetic**. The project ships 12 orders from 2026-10-30 and 2026-10-31.

| Dataset | Format | Primary grain / ID | Main fields |
|---|---|---|---|
| `production_orders.csv` | CSV | `order_id` | facility_id, line_id, product_id, production_date, production_status, planned_units |
| `machine_operations.jsonl` | JSON Lines | `operation_id` | order_id, machine_id, operation_at, run_minutes, downtime_minutes, energy_consumption_kwh |
| `quality_inspections.parquet/` | Parquet | `inspection_id` | order_id, inspected_units, rejected_units, inspection_at |
| `maintenance_records.csv` | CSV | `maintenance_id` | machine_id, maintenance_date, downtime_minutes, maintenance_type |
| `facilities.csv` | CSV | `facility_id` | facility_name, region |
| `production_lines.csv` | CSV | `line_id` | facility_id, line_name |
| `machines.csv` | CSV | `machine_id` | line_id, machine_type |
| `products.csv` | CSV | `product_id` | product_name, product_family |

The Parquet directory is **generated at runtime** from `data/seed/quality_inspections.jsonl` because this project includes a Spark bootstrap step; it is not pre-generated or merely renamed JSON.

## Metrics

- `actual_units`: sum of inspected units per production order in this simplified demo.
- `rejected_units`: sum of inspected units rejected by quality inspection.
- `defect_rate`: `rejected_units / actual_units`, protected against division by zero.
- `runtime_minutes`: sum of machine run time for the order.
- `downtime_minutes`: sum of machine downtime for the order.
- `production_duration_minutes`: `runtime_minutes + downtime_minutes`.
- `weighted_defect_rate`: daily sum of rejects divided by daily sum of inspected units.

**Important:** `actual_units` is a training proxy inferred from quality-inspection volume, not a production-grade ERP throughput measure. For real facilities, actual produced units must come from trustworthy counters or production completion records.
