m1_4 — Working with Kafka Partitions and Consumer Groups
R. Lisovenko | 06.11.2026
STATUS: CORE LAB COMPLETE; optional controlled rebalance + CLI assignment capture remain unverified.

IMPORTANT: Use PowerShell and 'py' (NOT 'python'). Run the Python commands
from the folder containing this README.txt, producer.py and consumer.py.
The existing Kafka Docker container is kafka-local. Do not create a second broker.

======================================================================
A. ONE-TIME PREPARATION — ANY FREE TERMINAL
======================================================================

# Start Docker Desktop manually; wait for "Engine running".
docker ps -a --filter "name=kafka-local"
# ONLY if kafka-local is stopped:
docker start kafka-local

# Verify Kafka CPU/RAM quota and resource use:
docker inspect kafka-local --format 'CPU={{.HostConfig.NanoCpus}} RAM={{.HostConfig.Memory}} SWAP={{.HostConfig.MemorySwap}}'
docker stats --no-stream kafka-local
# Expected quotas: CPU=2000000000 RAM=2147483648 SWAP=3221225472
# ONLY if quotas are missing and appropriate for this laptop:
docker update --cpus=2 --memory=2g --memory-swap=3g kafka-local

# Python prerequisites:
py --version
py -m pip show kafka-python
# ONLY if the package is missing:
py -m pip install -r .\requirements.txt

# Create topic if missing; safe if it already exists:
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic partitioned-orders --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
# Verify PartitionCount 3 and ReplicationFactor 1:
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic partitioned-orders --bootstrap-server localhost:9092

======================================================================
B. BASIC EXERCISE — ONE PRODUCER AND TWO CONSUMERS
======================================================================

TERMINAL 1 — Consumer-1 (START FIRST; leave running):
$env:CONSUMER_NAME="Consumer-1"; py .\consumer.py

TERMINAL 2 — Consumer-2 (START SECOND; leave running):
$env:CONSUMER_NAME="Consumer-2"; py .\consumer.py

TERMINAL 3 — Producer (RUN AFTER THE TWO CONSUMERS):
py .\producer.py

Expected: producer reports 6 published orders PORD101...PORD106.
Observed initial routing: customer-A -> partition 1; customer-B/C -> partition 2.
Consumer-1 received PORD101/PORD104; Consumer-2 the other four.

======================================================================
C. EXTENDED EXERCISE — TWO PRODUCERS, THREE CONSUMERS (5 PANES)
======================================================================

TERMINAL 3 — Consumer-1 (START FIRST; leave running):
$env:CONSUMER_NAME="Consumer-1"; py .\consumer.py

TERMINAL 4 — Consumer-2 (START SECOND; leave running):
$env:CONSUMER_NAME="Consumer-2"; py .\consumer.py

TERMINAL 5 — Consumer-3 (START THIRD; leave running):
$env:CONSUMER_NAME="Consumer-3"; py .\consumer.py

TERMINAL 1 — Producer-1 (run when all consumers are ready):
py .\producer.py

TERMINAL 2 — Producer-2 (run at about the same time):
py .\producer.py

IMPORTANT:
- Each Consumer runs in the SAME group: order-processing-group-demo
  (configured inside consumer.py).
- CONSUMER_NAME is only a DISPLAY LABEL and does not choose partitions.
- Kafka assigns each partition to ONE consumer at a time within the group.
- Partition 0 received no messages from our example keys. A consumer assigned
  to it may show no output; this is normal.
- Both Producers write to the same topic. Repeating runs appends new records
  and new offsets; repeated PORD IDs are not automatically deduplicated.
- Different consumer windows may show a partition in output from DIFFERENT
  moments after group changes. This is not evidence of simultaneous ownership.

======================================================================
D. VERIFY GROUP ASSIGNMENTS — FREE PRODUCER TERMINAL
======================================================================

docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processing-group-demo

docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processing-group-demo --members --verbose

The last command is needed to verify CURRENT partition assignments.
This was NOT captured in the documented runs.

======================================================================
E. OPTIONAL REBALANCE TEST — NOT YET VERIFIED
======================================================================

1) Check current assignments (section D).
2) Ctrl+C in Consumer-2 terminal only.
3) Check assignments again in a free Producer terminal (section D).
4) py .\producer.py
5) See how the remaining consumers receive new events.

======================================================================
F. FINISH SAFELY
======================================================================

Stop each Consumer with Ctrl+C. Producer exits on its own.
Only if Kafka is no longer needed:
docker stop kafka-local

Do NOT run docker compose down -v or remove kafka-local.
Keep other lab stacks (Airflow/Spark) stopped on this laptop.

See README.md for real screenshots, detailed results, troubleshooting and theory.


заупск в разных окнах увидеть результаты смещения и отрбаотки кафка и Спарк
docker exec -it structured-streaming-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/streaming_reader.py
docker exec -it structured-streaming-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/streaming_reader.py
проверка видит ли Spark контейнер Kafka
docker network connect runningapachekafkalocally_default structured-streaming-spark
docker exec structured-streaming-spark getent hosts kafka-local