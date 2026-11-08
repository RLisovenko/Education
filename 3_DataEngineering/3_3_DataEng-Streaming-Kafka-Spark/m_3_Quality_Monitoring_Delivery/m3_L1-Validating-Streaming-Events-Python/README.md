# m3_L1 — Validating Streaming Events with Python

**Module:** 3 — Quality, Monitoring, and Delivery  
**Lab:** 1 — Validating Streaming Events with Python  
**Executor:** Li R.  
**Date:** 08 November 2026  
**Status:** Prepared for execution; final runtime results not yet recorded.

![Lab topic — Validating Streaming Events with Python](./pic/lab_title_validating_streaming_events.png)

## 1. Objective

Validate Kafka order events in real time with a Python consumer. Each incoming JSON message is checked against required fields, numeric constraints, and the supported order statuses. The validator prints whether the message is valid, provides reasons for rejection, and reports Kafka partition/offset and cumulative validation counts.

This exercise focuses on **data quality at the ingestion stage**. It uses Python and `kafka-python`; Apache Spark is **not required**.

### Data flow

```text
Python Producer                 Existing Kafka broker                  Python Validator
producer.py                    kafka-local                              validator.py
localhost:9092                 topic: validation-orders                localhost:9092
     |                                   |                                    |
     +----- JSON events ---------------->|---- consume and validate -------->|
                                                                          VALID / INVALID
                                                                          failure reasons
                                                                          partition / offset
                                                                          running counters
```

## 2. Project files

```text
m3_L1-Validating-Streaming-Events-Python/
├── producer.py                  # Publishes five predefined JSON test events
├── validator.py                 # Continuously validates consumed Kafka events
├── requirements.txt             # kafka-python==2.2.15
├── README.md                    # Detailed lab documentation
├── README.txt                   # PowerShell command reference
└── pic/
    ├── lab_title_validating_streaming_events.png
    └── lab_source_files.png
```

![Initial lab file listing](./pic/lab_source_files.png)

The supplied Python scripts are retained as the reference implementation. This documentation does not require changing their contents.

## 3. Prerequisites

- Windows PowerShell and Python. Use the available `py` launcher.
- Docker Desktop with the **existing** Kafka container named `kafka-local` running and host port `9092` available.
- The Python package `kafka-python==2.2.15`.
- A topic named `validation-orders` on the existing Kafka broker.
- Run commands from this lab directory; keep the Python validator and producer in separate terminals.

No additional Kafka broker, Spark service, or Docker Compose project is necessary for this exercise.

### Check the existing Kafka broker

```powershell
docker ps -a --filter "name=kafka-local"
```

Start it **only if stopped**:

```powershell
docker start kafka-local
```

Inspect available topics:

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

If `validation-orders` is missing, create it without changing other topics:

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic validation-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Verify the topic configuration:

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic validation-orders --bootstrap-server localhost:9092
```

The command above requests one partition **only when creating a new topic**. An existing topic retains its own configuration; its partition/offset values may differ.

### Python dependency

Check Python and the Kafka client:

```powershell
py --version
py -m pip show kafka-python
```

Install the lab dependency if missing:

```powershell
py -m pip install -r .\requirements.txt
```

For isolation, a Python 3.12 virtual environment may be used instead:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

If the virtual environment is used, replace `py` in the execution commands with `.\.venv\Scripts\python.exe`. There is no need to install PySpark for this lab.

## 4. Validation rules (`validator.py`)

The validator reads JSON records from Kafka topic `validation-orders`, then evaluates the current event using `validate_event(event)`.

| Field | Rule | Failure reason |
|---|---|---|
| `order_id` | Must be present and truthy | `order_id is required` |
| `customer` | Must not be empty or whitespace-only | `customer is required` |
| `amount` | Required | `amount is required` |
| `amount` | Must be a Python `int` or `float` | `amount must be numeric` |
| `amount` | Must be greater than zero | `amount must be greater than zero` |
| `status` | Required | `status is required` |
| `status` | Must be one of the supported status values | `unsupported status: ...` |

**Supported statuses:** `CREATED`, `PAID`, `SHIPPED`, `DELIVERED`, `CANCELLED`.

The function returns a list of validation errors. If the list is empty, the event is marked `[VALID EVENT]`; otherwise it is marked `[INVALID EVENT]`, and each error is printed. The consumer also prints the Kafka partition and offset together with the current valid/invalid counters.

## 5. Predefined test data (`producer.py`)

The producer sends five JSON order events to `validation-orders`, waiting one second between messages:

| Event | Customer | Amount | Status | Expected validation | Expected reason |
|---|---|---:|---|---|---|
| `VAL001` | Asha | 1250.50 | `CREATED` | **VALID** | — |
| `VAL002` | Empty | 899.00 | `PAID` | **INVALID** | `customer is required` |
| `VAL003` | Meera | -250.00 | `CREATED` | **INVALID** | `amount must be greater than zero` |
| `VAL004` | Vikram | 1750.00 | `UNKNOWN` | **INVALID** | `unsupported status: UNKNOWN` |
| `VAL005` | Neha | 2100.00 | `SHIPPED` | **VALID** | — |

**Expected for exactly one clean five-event test:** 2 valid events and 3 invalid events. This is an expectation derived from the scripts, **not a recorded execution result**.

Actual Kafka offsets depend on the broker's previous messages. The `producer.py` script prints the offsets assigned at publish time.

## 6. Execution — two PowerShell terminals

### Terminal 1 — start the validator first

```powershell
py .\validator.py
```

Expected startup text:

```text
PYTHON STREAMING EVENT VALIDATOR
Listening for events from topic: validation-orders
Press Ctrl+C to stop.
```

The validator is a continuous Kafka consumer. It normally keeps running while waiting for new messages; this is intentional.

### Terminal 2 — publish the five events

Open a **separate terminal** in the same lab directory:

```powershell
py .\producer.py
```

The producer should report five published records and finish with:

```text
All validation test events published successfully.
```

### Terminal 1 — inspect validation results

For each received event, check:

- `[VALID EVENT]` or `[INVALID EVENT]` status;
- one or more validation reasons for invalid events;
- `Partition` and `Offset`;
- cumulative `Valid` and `Invalid` counters.

For a clean run containing only the five specified events, the final counters should reach:

```text
Validation Summary -> Valid: 2 | Invalid: 3
```

**Important:** The consumer is configured with `auto_offset_reset="earliest"`, `enable_auto_commit=False`, and **no `group_id`**. It does not commit progress. Restarting the validator can reread retained events already present in the topic, including messages from previous runs. Consequently, counters may exceed `2 / 3`, and a later run can show repeated test IDs. This is expected from the supplied script, not evidence of exactly-once processing.

Stop the validator with **Ctrl+C** to show the final session summary. The producer exits automatically.

## 7. Screenshot evidence

The included images document the lab topic and initial file layout. They are **pre-execution evidence only**.

After a successful run, save additional screenshots such as:

```text
pic/validation_producer_published.png
pic/validation_consumer_valid_invalid.png
pic/validation_final_summary.png
```

Add their relative Markdown links here only once the files are available. Replace the **Prepared for execution** status with a verified result only after reviewing the actual terminal output.

## 8. What this lab demonstrates — and what it does not

| Implemented | Not implemented in the supplied scripts |
|---|---|
| JSON event production and consumption using `kafka-python` | Spark Structured Streaming transformations |
| Required-field, amount, and status checks | Dead-letter topic or quarantine storage |
| Per-event valid/invalid reporting | Persistence of rejected events |
| Kafka partition and offset reporting | Consumer group offset commits / checkpoints |
| In-memory session-level validation counters | Deduplication or durable exactly-once processing |

The invalid events are **reported to the console**, not automatically removed from Kafka or redirected to a DLQ. The exercise therefore demonstrates event validation, not a complete production data-quality workflow.

## 9. Troubleshooting

| Symptom | Action |
|---|---|
| `NoBrokersAvailable` / connection refused | Confirm Docker Desktop is running, `kafka-local` is Up, and Kafka is reachable on host port 9092. |
| `No module named 'kafka'` | Install `kafka-python==2.2.15` in the interpreter used to run the script. |
| Producer finishes, validator prints nothing | Check the topic name `validation-orders`, broker address `localhost:9092`, and the consumer terminal. |
| More than five events appear | The consumer begins at `earliest` without committed offsets; older messages may be replayed. |
| Duplicate order IDs appear after rerunning Producer | Each execution sends new Kafka records with the same predefined IDs. |
| Terminal does not return to the PowerShell prompt | The validator is a long-running consumer; stop it using Ctrl+C. |

## 10. Conclusion

This laboratory establishes a basic event-validation stage for a Kafka pipeline. The Python validator applies structural and business-rule checks, distinguishes valid from invalid records, and exposes the original Kafka position of each event. It forms a foundation for later work on quarantine handling, dead-letter queues, monitoring, and reliable downstream delivery.

**Execution status:** Pending terminal verification.
