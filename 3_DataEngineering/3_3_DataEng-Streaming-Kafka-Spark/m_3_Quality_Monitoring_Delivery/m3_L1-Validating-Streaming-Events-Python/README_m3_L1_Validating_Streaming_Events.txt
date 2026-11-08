m3_L1 — Validating Streaming Events with Python
Executor: Li R.
Status: Prepared; execution output not yet verified

Run these commands from the m3_L1-Validating-Streaming-Events-Python folder.
Use PowerShell; Python command on this PC: py.

=====================================================================
1) EXISTING KAFKA — SETUP TERMINAL
=====================================================================

# Show existing broker status:
docker ps -a --filter "name=kafka-local"

# ONLY if stopped:
docker start kafka-local

# List Kafka topics:
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Create topic ONLY if missing (safe if it already exists):
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic validation-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Verify topic:
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic validation-orders --bootstrap-server localhost:9092

=====================================================================
2) PYTHON DEPENDENCY — SETUP TERMINAL
=====================================================================

py --version
py -m pip show kafka-python

# Only if kafka-python is missing:
py -m pip install -r .\requirements.txt

# OPTIONAL isolated Python 3.12 environment:
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt

# If using this .venv, replace "py" below with:
# .\.venv\Scripts\python.exe

=====================================================================
3) TWO TERMINALS — START VALIDATOR FIRST
=====================================================================

# LEFT terminal (leave running):
py .\validator.py

# RIGHT terminal (start after validator is waiting):
py .\producer.py

# Expected for the five supplied test events only:
# VAL001 VALID
# VAL002 INVALID: customer is required
# VAL003 INVALID: amount must be greater than zero
# VAL004 INVALID: unsupported status: UNKNOWN
# VAL005 VALID
# Summary: Valid=2, Invalid=3

=====================================================================
4) STOP / VERIFY
=====================================================================

# Stop validator using Ctrl+C in LEFT terminal.
# Producer exits automatically.

# IMPORTANT: validator has NO group_id and enable_auto_commit=False;
# auto_offset_reset="earliest" may replay retained records on restart.
# New Producer runs append more messages with new Kafka offsets.

# Keep existing Kafka broker for subsequent labs; optionally stop only
# if no other lab needs it:
# docker stop kafka-local

# Do NOT remove or recreate kafka-local.
# Do NOT run docker compose down -v.

See README.md for the complete procedure, expected results, and cautions.
