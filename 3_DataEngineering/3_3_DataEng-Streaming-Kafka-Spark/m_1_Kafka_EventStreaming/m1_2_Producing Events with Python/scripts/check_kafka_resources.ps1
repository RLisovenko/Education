# m1_2 Kafka diagnostics — read-only helper; does not start/stop containers.
# Run this from the lab folder: .\scripts\check_kafka_resources.ps1
$ErrorActionPreference = "Continue"
Write-Host "Docker client / server versions:" -ForegroundColor Cyan
docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
if ($LASTEXITCODE -ne 0) { Write-Warning "Docker Engine is unavailable. Start Docker Desktop."; exit 1 }
Write-Host "Kafka container status:" -ForegroundColor Cyan
docker ps -a --filter "name=kafka-local"
Write-Host "Kafka configured limits:" -ForegroundColor Cyan
docker inspect kafka-local --format 'CPU={{.HostConfig.NanoCpus}} RAM={{.HostConfig.Memory}} SWAP={{.HostConfig.MemorySwap}}'
if ($LASTEXITCODE -ne 0) { Write-Warning "Container kafka-local not found."; exit 2 }
Write-Host "Kafka current resource usage:" -ForegroundColor Cyan
docker stats --no-stream kafka-local
Write-Host "Kafka topics (requires a running broker):" -ForegroundColor Cyan
docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
