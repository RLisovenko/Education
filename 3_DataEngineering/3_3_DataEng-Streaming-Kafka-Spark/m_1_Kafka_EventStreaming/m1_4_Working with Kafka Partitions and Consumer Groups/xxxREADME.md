# m1_4 — Working with Kafka Partitions and Consumer Groups

**Course:** Streaming Data Pipelines with Kafka and Spark  
**Module:** 1 — Event Streaming with Apache Kafka  
**Lab:** Working with Kafka Partitions and Consumer Groups  
**Executor:** R. Lisovenko  
**Prepared:** 06 November 2026  
**Location:** Deutschland  

![Course lab: Working with Kafka Partitions and Consumer Groups](./pic/edureka_lab4_title.png)

## 1. Objective

Learn how **Kafka partitions** distribute keyed order events and how **consumer groups** share partition ownership among consumers. This lab uses the **original Edureka Python files** (`producer.py`, `consumer.py`) and the existing **Apache Kafka 3.9.1** Docker broker from Lab m1_1. We do **not** create a second broker or modify the existing `orders` topic.

**Data flow:** `Python Producer (keyed events) → Kafka topic partitioned-orders (3 partitions) → Consumer A + Consumer B (same group)`

### What this lab demonstrates

- A Kafka **topic** can have multiple **partitions**, enabling parallel consumption.
- Events with the **same key** normally map to the same partition under the same partitioning setup; Kafka orders records **within a partition**, not globally across the topic.
- Members of **one consumer group** divide the assigned partitions between them. A partition is assigned to at most one active member of a given group at a time.
- **Offsets** represent positions *within each partition*. A consumer group's committed offsets determine where it resumes.
- **Consumer rebalancing** can happen when members join, leave, or fail.

## 2. Files and prerequisites

```text
m1_4_Working with Kafka Partitions and Consumer Groups/
├── README.md                  # Detailed instructions and evidence
├── README.txt                 # Quick PowerShell command reference
├── producer.py                # Original Edureka keyed producer
├── consumer.py                # Original Edureka group consumer
├── requirements.txt           # kafka-python==2.2.15
└── pic/
    ├── edureka_lab4_title.png
    └── kafka_2cpu_resource_limits_previous_lab.png
```

**Environment:** Windows, PowerShell, VS Code, Python 3.14 with `py`, Docker Desktop using Linux containers. Kafka is reachable on `localhost:9092`; the existing container name is `kafka-local`.

> **Fujitsu CELSIUS H760 / resource note:** The existing Kafka container was deliberately limited to **2 CPU equivalents**, **2 GiB RAM**, and **3 GiB RAM + swap** in earlier labs because Docker activity increased fan noise. These are training resource limits, **not a thermal-safety guarantee**. Do not run Spark or other laboratory stacks concurrently. Monitor actual CPU temperature and stop if the laptop shows instability. Previous sudden shutdowns warrant hardware diagnosis if they recur.

## 3. Step-by-step execution — Windows PowerShell

All terminal commands below are entered from this **Lab 4 directory**, unless noted. Use **separate VS Code terminals** for consumers and producer.

### Step 1 — Check the existing Docker engine and broker

Start **Docker Desktop** manually and wait for **Engine running**.

```powershell
docker version
docker ps -a --filter "name=kafka-local"
```

If the container is stopped, restart the **existing** broker; don't run another `docker compose up` in this directory:

```powershell
docker start kafka-local
```

Verify the settings and live usage:

```powershell
docker inspect kafka-local --format 'CPU={{.HostConfig.NanoCpus}} RAM={{.HostConfig.Memory}} SWAP={{.HostConfig.MemorySwap}}'
docker stats --no-stream kafka-local
```

**Previously verified limits:**

```text
CPU=2000000000 RAM=2147483648 SWAP=3221225472
```

If these limits are missing, the previously tested update command is:

```powershell
docker update --cpus=2 --memory=2g --memory-swap=3g kafka-local
```

Run it only if appropriate for your system. Avoid starting the broker repeatedly when the fan is unusually loud. The earlier CPU observations (83.79% at startup with 1 CPU, later 5.27% with 2 CPU) were **not a controlled benchmark**; the fall also reflects different startup phases.

![Kafka resource limits verified in the previous lab](./pic/kafka_2cpu_resource_limits_previous_lab.png)

*Evidence from Lab 2, not a new Lab 4 measurement.*

### Step 2 — Create the dedicated three-partition topic

This lab uses **`partitioned-orders`**, *not* the earlier `orders` topic. With one Kafka broker, use replication factor 1.

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic partitioned-orders --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

Inspect the topic:

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic partitioned-orders --bootstrap-server localhost:9092
```

Expected: `PartitionCount: 3`, `ReplicationFactor: 1`, and individual partition entries for `0`, `1`, and `2`.

> If the topic already exists with a different number of partitions, do **not** delete it to fix the mismatch. Check `--describe` first. Kafka can increase partition count but cannot decrease it; increasing partitions may alter the partition chosen for a given key. For this exercise, use 3 partitions before publishing events.

### Step 3 — Verify Python dependencies

The course files use `from kafka import KafkaProducer` and `from kafka import KafkaConsumer`. On this PC, `python` may display **“Python was not found”** because the Windows app alias is active. Use **`py`** instead.

```powershell
py --version
py -m pip show kafka-python
```

If the library is missing from the interpreter you use:

```powershell
py -m pip install -r .\requirements.txt
```

This lab's original `requirements.txt` pins **`kafka-python==2.2.15`**. For dependency isolation you may use a `.venv`, but reuse the confirmed working Python installation if you are only repeating this small exercise.
### Python Kafka Client — Dependency Verification

The `kafka-python` package (version 2.2.15) was successfully installed and verified using Python 3.14.

**Verification command:**

```powershell
py -m pip show kafka-python

### Step 4 — Start Consumer A (Terminal A)

Run this in the **first terminal**:

```powershell
$env:CONSUMER_NAME = "consumer-A"
py .\consumer.py
```

The original script listens to `partitioned-orders` with:

- `group_id="order-processing-group-demo"`
- `auto_offset_reset="earliest"`
- `enable_auto_commit=True`

Expected opening lines:

```text
KAFKA CONSUMER GROUP MEMBER: consumer-A
Waiting for partition assignments and order events...
Press Ctrl+C to stop.
```

### Step 5 — Start Consumer B (Terminal B)

Open a **second terminal** in the same folder:

```powershell
$env:CONSUMER_NAME = "consumer-B"
py .\consumer.py
```

Allow both consumers to join the group and the partition assignment to settle before publishing. The consumers are in the **same group**, so the group's partitions will be shared between them; this does **not** mean that every event is delivered to both consumers.

### Step 6 — Run the keyed Python Producer (Terminal C)

Open a **third terminal**:

```powershell
py .\producer.py
```

The **original course code** sends six synthetic events into `partitioned-orders`:

| Key | Event | Customer | Amount |
|---|---|---|---:|
| `customer-A` | `PORD101` | Asha | 1200 |
| `customer-B` | `PORD102` | Rahul | 850 |
| `customer-C` | `PORD103` | Meera | 2100 |
| `customer-A` | `PORD104` | Asha | 640 |
| `customer-B` | `PORD105` | Rahul | 1750 |
| `customer-C` | `PORD106` | Meera | 990 |

For each event the producer prints its **key**, **partition**, and **offset** after `future.get(timeout=10)` confirms broker acknowledgment. Actual partition assignments and offset values depend on the current topic state and partitioner. Do not copy sample offsets as verified results.

Expected final message:

```text
All partitioned order events published successfully.
```

### Step 7 — Verify consumption and group membership

Consumer A and B together should print the newly published records, indicating their **consumer name, key, partition, and offset**. One consumer might receive more events than the other, depending on assigned partitions and key distribution. Messages from the same partition are delivered to one member at a time within this group.

Check the consumer group while consumers are still running:

```powershell
docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processing-group-demo
```

The command shows topic partitions, committed offsets, log end offsets, lag, and consumer assignments. A small delay is possible before auto-commits become visible.

**Important:** `auto_offset_reset="earliest"` works **only when no committed offset exists** for the group/partition. On repeated runs, the existing group may resume from its saved offsets and **wait for new events**. To test again, keep the consumers open and rerun `py .\producer.py` in Terminal C. That publishes a *new* copy of the same example IDs with new offsets; it is expected in this demo, not production-grade idempotency.

**Save actual Lab 4 screenshots** after successful execution:

```text
pic/kafka_partitioned_topic_description.png
pic/kafka_two_consumers_and_producer.png
pic/kafka_consumer_group_describe.png
```

Then insert these screenshot links into this section of the README; they are intentionally not linked yet because Lab 4 results have **not** been captured.

### Step 8 — Stop safely

Stop **both** Python consumers with **Ctrl+C**, then confirm the producer has exited. The Kafka broker can remain running for the next lab or be stopped:

```powershell
docker stop kafka-local
```

When finished, **Quit Docker Desktop**. Optionally run `wsl --shutdown` if no other WSL workloads are needed. **Do not use** `docker compose down -v` or remove `kafka-local` just to end the session: the original m1_1 Compose file does not define a persistent Kafka data volume.

## 4. Troubleshooting

| Problem | What to check / fix |
|---|---|
| `Python was not found` | Use `py .\producer.py` / `py .\consumer.py` on Windows. |
| `No module named kafka` | Install `kafka-python==2.2.15` for the active Python environment. |
| `NoBrokersAvailable` | Check Docker Desktop is running, `docker ps` includes `kafka-local`, and port 9092 is available. |
| Topic missing | Create only `partitioned-orders` with three partitions as shown above. |
| One consumer has no output | Wait for group assignment, inspect partitions and group, and send more new events. This alone does not prove failure. |
| Old messages do not reappear | Existing group committed offsets override the `earliest` fallback. |
| Repeated IDs after rerun | The producer sends example events again; this exercise does not implement deduplication. |
| Docker name conflict | Reuse the existing `kafka-local`; avoid creating a second broker with the same fixed container name. |
| Fan noise or unexpected shutdown | Stop the lab; resource caps cannot guarantee hardware safety. Investigate thermals/power if instability recurs. |

## 5. Validation checklist

- [x] Original Edureka Python scripts and dependency versions preserved.
- [x] Prior Kafka 3.9.1 broker and resource settings documented.
- [ ] Three-partition topic `partitioned-orders` created and verified locally.
- [ ] Consumer A and Consumer B started with the same group ID.
- [ ] Six keyed events `PORD101`–`PORD106` published successfully.
- [ ] Both consumers' assignments / received events checked.
- [ ] Consumer group status and offsets inspected.
- [ ] Lab 4 screenshots captured and linked.

**Current status: PENDING EXECUTION.** Update to **COMPLETED — SUCCESS** only after the above steps are verified on the local machine.

---

**R. Lisovenko**  
**Deutschland, November 2026**
