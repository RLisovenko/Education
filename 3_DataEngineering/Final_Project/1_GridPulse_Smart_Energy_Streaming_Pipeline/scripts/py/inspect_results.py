"""Inspect trusted events, quarantine and finalized regional windows in SQLite."""
import argparse
import sqlite3
from config import DB_PATH


def show(cursor, title, sql, max_rows):
    rows = cursor.execute(sql).fetchmany(max_rows)
    print(f"\n{title}")
    for row in rows:
        print(" | ".join(str(v) for v in row))
    if not rows:
        print("(no results yet)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    if not DB_PATH.exists():
        print(f"Results database not created yet: {DB_PATH}")
        return
    with sqlite3.connect(str(DB_PATH)) as con:
        for table in ("valid_events", "quarantine_events", "energy_windows"):
            n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {n}")
        show(con, "VALID EVENT SAMPLES", """
            SELECT event_id, meter_id, region, energy_usage_kwh, usage_category
            FROM valid_events ORDER BY ingested_at DESC, source_offset DESC
        """, args.limit)
        show(con, "QUARANTINE", """
            SELECT source_partition, source_offset, error_reason, raw_json
            FROM quarantine_events ORDER BY ingested_at DESC, source_offset DESC
        """, args.limit)
        show(con, "FINALIZED 5-MINUTE WINDOWS", """
            SELECT region, window_start, window_end, reading_count, total_kwh,
                   avg_voltage, high_usage_count
            FROM energy_windows ORDER BY window_start DESC, region
        """, args.limit)


if __name__ == "__main__":
    main()
