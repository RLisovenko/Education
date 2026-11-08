"""Observe Kafka end offsets and the locally committed event-sink progress.

Kafka's Spark source does not expose a normal committed consumer-group offset,
so the comparison here uses SQLite source_progress recorded by the event sink.
"""
import argparse
import sqlite3
import time
from pathlib import Path
from kafka import KafkaConsumer, TopicPartition
from config import BOOTSTRAP_HOST, DB_PATH, TOPIC


def inspect_once(consumer):
    partitions = consumer.partitions_for_topic(TOPIC)
    if not partitions:
        print(f"Topic {TOPIC!r} not available yet")
        return
    tps = [TopicPartition(TOPIC, n) for n in sorted(partitions)]
    end_offsets = consumer.end_offsets(tps)
    progress = {}
    valid = rejected = windows = recent = 0
    if DB_PATH.exists():
        try:
            with sqlite3.connect(str(DB_PATH), timeout=5) as con:
                progress = {partition: nxt for partition, nxt in con.execute(
                    "SELECT source_partition, next_offset FROM source_progress "
                    "WHERE source_topic = ?", (TOPIC,))}
                valid = con.execute("SELECT COUNT(*) FROM valid_events").fetchone()[0]
                rejected = con.execute("SELECT COUNT(*) FROM quarantine_events").fetchone()[0]
                windows = con.execute("SELECT COUNT(*) FROM energy_windows").fetchone()[0]
                recent = con.execute("""
                    SELECT (SELECT COUNT(*) FROM valid_events WHERE ingested_at >= datetime('now', '-60 seconds'))
                         + (SELECT COUNT(*) FROM quarantine_events WHERE ingested_at >= datetime('now', '-60 seconds'))
                """).fetchone()[0]
        except sqlite3.OperationalError:
            print("Waiting for database tables to become available")
    total_lag = 0
    print("=" * 72)
    print(f"GridPulse monitoring | topic={TOPIC}")
    for tp in tps:
        latest = end_offsets[tp]
        next_offset = progress.get(tp.partition, 0)
        lag = max(latest - next_offset, 0)
        total_lag += lag
        print(f"partition={tp.partition} next_offset={next_offset} "
              f"end_offset={latest} event_sink_lag={lag}")
    status = "HEALTHY" if total_lag == 0 else "PROCESSING" if total_lag < 50 else "LAGGING"
    print(f"status={status} total_lag={total_lag} "
          f"valid={valid} quarantined={rejected} finalized_windows={windows} "
          f"recent_unique_events_per_minute={recent}")
    print("Lag is measured at the idempotent event sink; it is not Spark's Kafka consumer-group lag.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()
    consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_HOST, enable_auto_commit=False)
    try:
        while True:
            inspect_once(consumer)
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
