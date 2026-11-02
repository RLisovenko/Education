# Business Scenario — NovaForge Manufacturing

NovaForge Manufacturing operates plants in Bremen, Oldenburg and Hamburg. Production orders arrive as CSV, machine operation events as JSON Lines, and quality results as Parquet. Additional CSV files describe facilities, production lines, machines, products and maintenance events.

## Business problem

Independent teams use different transformation rules. Quality and runtime reports are inconsistent, machine events are not joined consistently to orders, and historical corrections need repeatable reprocessing.

## Project objective

Develop an orchestrated pipeline that validates and standardizes manufacturing records, implements reusable transformations and analytical models in dbt Core, and publishes a trusted Iceberg table to MinIO. The DAG coordinates processing and tests before the lakehouse output is accepted.

## Validation targets

- Parse CSV, JSON Lines and Parquet.
- Correctly join machine and quality events to production orders.
- Build reusable staging, intermediate, fact and dimension models.
- Execute data tests before publication.
- Publish Iceberg manufacturing metrics and validate record counts/snapshots.
- Demonstrate update, schema evolution and compaction in a **separate** demo table.
- Document retries and manual reprocessing, along with limitations.

All sample identifiers and figures are fictional.
