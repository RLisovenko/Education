m1_3 - Consuming Events with Python
Course: Streaming Data Pipelines with Kafka and Spark
Executor: R. Lisovenko | Deutschland, 06.11.2026

STEP 1 - START DOCKER DESKTOP (wait for "Engine running")

STEP 2 - CHECK THE EXISTING KAFKA CONTAINER (PowerShell)
docker version
docker ps -a --filter "name=kafka-local"

STEP 3 - START KAFKA IF STOPPED
docker start kafka-local

STEP 4 - VERIFY LIMITS AND KAFKA STATUS
docker inspect kafka-local --format 'CPU={{.HostConfig.NanoCpus}} RAM={{.HostConfig.Memory}} SWAP={{.HostConfig.MemorySwap}}'
docker stats --no-stream kafka-local
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

STEP 5 - CHECK PYTHON / DEPENDENCY (Lab m1_3 folder)
py --version
py -m pip show kafka-python

IF THE LIBRARY IS MISSING:
py -m pip install -r .\requirements.txt

STEP 6 - TERMINAL A: START THE PYTHON CONSUMER (Lab m1_3 folder)
py .\consumer.py

STEP 7 - TERMINAL B: SEND NEW EVENTS (from Lab m1_3 folder)
py "..\m1_2_Producing Events with Python\producer.py"

STEP 8 - OPTIONAL: CHECK CONSUMER GROUP (third terminal)
docker exec kafka-local /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processing-group

STEP 9 - STOP CONSUMER
Ctrl+C (in Terminal A)

STEP 10 - STOP KAFKA (when finished)
docker stop kafka-local

OPTIONAL - SHUT DOWN WSL AFTER QUITTING DOCKER DESKTOP
wsl --shutdown

NOTES:
- Use "py", not "python", on this Windows PC.
- Keep the Producer in m1_2 and the Consumer in m1_3.
- Keep CPU 2 / RAM 2 GiB / RAM+swap 3 GiB limits; do not launch another Kafka container.
- If needed, reapply: docker update --cpus=2 --memory=2g --memory-swap=3g kafka-local
- If the Consumer raises KeyError: 'customer', it encountered an older event with a different JSON schema; follow the README.md troubleshooting section.
- Do not use docker compose down -v or delete kafka-local; earlier Kafka setup has no guaranteed persistent data volume.
- At strong fan noise, overheating, or instability: stop and check the laptop before continuing.
