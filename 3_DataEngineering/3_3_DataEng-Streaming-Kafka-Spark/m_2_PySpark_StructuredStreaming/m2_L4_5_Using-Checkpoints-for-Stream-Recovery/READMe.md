# m2_L4 — Using Checkpoints for Stream Recovery

**Course:** Streaming Data Pipelines with Kafka and Spark (Edureka / Coursera)  
**Module:** 2 — Stream Processing with PySpark  
**Lab:** Lesson 4 — Using Checkpoints for Stream Recovery  
**Student:** R. Lisovenko  
**Execution / documentation date:** 07 November 2026  
**Status:** **Batch 1 verified end-to-end; Batch 2 published and REC005 observed in Spark. Complete restart/recovery verification remains open.**

> **Documentation scope and provenance.** This is an update to the original pre-lab README using the supplied `checkpoint_stream.py`, the two original README files, the actual terminal outputs shared during setup, and screenshots from the exercise. The complete contents of `producer.py`, `docker-compose.yml`, and `requirements.txt` were **not provided**. Commands that depend on those files are labeled as checks or recommendations, not independently verified. The instructor's source scripts have not been changed in this documentation package. The screenshots were supplied by the learner; this documentation did not execute Docker or Kafka on the learner's computer.

## 1. Objective and result

Apache Spark Structured Streaming uses checkpoint metadata to retain query progress, including consumed Kafka partition offsets. The lab demonstrates publishing events, stopping the streaming reader, and restarting the *same query* with the *same valid checkpoint* so the reader can resume where it left off.

**Result as evidenced on 07.11.2026:**

- **Batch 1:** `producer.py batch1` published `REC001`, `REC002`, `REC003`; all three appear in Spark with offsets `0`, `1`, `2`.
- **Batch 2:** `producer.py batch2` published `REC004`, `REC005` with offsets `3`, `4`; the visible Spark output contains `REC005` at offset `4`.
- **Not yet fully demonstrated in the screenshots:** the exact stop/restart sequence and a complete post-restart view containing `REC004` and `REC005` without reprocessing Batch 1. A new screenshot and checkpoint inspection are needed before declaring the recovery scenario fully verified.

The Kafka offsets quiz answer for this lesson was **“The exact positions of processed records”**. Offsets are per partition; an offset is a position, not a count of workers or a checkpoint path.

## 2. Project files and evidence

The original Lab 4 project was shown as containing:

```text
m_2_PySpark_StructuredStreaming/
└── m2_L4_Using-Checkpoints-for-Stream-Recovery/
    ├── producer.py                  # instructor-supplied Python producer
    ├── checkpoint_stream.py         # instructor-supplied PySpark reader
    ├── docker-compose.yml           # inspect before using docker compose
    ├── requirements.txt             # inspect before installing locally
    ├── checkpoints/                 # preserve: Spark query metadata and offsets
    ├── pic/                         # course images + evidence images
    ├── README.md                    # this expanded report
    └── README.txt                   # step-by-step PowerShell command sheet
```

**Evidence included in this update** (all embedded files are in `pic/`):

| Screenshot | Contents | Interpretation |
|---|---|---|
| [`lab4_vscode_pyspark_imports.png`](pic/lab4_vscode_pyspark_imports.png) | Yellow underlines on `pyspark` imports in VS Code | Motivated local interpreter setup; does not imply Docker Spark is missing |
| [`lab4_instructor_spark_submit_reference.png`](pic/lab4_instructor_spark_submit_reference.png) | Instructor's Maven/Ivy connector resolution | Reference image, **not evidence of our own run** |
| [`lab4_instructor_producer_reference.png`](pic/lab4_instructor_producer_reference.png) | Instructor Batch 1 example | Reference image, **not evidence of our own run** |
| [`lab4_batch1_verified.png`](pic/lab4_batch1_verified.png) | Our producer Batch 1 + Spark rows | **Verified** Kafka publication and Spark output |
| [`lab4_batch2_partial_spark_output.png`](pic/lab4_batch2_partial_spark_output.png) | Our producer Batch 2 + visible Spark row `REC005` | Publication of two records verified, one Spark row visible |
| [`lab4_quiz_kafka_offsets.png`](pic/lab4_quiz_kafka_offsets.png) | Question about Kafka offsets | Correct choice explained in §10 |

The earlier pre-lab README also referenced `./pic/course_using_checkpoints_for_stream_recovery.png` and `./pic/lab4_original_course_files.png`. Those two **original local pictures were not uploaded for this update**; if present in your existing `pic/` directory, keep them. This archive does not replace or delete them.

## 3. Verified software and settings

| Item | Observed / known value | Evidence or limitation |
|---|---|---|
| Operating environment | Windows PowerShell, VS Code, virtual environment `.venv` | Visible in terminal screenshots |
| Docker Spark image | `apache/spark:3.5.7` | Container inspection / `spark-submit --version` from older Spark container |
| Spark version | `3.5.7` (Scala 2.12.18, Java 11.0.27) | `spark-submit --version` output |
| Lab 4 Spark container | `checkpoint-recovery-spark` | Used in course-matching execution screenshots / command |
| Prior lab Spark container | `windowed-aggregation-spark` | Lab 3; do not confuse its project mount with Lab 4 |
| Kafka image | `apache/kafka:3.9.1` | Docker container `kafka-local` |
| Shared Docker network | `runningapachekafkalocally_default` | Network inspection originally confirmed for `windowed-aggregation-spark` and `kafka-local`; Lab 4 network should be checked separately |
| Kafka internal listener | `kafka-local:29092` | `KAFKA_ADVERTISED_LISTENERS=HOST://localhost:9092,DOCKER://kafka-local:29092` |
| Kafka topic | `checkpoint-orders` | Actual Spark Python source and producer console |
| Spark Kafka package | `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7` | Explicit `--packages` in `spark-submit` |
| Lab 4 Python script | `/opt/project/checkpoint_stream.py` | Actual Spark submission path |
| Checkpoint directory | `/opt/project/checkpoints` | Explicit in `checkpoint_stream.py` |
| Output sink | `console`, `append`, `truncate=false` | Explicit in `checkpoint_stream.py` |
| `startingOffsets` | `earliest` | Applies on initial query start **without** a checkpoint |

### Actual reader logic (from the supplied Python file)

The `checkpoint_stream.py` file creates `SparkSession(appName='CheckpointStreamRecovery', master='local[*]')`, reads Kafka JSON, and parses these fields:

```python
schema = StructType([
    StructField('order_id', StringType(), True),
    StructField('customer', StringType(), True),
    StructField('amount', DoubleType(), True),
    StructField('status', StringType(), True),
])
```

The output adds Kafka `partition`, `offset` and `timestamp`. The stream uses:

```python
.option('kafka.bootstrap.servers', 'kafka-local:29092')
.option('subscribe', 'checkpoint-orders')
.option('startingOffsets', 'earliest')
# ...
.option('checkpointLocation', '/opt/project/checkpoints')
```

These settings were read from the provided file, not inferred from the instructor screenshot.

## 4. Windows / VS Code — local library configuration

There are **two separate Python environments**:

1. **Windows `.venv`** for running `producer.py`, VS Code completion, and (optionally) local code analysis.
2. **Docker Spark Python** for running the Structured Streaming reader with `spark-submit`.

Installing in one environment does **not** automatically install packages in the other.

### 4.1 Create/activate the Windows environment

PowerShell commands, from the Lab 4 directory:

```powershell
py -0p                                     # show installed Python versions
# If Python 3.12 is available:
py -3.12 -m venv .venv
# If already created, do not recreate it.
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
```

The source README mentioned Python 3.12. The session confirms use of an activated `.venv`, **not its precise Python version**. Use Python 3.11 or 3.12 for reliable compatibility with PySpark 3.5.7; avoid treating Python 3.14 as verified for this version.

### 4.2 Install project requirements (the preferred method)

```powershell
Get-Content .\requirements.txt
python -m pip install -r .\requirements.txt
python -c "from kafka import KafkaProducer; print('KafkaProducer OK')"
python -m pip show kafka-python
```

`producer.py` imports `from kafka import KafkaProducer`. `kafka-python` is the relevant dependency; installing from the real `requirements.txt` is preferred to guessing a version. **The content of that requirements file was not supplied**, so this README does not assert its exact pinned versions.

### 4.3 Optional local PySpark installation for VS Code underlines

The VS Code editor showed unresolved `pyspark.sql` imports. The Docker environment was already working; these underlines can be caused by selecting a Windows interpreter without PySpark. If you want those imports resolvable **in the Windows `.venv`**, run:

```powershell
python -m pip install pyspark==3.5.7
python -c "from pyspark.sql import SparkSession; from pyspark.sql.functions import col, from_json; from pyspark.sql.types import StructType, StructField, StringType, DoubleType; print('All imports OK')"
```

`py4j` is installed automatically as a PySpark dependency. Do **not** install `col`, `from_json`, `StructType`, `StructField`, `StringType`, or `DoubleType` separately. Do not install the mismatched `pyspark==3.5.6` previously proposed during troubleshooting; Docker uses **3.5.7**. `pandas` and `pyarrow` are optional for other workloads and are **not required by this provided script**.

In VS Code select **Python: Select Interpreter** → `.venv\Scripts\python.exe`. Use `python -m pip ...` in an activated environment so the dependency is installed for the same interpreter.

![Unresolved PySpark imports in VS Code before local environment alignment](./pic/lab4_vscode_pyspark_imports.png)

## 5. Docker configuration and PySpark diagnostic history

### 5.1 Inspect containers and bind mounts

```powershell
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
docker inspect checkpoint-recovery-spark --format '{{json .Mounts}}'
docker inspect checkpoint-recovery-spark --format '{{json .NetworkSettings.Networks}}'
docker inspect kafka-local --format '{{json .NetworkSettings.Networks}}'
docker exec kafka-local sh -c "env | grep KAFKA_ADVERTISED_LISTENERS"
```

**Important historical finding:** the previous `windowed-aggregation-spark` mounted the **Lesson 3** folder at `/opt/project`, not the Lesson 4 folder. When `/opt/project/checkpoint_stream.py` was missing, we temporarily copied the Lab 4 script to `/tmp/checkpoint_stream.py` in that old container. That workaround is **not** the recommended final design. Lesson 4 uses its own container and `/opt/project/checkpoint_stream.py`; verify its mount independently.

If `checkpoint-recovery-spark` already exists, **do not create a duplicate**. If it does not exist, prefer the supplied Lab 4 Compose configuration after inspecting it:

```powershell
docker compose config --services
docker compose config
# Only if the actual service is named 'spark':
docker compose up -d spark
```

An alternative manual creation **only when Compose is not being used and the name is free** (the course folder must be the current `$PWD`):

```powershell
docker run -d --name checkpoint-recovery-spark --network runningapachekafkalocally_default -v "${PWD}:/opt/project" -w /opt/project apache/spark:3.5.7 tail -f /dev/null
```

The manual command is a reproducible setup option, **not proof that this exact creation command was executed**. Never remove existing Kafka volumes or use `docker compose down -v` to debug the streaming job.

### 5.2 Docker PySpark import issue — verified fix

In the older Spark container, direct `python3 -c "import pyspark"` gave `ModuleNotFoundError: pyspark` despite Spark being installed. Its source files existed in `/opt/spark/python/pyspark`; after adding that path, the next error was `ModuleNotFoundError: py4j`. The ZIP dependency existed under `/opt/spark/python/lib/py4j-0.10.9.7-src.zip`.

**Verified on `windowed-aggregation-spark`:**

```powershell
docker exec -e PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.7-src.zip windowed-aggregation-spark python3 -c "import pyspark, py4j; print('PySpark:', pyspark.__version__); print('Py4J: OK')"
```

Observed:

```text
PySpark: 3.5.7
Py4J: OK
```

Imports were then verified:

```powershell
docker exec -e PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.7-src.zip windowed-aggregation-spark python3 -c "from pyspark.sql import SparkSession; from pyspark.sql.functions import col, from_json; from pyspark.sql.types import StructType, StructField, StringType, DoubleType; print('All imports OK')"
```

Observed: `All imports OK`. A later real `SparkSession` test returned **`SparkSession OK: 3.5.7`**, with harmless `NativeCodeLoader` and Spark UI port 4040/4041 warnings.

**Do not install PySpark into the Docker image to fix this.** For the lab reader, `/opt/spark/bin/spark-submit` sets up Spark's Python environment itself; explicitly setting `PYTHONPATH` is only useful for manual `python3 -c` diagnostics. `grep` as a filter of a PowerShell pipeline will not work: use `Select-String` on Windows, or run `sh -c '... | grep ...'` entirely in the Linux container.

### 5.3 Spark Kafka connector is not bundled in the image

The prior Spark container had no `*kafka*.jar` under `/opt/spark`. Use the version-matched connector dynamically with `--packages`:

```powershell
docker exec -it checkpoint-recovery-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/checkpoint_stream.py
```

Ivy/Maven may download its transitive dependencies on the first run. A successful `--version` invocation alone does **not** verify Kafka connectivity or streaming.

![Instructor reference: Kafka package resolution (not our own execution proof)](./pic/lab4_instructor_spark_submit_reference.png)

## 6. Kafka connectivity and offsets

The **verified advertised listeners** were:

```text
KAFKA_ADVERTISED_LISTENERS=HOST://localhost:9092,DOCKER://kafka-local:29092
```

- Producer running in Windows connects to a host-mapped listener (the exact `producer.py` config was not supplied; earlier labs used `localhost:9092`).
- Spark running in Docker uses `kafka-local:29092` on a common Docker network.
- A shared Docker network and correct advertised listener are both necessary; the Lab 4 container's network should be verified by `docker inspect`.

To inspect Kafka topic offsets:

```powershell
# earliest available offset
docker exec kafka-local /opt/kafka/bin/kafka-get-offsets.sh --bootstrap-server kafka-local:29092 --topic checkpoint-orders --time -2
# log-end offset (next position to be assigned)
docker exec kafka-local /opt/kafka/bin/kafka-get-offsets.sh --bootstrap-server kafka-local:29092 --topic checkpoint-orders --time -1
```

**Observed before Batch 2:**

```text
checkpoint-orders:0:0     # earliest offset = 0
checkpoint-orders:0:3     # end offset = 3
```

That means offsets `0`, `1`, `2` were available in partition `0` at that observation point. The `3` is the **next offset**, not an additional existing record. Batch 2 subsequently published offsets `3` and `4`; a later `--time -1` value was **not provided**.

## 7. Run the lab — exact successful commands

Use **two PowerShell terminals** inside the Lab 4 directory, with the `.venv` active on the Windows producer side.

### Terminal LEFT — Spark Structured Streaming reader

```powershell
docker exec -it checkpoint-recovery-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/checkpoint_stream.py
```

Leave this process running for the initial publication. The script prints:

```text
STRUCTURED STREAMING CHECKPOINT RECOVERY
Connected to Kafka topic: checkpoint-orders
Checkpoint directory: /opt/project/checkpoints
Waiting for order events...
```

**Caveat:** these lines are Python `print()` output and do not alone prove a successful Kafka connection; verify actual rows in the console.

### Terminal RIGHT — publish Batch 1

```powershell
python .\producer.py batch1
```

The observed run reported `BATCH1 published successfully` and published three records at offsets `0–2`.

### Batch 1: verified result

| Order | Customer | Amount | Status | Partition | Offset | Kafka timestamp shown |
|---|---|---:|---|---:|---:|---|
| REC001 | Asha | 1250.50 | CREATED | 0 | 0 | 2026-11-07 19:48:17.749 |
| REC002 | Rahul | 899.00 | PAID | 0 | 1 | 2026-11-07 19:48:19.989 |
| REC003 | Meera | 2100.75 | CREATED | 0 | 2 | 2026-11-07 19:48:21.994 |

![Lab 4 — own evidence: Spark received all three Batch 1 records](./pic/lab4_batch1_verified.png)

### Stop and publish Batch 2

To test recovery, stop the Spark reader with `Ctrl+C` in the **left** terminal, but keep the Kafka broker running. Do not delete, edit, or move the checkpoint directory. Publish new records in the **right** terminal:

```powershell
python .\producer.py batch2
```

Observed producer result:

```text
Published REC004 | Partition: 0 | Offset: 3
Published REC005 | Partition: 0 | Offset: 4
BATCH2 published successfully.
```

For a checkpoint recovery test, re-run **the exact same `spark-submit` command** (same script, topic, query options and checkpoint path) in the left terminal.

### Batch 2: what the screenshot demonstrates

| Order | Customer | Amount | Status | Partition | Offset | Evidence |
|---|---|---:|---|---:|---:|---|
| REC004 | Not visible in available Spark frame | — | — | 0 | 3 | Producer published successfully; Spark row not visible in supplied image |
| REC005 | Neha | 2450.25 | SHIPPED | 0 | 4 | Producer published; Spark row visible at 2026-11-07 20:05:35.879 |

![Lab 4 — own evidence: Batch 2 published; REC005 visible in Spark](./pic/lab4_batch2_partial_spark_output.png)

**Documentation status:** the screenshot shows meaningful continuation of the flow, but by itself does not prove the same checkpoint was reused after an intentional interruption or that all records were handled exactly once. In particular, `REC004` may be outside the captured viewport. Record a full post-restart console or checkpoint log evidence before checking off the recovery criterion.

## 8. Checkpoint files, stale-offset error and safe recovery

The Windows `checkpoints/` folder was inspected. Observed directory entries included:

```text
checkpoints/
├── commits/
├── offsets/
├── sources/
├── metadata
└── .metadata.crc
```

The user also received a Spark error stating that data may have been lost because previously recorded Kafka offsets were unavailable. That error can arise when a checkpoint refers to offsets unavailable in the current topic (for example, after topic recreation or retention), but the supplied log fragment does **not** prove which cause applied in this run. Existing checkpoint metadata had older timestamps, so stale state was a plausible explanation, not a confirmed diagnosis.

**Inspect without modifying:**

```powershell
Get-ChildItem .\checkpoints -Recurse -Force
Get-ChildItem .\checkpoints\offsets -File | Where-Object { $_.Name -match '^\d+$' } | Sort-Object { [int64]$_.Name } | Select-Object -Last 3 | ForEach-Object { "=== offsets/$($_.Name) ==="; Get-Content $_.FullName }
Get-ChildItem .\checkpoints\commits -Name
```

If you are intentionally starting a **new demonstration**, and **only after stopping** the Spark reader, you may archive an incompatible checkpoint under a different name, then let Spark initialize a new one:

```powershell
# Only for a deliberate FRESH run; this is NOT recovery of old state:
Rename-Item .\checkpoints ("checkpoints_backup_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
```

This discards the old query's resumption position for the *new* run (while preserving the files as a backup). **Do not run it as part of the Batch 1 → Batch 2 recovery demonstration.** Also do not casually set `failOnDataLoss=false`: Spark may skip data, which undermines this recovery exercise. `startingOffsets='earliest'` does not override offsets stored in a valid existing checkpoint.

To verify persistence, inspect the Lab 4 container's mount:

```powershell
docker inspect checkpoint-recovery-spark --format '{{json .Mounts}}'
Test-Path .\checkpoints
```

The desired mapping is the **current Lab 4 host directory** → `/opt/project`; then `/opt/project/checkpoints` is preserved on Windows. The actual Lab 4 mount inspection output has **not been supplied**, so this remains a verification item.

## 9. Reproducible end-to-end workflow (short checklist)

1. Open Docker Desktop. Confirm the existing `kafka-local` and `checkpoint-recovery-spark` are running; do not create a second Kafka broker.
2. Confirm Lab 4 `/opt/project` bind mount, shared Kafka Docker network and listener.
3. Activate Windows `.venv`; install the actual `requirements.txt` and verify `KafkaProducer`.
4. Start `checkpoint_stream.py` through Spark with the version-matched Kafka connector.
5. Publish `python .\producer.py batch1`; confirm `REC001`–`REC003` at offsets `0–2` in Spark.
6. Wait for the corresponding Spark microbatch to commit; stop only the Spark application with `Ctrl+C`. Preserve `checkpoints/`.
7. Publish `python .\producer.py batch2` while Spark is stopped; confirm new Kafka offsets.
8. Restart the same script with the same checkpoint; inspect the **full** Spark output and commits/offset logs.
9. Capture evidence for `REC004` and `REC005`, no unexpected replay of committed Batch 1, and no `DataLossException`.
10. Stop Spark safely. Do not delete the checkpoint folder or Kafka volumes.

### Optional resource management (not an observed part of this execution)

The earlier README recommended limits of 2 CPUs / 3 GiB RAM / 4 GiB including swap for **one Spark lab container**, but no output confirming those limits on Lab 4 was supplied. To apply them deliberately:

```powershell
docker update --cpus=2 --memory=3g --memory-swap=4g checkpoint-recovery-spark
docker stats --no-stream checkpoint-recovery-spark kafka-local
```

Stop older Spark lab containers only if they are not doing other work. Do not run `docker compose down -v`.

## 10. Checkpoint recovery concept and quiz

Kafka records have monotonically increasing offsets **within a topic partition**. A Spark checkpoint tracks the progress of a particular streaming query. After a compatible restart, Spark recovers the source position from the checkpoint. In this lab, the recorded offsets were `0–2` for Batch 1, then `3–4` for Batch 2.

**Quiz question:** “What do Kafka offsets help identify in this recovery flow?”  
**Correct answer:** **The exact positions of processed records.**

![Edureka quiz about offsets](./pic/lab4_quiz_kafka_offsets.png)

A checkpoint is **not** a Kafka backup. The console sink is useful for a demonstration, but console output is not a durable production sink; screenshots alone do not establish full end-to-end exactly-once delivery.

## 11. Completion checklist and further evidence

- [x] Spark 3.5.7 and PySpark/Py4J imports verified in the prior Spark container.
- [x] `SparkSession` created successfully (`SparkSession OK: 3.5.7`).
- [x] Kafka 3.9.1 container and advertised internal Kafka address verified.
- [x] Kafka Connector version selected to match Spark 3.5.7.
- [x] Lesson 4 `checkpoint_stream.py` inspected and documented.
- [x] Initial Kafka offsets `0` and log-end `3` checked before Batch 2.
- [x] Batch 1 producer publication and all three Spark rows documented.
- [x] Batch 2 producer publication at offsets `3` and `4` documented.
- [x] Spark output row `REC005` (offset `4`) documented.
- [x] Checkpoint directory structure inspected on Windows.
- [ ] Confirm actual Lab 4 `/opt/project` bind mount with `docker inspect`.
- [ ] Confirm the documented stop and restart sequence with the same checkpoint from full logs/screenshots.
- [ ] Confirm `REC004` in Spark output after restart.
- [ ] Confirm whether previously committed Batch 1 rows were replayed.
- [ ] Save full post-restart proof and checkpoint commit/offset snapshots.

**Final evidence-qualified status:** the data pipeline functions and has processed new events. **Complete checkpoint recovery verification is pending** until the remaining checkpoints above are documented.

---

**R. Lisovenko** — Oldenburg, Deutschland · 07 November 2026  
**Documentation revision:** adds real Batch 1/2 evidence, Docker/PySpark/VS Code troubleshooting, Python dependency setup and corrected PowerShell commands.
