# m2_L4 — Using Checkpoints for Stream Recovery

**Course:** Streaming Data Pipelines with Kafka and Spark (Edureka / Coursera)  
**Module:** 2 — Streaming Processing with PySpark  
**Lab:** Using Checkpoints for Stream Recovery  
**Prepared:** 07 November 2026  
**Status:** **PREPARATION COMPLETE — streaming execution and recovery test NOT YET VERIFIED**

> **Evidence scope.** This pre-lab guide is based on the two supplied screenshots, the verified Kafka/Spark environment from Labs 1–3, and the general behaviour of Spark Structured Streaming. The **contents** of the instructor's `checkpoint_stream.py`, `producer.py`, `docker-compose.yml`, and `requirements.txt` have **not yet been supplied for this lab**. Therefore any exact container name, checkpoint path, topics, sample records, and recovery behaviour must be checked against the original files before declaring the exercise complete. **No instructor source files were modified.**

## 1. Introduction and objective

![Edureka lesson: Using Checkpoints for Stream Recovery](./pic/course_using_checkpoints_for_stream_recovery.png)

In Spark Structured Streaming, a checkpoint stores progress information (such as Kafka source offsets) and, for stateful queries, metadata and state needed for recovery. If the same streaming query restarts with access to its **unchanged, valid checkpoint directory**, Spark can use the saved progress rather than simply treating it as an entirely new query.

**Objective:** understand why checkpoints matter, start a streaming reader connected to Kafka, observe its output, stop the application and restart it with the same checkpoint location, and verify recovery using actual records, Kafka offsets, Spark output, and checkpoint files.

A checkpoint is **not** a backup of the Kafka broker. End-to-end recovery also depends on Kafka retaining the relevant records, a stable query definition, and accessible checkpoint storage. Exactly-once guarantees vary by sink and query and are not established by a screenshot alone.

## 2. Original laboratory files

![Instructor-supplied files for Lab 4](./pic/lab4_original_course_files.png)

The screenshot shows this existing lab directory:

```text
m_2_PySpark_StructuredStreaming/
└── m2_L4_Using-Checkpoints-for-Stream-Recovery/
    ├── checkpoints/                # Local folder visible in the user's screenshot
    ├── pic/
    │   ├── course_using_checkpoints_for_stream_recovery.png
    │   └── lab4_original_course_files.png
    ├── producer.py                 # Supplied by the instructor
    ├── checkpoint_stream.py        # Supplied by the instructor
    ├── docker-compose.yml          # Supplied by the instructor
    ├── requirements.txt            # Supplied by the instructor
    ├── README.md                   # This guide
    └── README.txt                  # Quick PowerShell commands
```

**Important:** The `checkpoints/` directory already exists in the user's lab folder. Do not replace, clear, rename or delete it as part of documentation updates or the recovery experiment.

### Inspect original source settings before execution

Run from the Lab 4 directory in **Windows PowerShell**:

```powershell
Get-Content .\docker-compose.yml
Get-Content .\requirements.txt
Select-String -Path .\checkpoint_stream.py -Pattern 'checkpointLocation|checkpoints|kafka.bootstrap.servers|subscribe|startingOffsets|outputMode|format'
Select-String -Path .\producer.py -Pattern 'bootstrap_servers|producer.send|order_id|event_time|sleep'
docker compose config --services
```

Record these values after inspection:

| Parameter | What to verify | Status |
|---|---|---|
| Docker Compose service | Expected `spark` from Labs 1–3; verify in Lab 4 | Pending |
| Spark container name | Read actual `container_name` in Compose | Pending |
| Spark image/version | Confirm Spark 3.5.7 before using the connector below | Pending |
| Kafka broker | Reuse existing `kafka-local`; do not create another broker | Known from previous labs |
| Kafka source | Check address and topic in `checkpoint_stream.py` | Pending |
| Checkpoint path | Check the precise `checkpointLocation` and whether it is persistent | Pending |
| Kafka Producer payload | Check which messages and timestamps are sent | Pending |
| Output sink and mode | Confirm writer settings in source | Pending |

## 3. Architecture and checkpoint persistence

```text
Windows PowerShell
  producer.py
       |
       | Kafka host port (verify in producer.py; previous labs: localhost:9092)
       v
Existing Kafka broker: kafka-local
       |
       | Docker listener (previous labs: kafka-local:29092)
       v
Lab 4 Spark container
  checkpoint_stream.py
       |
       +------> Streaming output / results
       |
       +------> Checkpoint directory
                (must survive Spark application restarts)
```

If the checkpoint directory is inside the container, it needs a **persistent mount** (or another durable storage arrangement). A path under `/tmp/` in an ephemeral container is not a reliable persistence strategy.

Check the Compose volume mapping carefully. In previous labs, the course provided `./:/opt/project`, meaning `/opt/project/checkpoints` would refer to the host's lab directory, **but this is not yet verified for Lab 4**.

Do **not** manually edit checkpoint log files while Spark is running. Do not change the checkpoint location, delete its contents, or casually change the query schema or sink between recovery runs. Some query changes make an existing checkpoint incompatible.

## 4. Lab environment and preparation

Reuse the Kafka container created in Module 1. Previous successful labs used these resource limits:

| Container | Existing lab resource policy |
|---|---|
| Kafka: `kafka-local` | Up to 2 CPUs, 2 GiB memory, 3 GiB memory + swap |
| One active Spark container | Up to 2 CPUs, 3 GiB memory, 4 GiB memory + swap |

These are **upper limits, not reserved amounts**; they do not prevent overheating. Keep earlier lab Spark containers stopped while testing Lab 4.

### Step 1 — Check Docker Engine and existing Kafka

Open Docker Desktop and wait for the engine to be running. Then:

```powershell
docker ps -a --filter "name=kafka-local"
docker ps --filter "name=kafka-local"
```

Only if Kafka is **stopped**:

```powershell
docker start kafka-local
```

No new Kafka broker is required. Avoid `docker compose down -v` and avoid removing Kafka's data.

### Step 2 — Stop previous lab Spark containers (only if running)

```powershell
docker stop structured-streaming-spark filtering-enrichment-spark windowed-aggregation-spark
```

If one or more containers are already stopped, Docker may print a corresponding message. Do not delete them.

### Step 3 — Verify and start the Lab 4 Compose service

From the Lab 4 directory:

```powershell
docker compose config --services
docker compose config
```

**If** the service listed is `spark`, start it:

```powershell
docker compose up -d spark
docker compose ps
```

Do not assume its exact container name. Obtain the current container ID from the Compose service:

```powershell
$Lab4Spark = docker compose ps -q spark
$Lab4Spark
```

If `$Lab4Spark` is empty, check the Compose service name and current directory instead of guessing a container name.

### Step 4 — Apply reasonable resource limits

```powershell
docker update --cpus=2 --memory=3g --memory-swap=4g $Lab4Spark
docker inspect $Lab4Spark --format 'Name={{.Name}} CPU={{.HostConfig.NanoCpus}} RAM={{.HostConfig.Memory}} SWAP={{.HostConfig.MemorySwap}}'
docker stats --no-stream $Lab4Spark kafka-local
```

The existing Kafka container's previously configured limits are reused; there is no need to recreate it.

### Step 5 — Connect to the existing Kafka Docker network

The previous labs successfully used the Kafka network `runningapachekafkalocally_default`:

```powershell
docker network ls
docker network connect runningapachekafkalocally_default $Lab4Spark
```

If `docker network connect` reports `endpoint ... already exists`, the container is already attached.

Check **name resolution** from the Spark service:

```powershell
docker compose exec spark getent hosts kafka-local
```

A returned IP and `kafka-local` confirms Docker DNS resolution; this is a necessary but not by itself sufficient check of broker connectivity. In previous labs the IP changed, so do not hard-code it.

### Step 6 — Verify checkpoint directory and container mount

```powershell
Test-Path .\checkpoints
docker compose config
docker compose exec spark sh -c 'ls -ld /opt/project /opt/project/checkpoints'
```

The last command assumes the same `/opt/project` mount used in previous labs. **If it fails**, inspect Lab 4's Compose volume and the actual `checkpointLocation` in `checkpoint_stream.py`; do not create a different path blindly.

The checkpoint directory must be the **same persistent location** for both execution runs.

## 5. Running and demonstrating recovery

Use **two VS Code PowerShell terminals**. Open each at the Lab 4 project directory.

### Terminal LEFT — Start Spark Structured Streaming

If the Compose file uses `apache/spark:3.5.7`, run:

```powershell
docker compose exec spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/checkpoint_stream.py
```

This adds the compatible Spark Kafka connector. On the first use within a new container, Maven/Ivy may download dependencies; harmless Hadoop native-library warnings are common. **An application startup message alone does not prove the streaming query has connected to Kafka.**

Leave Spark running while producing data. Wait until the streaming query has started without connection or checkpoint errors.

### Terminal RIGHT — Publish the first batch of events

Use the host Python launcher from the Lab 4 directory:

```powershell
py .\producer.py
```

If `kafka` cannot be imported, inspect `requirements.txt` first. Earlier labs used `kafka-python==2.2.15`; for that same requirement:

```powershell
py -m pip install kafka-python==2.2.15
```

If you already configured a local Python 3.12 `.venv`, you may use its interpreter instead. Docker contains Spark; installing PySpark on Windows is not necessary solely to run `spark-submit` in the container.

Record actual producer event IDs, Kafka partition IDs and offsets, and Spark batch output. **Do not invent expected offsets.** If the application starts at `latest` on a new checkpoint, messages produced before the query is ready may be skipped.

### Recovery test — Stop and restart the Spark application

1. **While Spark is running**, capture the first observed results and inspect which files are created in `checkpoints/`.
2. Stop only the **Spark application** in the left terminal using **Ctrl+C**. Keep Kafka and the Docker container running.
3. Confirm the checkpoint directory and its contents still exist. **Do not clear it.**
4. Optionally run `py .\producer.py` again while Spark is stopped to generate a second batch (this is appropriate if the source code and Kafka retention allow it). Running the Producer again can repeat sample event IDs while creating new Kafka offsets.
5. Restart the **same** Spark script with the **same** checkpoint location and compatible source/sink/query settings using the exact Spark command above.
6. Compare recovered output with published Kafka offsets and the first run. Verify that subsequent data is processed and inspect whether already committed data is replayed. Do not claim exactly-once delivery unless the sink supports it and the observed evidence confirms it.

Check the local checkpoint directory without modifying it:

```powershell
Get-ChildItem .\checkpoints -Force
Get-ChildItem .\checkpoints -Recurse -Force | Select-Object -First 30 FullName
```

**Caution:** Spark stores checkpoint data per query. Creating a new query or moving the checkpoint path is not the same as restoring the previous stream.

## 6. Evidence to capture

The files already provided for this README document the **course topic and initial directory structure**, not a completed recovery run.

Add execution screenshots to the existing `pic/` folder as the lab proceeds:

| Suggested filename | Evidence | Currently available |
|---|---|---|
| `lab4_docker_containers_and_dns.png` | Kafka + Spark running, successful `getent hosts kafka-local` | No |
| `lab4_initial_spark_stream.png` | First Spark run and streaming batches | No |
| `lab4_first_producer_run.png` | First Producer run and offsets | No |
| `lab4_checkpoint_directory.png` | Checkpoint files after first run | No |
| `lab4_recovery_restart.png` | Re-started query using same checkpoint | No |
| `lab4_recovery_result.png` | Processing after recovery, with offsets | No |

When available, embed screenshots here using relative paths, for example:

```markdown
![Spark query after checkpoint recovery](./pic/lab4_recovery_result.png)
```

Do not mark the recovery experiment successful based only on a successful `spark-submit` start.

## 7. Troubleshooting

| Symptom | Likely cause / safe next step |
|---|---|
| `No such container` when using `docker exec` | Create the Lab 4 Spark service with `docker compose up -d spark`; determine the actual container name/ID. |
| `kafka-local` DNS resolution failure | Attach Spark to `runningapachekafkalocally_default`, then run `getent hosts kafka-local` inside Spark. |
| `Failed to find data source: kafka` | Supply the `spark-sql-kafka-0-10_2.12:3.5.7` connector for a Spark 3.5.7 image. |
| No streaming events | Check Kafka connectivity, query readiness, topic and `startingOffsets`; launch Producer after Spark is ready. |
| `py` command fails | Check `py -0p` and use the installed Python launcher rather than assuming `python` exists. |
| Checkpoint not found after restart | Inspect actual `checkpointLocation` and verify the container volume is mapped to persistent host storage. |
| Checkpoint incompatible with modified query | Restore the original compatible query settings; do not delete the checkpoint as a first troubleshooting step. |
| Spark cannot write checkpoint data | Verify filesystem ownership, permissions, available disk space, and volume path. |
| Unusually high CPU/fan noise | Stop the job and confirm other Spark/Airflow stacks are shut down; check temperatures and resource limits. |

## 8. Key concepts

| Term | Role |
|---|---|
| **Checkpoint** | Persistent metadata about query progress and, when needed, state for recovery. |
| **Source offset** | Position within a Kafka partition. |
| **StreamingQuery** | The running Spark Structured Streaming application. |
| **Restart/recovery** | Continue a compatible query using its previously persisted checkpoint. |
| **State store** | Maintains data required for stateful operators; some stateful queries also persist it in checkpoint storage. |
| **Checkpoint persistence** | Storage must survive application restarts and be accessible to the restarted query. |
| **Fault tolerance** | Coordinated handling of recoverable failures; exact delivery semantics depend on source, sink and query. |

## 9. Completion checklist

- [x] Lesson title confirmed from the screenshot.
- [x] Original visible Lab 4 filenames and `checkpoints/`/`pic/` folders recorded.
- [x] Preliminary PowerShell and Docker procedures prepared based on the existing lab environment.
- [x] Two supplied screenshots included in `pic/`.
- [ ] Original Lab 4 scripts and Compose settings inspected.
- [ ] Kafka and Lab 4 Spark DNS/network checked.
- [ ] Checkpoint path and persistent mount verified.
- [ ] First run: Producer events and Spark output captured.
- [ ] Checkpoint data preserved after stopping the reader.
- [ ] Restart with same checkpoint performed.
- [ ] Recovery behaviour confirmed from logs, Kafka offsets and Spark output.
- [ ] Final execution screenshots included.

**Lab status: README files prepared; actual stream recovery not yet verified.**

---

**R. Lisovenko**  
**Deutschland · 07 November 2026**
