"""SQLite demo sink with transactionally idempotent event and window writes.

This intentionally lightweight local demonstration uses SQLite instead of deploying
another database server. For a larger production deployment use a supported DBMS
or a transactional lakehouse sink and design matching transactional semantics.
"""
import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

DB_FILE = Path(os.environ.get("GRIDPULSE_DB", "/opt/project/data/gridpulse.db"))
FAIL_FILE = Path("/opt/project/logs/last_failure.json")


def connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DB_FILE), timeout=30)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=30000")
    return connection


def initialize_database():
    with connect() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS valid_events (
                event_id TEXT PRIMARY KEY,
                meter_id TEXT NOT NULL,
                region TEXT NOT NULL,
                energy_usage_kwh REAL NOT NULL,
                voltage REAL NOT NULL,
                device_status TEXT NOT NULL,
                event_timestamp TEXT NOT NULL,
                usage_category TEXT NOT NULL,
                voltage_status TEXT NOT NULL,
                source_topic TEXT NOT NULL,
                source_partition INTEGER NOT NULL,
                source_offset INTEGER NOT NULL,
                ingested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS quarantine_events (
                source_topic TEXT NOT NULL,
                source_partition INTEGER NOT NULL,
                source_offset INTEGER NOT NULL,
                raw_json TEXT,
                error_reason TEXT NOT NULL,
                ingested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_topic, source_partition, source_offset)
            );
            CREATE TABLE IF NOT EXISTS source_progress (
                source_topic TEXT NOT NULL,
                source_partition INTEGER NOT NULL,
                next_offset INTEGER NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_topic, source_partition)
            );
            CREATE TABLE IF NOT EXISTS energy_windows (
                region TEXT NOT NULL,
                window_start TEXT NOT NULL,
                window_end TEXT NOT NULL,
                reading_count INTEGER NOT NULL,
                total_kwh REAL NOT NULL,
                avg_voltage REAL,
                high_usage_count INTEGER NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (region, window_start, window_end)
            );
        """)


def write_events_batch(batch_df, batch_id, fail_on_offset=-1):
    """One SQL transaction per Spark micro-batch; repeatable on retries."""
    connection = connect()
    started = time.perf_counter()
    valid = rejected = 0
    try:
        connection.execute("BEGIN IMMEDIATE")
        for record in batch_df.toLocalIterator():
            row = record.asDict()
            if int(row["offset"]) == fail_on_offset:
                failure = {
                    "batch_id": batch_id,
                    "topic": row["topic"], "partition": row["partition"],
                    "offset": row["offset"], "event_id": row.get("event_id"),
                    "reason": "Controlled processing failure for recovery demonstration",
                }
                FAIL_FILE.parent.mkdir(parents=True, exist_ok=True)
                FAIL_FILE.write_text(json.dumps(failure, indent=2), encoding="utf-8")
                raise RuntimeError(f"Controlled failure at Kafka offset {fail_on_offset}")

            if row["is_valid"]:
                result = connection.execute("""
                    INSERT OR IGNORE INTO valid_events
                    (event_id, meter_id, region, energy_usage_kwh, voltage,
                     device_status, event_timestamp, usage_category,
                     voltage_status, source_topic, source_partition, source_offset)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["event_id"], row["meter_id"], row["region"],
                    row["energy_usage_kwh"], row["voltage"],
                    row["device_status"], row["event_timestamp"].isoformat(),
                    row["usage_category"], row["voltage_status"],
                    row["topic"], row["partition"], row["offset"],
                ))
                valid += int(result.rowcount > 0)
            else:
                result = connection.execute("""
                    INSERT OR IGNORE INTO quarantine_events
                    (source_topic, source_partition, source_offset, raw_json, error_reason)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    row["topic"], row["partition"], row["offset"],
                    row["raw_json"], row["validation_error"],
                ))
                rejected += int(result.rowcount > 0)

            connection.execute("""
                INSERT INTO source_progress(source_topic, source_partition, next_offset)
                VALUES (?, ?, ?)
                ON CONFLICT(source_topic, source_partition) DO UPDATE SET
                  next_offset = MAX(next_offset, excluded.next_offset),
                  updated_at = CURRENT_TIMESTAMP
            """, (row["topic"], row["partition"], int(row["offset"]) + 1))
        connection.commit()
        elapsed = max(time.perf_counter() - started, 0.001)
        print(f"[EVENT SINK] batch={batch_id} new_valid={valid} "
              f"new_quarantine={rejected} duration={elapsed:.2f}s "
              f"throughput={(valid + rejected) / elapsed:.1f} rows/sec", flush=True)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def write_windows_batch(batch_df, batch_id):
    """Output finalized (watermarked) regional windows; UPSERT is idempotent."""
    connection = connect()
    count = 0
    try:
        connection.execute("BEGIN IMMEDIATE")
        for record in batch_df.toLocalIterator():
            row = record.asDict()
            connection.execute("""
                INSERT INTO energy_windows
                (region, window_start, window_end, reading_count,
                 total_kwh, avg_voltage, high_usage_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(region, window_start, window_end) DO UPDATE SET
                  reading_count = excluded.reading_count,
                  total_kwh = excluded.total_kwh,
                  avg_voltage = excluded.avg_voltage,
                  high_usage_count = excluded.high_usage_count,
                  updated_at = CURRENT_TIMESTAMP
            """, (
                row["region"], row["window_start"].isoformat(),
                row["window_end"].isoformat(), row["reading_count"],
                row["total_kwh"], row["avg_voltage"], row["high_usage_count"],
            ))
            count += 1
        connection.commit()
        if count:
            print(f"[WINDOW SINK] batch={batch_id} finalized_windows={count}", flush=True)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
