"""Shared configuration for the GridPulse smart-meter demonstration."""
from pathlib import Path

TOPIC = "gridpulse-smart-meter-events"
PARTITIONS = 3
BOOTSTRAP_HOST = "localhost:9092"
BOOTSTRAP_DOCKER = "kafka-local:29092"
ALLOWED_STATUSES = ("ONLINE", "OFFLINE", "MAINTENANCE")
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "gridpulse.db"

