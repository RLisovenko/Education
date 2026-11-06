# Optional helper: inspect Kafka without modifying topics.
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    docker compose ps
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose is unavailable.' }
    docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --version
    if ($LASTEXITCODE -ne 0) { throw 'Container kafka-local is not running.' }
    docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
    if ($LASTEXITCODE -ne 0) { throw 'Kafka topic listing failed.' }
    docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
} finally {
    Pop-Location
}
