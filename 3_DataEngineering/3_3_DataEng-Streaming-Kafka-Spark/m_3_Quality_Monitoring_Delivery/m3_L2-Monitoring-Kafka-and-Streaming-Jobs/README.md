# m3_L2 — Monitoring Kafka and Streaming Jobs

**Module:** 3 — Quality, Monitoring, and Delivery  
**Lab2:** Monitoring Kafka and Streaming Jobs  
**Executor:** LiR.  
**Status:** Prepared for execution — results pending  
**Documentation date:** 08 November 2026

## 1. Objective

Monitor the progress and operational behavior of a Kafka-based streaming application. The exercise uses three Python programs: an event producer, a Kafka consumer acting as a streaming job, and a separate consumer-lag monitor. The goal is to observe how new messages, committed consumer offsets, processing throughput, and backlog relate to each other.

**Important:** Despite the general lesson title, the provided `streaming_job.py` is a **Python Kafka consumer**, not an Apache Spark application. No Spark container or Kafka–Spark connector is required for this lab.

### Processing flow

```text
                    Kafka broker: kafka-local
Python producer.py -- localhost:9092 --> topic: monitoring-orders
                                               |
                                               v
                                  streaming_job.py
                                  group: order-streaming-job
                                  reads messages and commits offsets
                                               |
                                               v
                                      Console metrics

kafka_monitor.py -- Kafka Admin API + end_offsets -->
    latest offset / committed group offset / consumer lag / status
```

## 2. Project files

```text
m3_L2-Monitoring-Kafka-and-Streaming-Jobs/
├── README.md                 # Detailed execution guide
├── README.txt                # Quick PowerShell command reference
├── kafka_monitor.py          # Lag and offset monitor
├── streaming_job.py          # Python Kafka consumer / streaming job
├── producer.py               # Generates eight sample order events
├── requirements.txt          # kafka-python==2.2.15
├── .venv/                    # Local virtual environment (not committed)
└── pic/
    ├── lab2_project_directory_2026-11-08.png
    └── ...                   # Add verified execution screenshots here
```

![Lab 2 project directory](./pic/lab2_project_directory_2026-11-08.png)

The original Python scripts and requirements are preserved without changes. Place the four supplied source files in this folder using their normal filenames (`producer.py`, not an upload suffix such as `producer(4).py`).

## 3. Original implementation

| File | Configuration / behavior |
|---|---|
| `producer.py` | Connects to `localhost:9092`; publishes `MON001` through `MON008` to `monitoring-orders` with a one-second pause between messages; prints partition and actual offset. |
| `streaming_job.py` | Consumes `monitoring-orders` in group `order-streaming-job`; uses `auto_offset_reset="earliest"` and `enable_auto_commit=True`; shows processed events and rate. |
| `kafka_monitor.py` | Reads the end offset for **partition 0**, checks the **committed offset** of group `order-streaming-job`, and prints lag and a simple status every three seconds. |
| `requirements.txt` | `kafka-python==2.2.15` |

### Kafka Monitor status thresholds

In the supplied monitor, `lag = max(latest_offset - consumer_offset, 0)`.

| Consumer lag | Displayed status |
|---:|---|
| `0` | `HEALTHY` |
| `1–3` | `PROCESSING` |
| `4 or more` | `LAGGING` |

These labels are **lab-defined thresholds**, not Kafka's built-in broker-health classifications. The monitor covers partition **0 only**; if additional partitions are introduced, its reported lag is not the full consumer-group lag.

The streaming job's displayed `Rate` is the number of records processed since the process started divided by elapsed wall-clock time; it is **not** an instantaneous throughput metric. The Kafka consumer commits offsets automatically, so committed progress may briefly lag behind records already displayed as processed.

## 4. Environment preparation

Use **Windows PowerShell** in the folder containing the original scripts. Reuse the already configured `kafka-local` container; do not create a second broker or start unrelated Spark/Airflow stacks.

### Step 1 — Start Kafka only if needed

```powershell
docker ps -a --filter "name=kafka-local"
# Only if the existing broker is stopped:
docker start kafka-local
# Verify it is running:
docker ps --filter "name=kafka-local"
```

### Step 2 — Prepare Python 3.12

```powershell
# Create once from the lab directory:
py -3.12 -m venv .venv

# Install from the unmodified requirements file:
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt

# Verify Python Kafka clients:
.\.venv\Scripts\python.exe -c "from kafka import KafkaProducer, KafkaConsumer; from kafka.admin import KafkaAdminClient; print('Kafka monitoring dependencies OK')"
```

Using `.\.venv\Scripts\python.exe` avoids PowerShell activation-policy problems and ensures all three programs use the same environment. Select `.venv\Scripts\python.exe` as the VS Code Python interpreter if needed.

### Step 3 — Verify or create the topic

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Create only if missing; --if-not-exists does not reset an existing topic:
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic monitoring-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic monitoring-orders --bootstrap-server localhost:9092
```

The single-partition configuration matches `kafka_monitor.py`, which explicitly monitors `PARTITION = 0`.

## 5. Lab execution — three VS Code terminals

All three terminals must use the same Lab 2 working directory. **Do not type the producer command into an active consumer or monitor terminal.**

### Terminal 1 — Start the streaming job

```powershell
.\.venv\Scripts\python.exe .\streaming_job.py
```

Wait until the console says `MONITORED STREAMING JOB` and `Waiting for streaming events...`. The process continues running until stopped with `Ctrl+C`.

### Terminal 2 — Start the monitor

```powershell
.\.venv\Scripts\python.exe .\kafka_monitor.py
```

The monitor periodically displays:

```text
Topic            : monitoring-orders
Partition        : 0
Latest Offset    : ...
Consumer Offset  : ...
Consumer Lag     : ...
Status           : HEALTHY / PROCESSING / LAGGING
```

The consumer group should be established by the running streaming job before monitoring starts. If an initial lookup fails, verify the broker and group are available, then restart the monitor.

### Terminal 3 — Publish the test data

```powershell
.\.venv\Scripts\python.exe .\producer.py
```

The producer submits eight orders and finishes automatically.

| Order ID | Customer | Amount |
|---|---|---:|
| MON001 | Asha | 1200.00 |
| MON002 | Rahul | 850.50 |
| MON003 | Meera | 2100.00 |
| MON004 | Vikram | 675.25 |
| MON005 | Neha | 1450.00 |
| MON006 | Arjun | 3200.50 |
| MON007 | Priya | 990.00 |
| MON008 | Karan | 1850.75 |

### Expected behavior (not yet verified)

1. The producer confirms publication of all eight records, with partition and actual offsets.
2. The streaming job displays each consumed record and cumulative processed count and rate.
3. The monitor periodically compares the latest partition offset with the consumer group's committed offset.
4. Consumer lag may briefly rise while new records are arriving and later decrease after the consumer processes and commits them.

**Offset note:** Kafka offsets are persistent log positions. A new topic typically starts at offset 0, but a reused topic may have higher offsets. They must be recorded from the actual output, not assumed.

### Optional controlled lag observation

For a clearer demonstration of backlog, let the consumer group establish and commit progress, then stop **only** `streaming_job.py` using `Ctrl+C`. Keep the monitor running, publish another batch with `producer.py`, and observe how the latest offset advances while the group's committed offset remains behind. Restart `streaming_job.py` to observe catch-up. Do not delete the topic or reset consumer-group offsets.

## 6. Verification commands

Run these in a **free PowerShell terminal**:

```powershell
# Broker and topic:
docker ps --filter "name=kafka-local"
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic monitoring-orders --bootstrap-server localhost:9092

# Current committed group offsets and lag, where available:
docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-streaming-job
```

The Kafka CLI and the Python monitor may show different snapshots during active processing; compare timestamps and refresh after auto commits.

## 7. Troubleshooting

| Symptom | Checks / action |
|---|---|
| `NoBrokersAvailable` / connection refused | Confirm Docker Desktop, `kafka-local`, and the host listener on `localhost:9092`. |
| `No module named kafka` | Install `requirements.txt` using the same `.venv` interpreter used to run the scripts. |
| Nothing appears in the streaming job | Check topic name, broker state, consumer group and whether the producer ran; existing committed offsets override `earliest`. |
| Monitor shows lag while job printed events | Auto-committed group offsets can update later than the consumer's console output. |
| Monitor stays at `LAGGING` | Check that the streaming job is running and committing; examine topic/partition assignments and processing errors. |
| `HEALTHY` with no new work | Lag 0 indicates no committed backlog for monitored partition 0; it does not mean that every part of a production pipeline is healthy. |
| Monitor and job disagree | Monitor samples every 3 seconds; job output is continuous and commit intervals differ. |

## 8. Evidence to capture after execution

Save actual VS Code screenshots in `pic/`:

- `monitoring_producer_eight_events.png` — producer event offsets.
- `monitoring_streaming_job_processing.png` — processed records and event rate.
- `monitoring_consumer_lag.png` — monitor offsets, lag, and status.
- `monitoring_three_terminals.png` — optional overview showing job, monitor, and producer together.

Only insert screenshots and measured offsets after the real run. This document currently contains **setup and expected results**, not claims of completed execution.

## 9. Safe shutdown

1. Use `Ctrl+C` in the Monitor terminal.
2. Use `Ctrl+C` in the Streaming Job terminal.
3. The Producer exits by itself.
4. If Kafka will not be used for the next activity, `docker stop kafka-local`.

Do not delete the Kafka container, topics, or persisted broker data. Exclude `.venv/` from version control.

## Conclusion

This exercise demonstrates basic operational visibility for Kafka event processing: producer activity, consumer throughput, committed offsets, and consumer lag. Monitoring multiple signals and their trends is more informative than relying on a single health label.

**Execution status:** Prepared; awaiting measured output and screenshots.
