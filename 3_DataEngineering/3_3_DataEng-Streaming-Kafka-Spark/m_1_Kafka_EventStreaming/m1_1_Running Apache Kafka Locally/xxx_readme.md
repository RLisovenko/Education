
# m1 - Running Apache Kafka Locally

**Course:** Streaming Data Pipelines with Kafka and Spark  
**Module:** 1 — Event Streaming with Apache Kafka  
**Lab:** Running Apache Kafka Locally  
**Executor:** R. Lisovenko  
**Date:** November 5, 2026  


## Introduction

This laboratory demonstrates how to deploy and operate **Apache Kafka 3.9.1** locally using Docker Compose and Visual Studio Code.

The main objective is to understand the fundamental components of an event-driven architecture and establish a working communication flow between a Kafka Producer and Consumer.

Kafka acts as a distributed event-streaming platform, allowing producers to publish events to topics while consumers read and process those events independently.

## Architecture and Workflow

The laboratory uses the following components:

- **Docker Desktop:** Runs and manages the Kafka container.
- **Apache Kafka 3.9.1:** Provides the event-streaming platform using KRaft mode.
- **Kafka Broker:** Receives, stores, and serves event records.
- **Topic `orders`:** Stores order-related events.
- **Producer:** Publishes JSON messages representing customer orders.
- **Consumer:** Reads messages from the Kafka topic.

**Event Processing Flow:**

`Kafka Producer → Kafka Broker → Topic (orders) → Kafka Consumer`

## Implementation and Initial Verification

The Kafka environment was configured and launched using Docker Compose.

**Configuration:**

| Component | Value |
|---|---|
| Kafka Version | 3.9.1 |
| Docker Image | `apache/kafka:3.9.1` |
| Container Name | `kafka-local` |
| Bootstrap Server | `localhost:9092` |
| Topic | `orders` |
| Partitions | 1 |
| Replication Factor | 1 |
| Execution Environment | Windows / Docker Desktop / PowerShell |

During setup, an initial Docker Engine connection problem was encountered. After restoring Docker Desktop, Kafka was launched and the topic was created successfully.

The Producer and Consumer were tested using separate VS Code terminals.

**Verified Message:**

```json
{
  "order_id": 101,
  "product": "Laptop",
  "quantity": 2
}
```

The message published by the Producer was successfully received by the Consumer.

**Initial Validation Status: SUCCESS**

This confirms successful local communication between the Kafka Producer, Broker, Topic, and Consumer.

## Learning Outcomes

This exercise provides practical experience with:

- Running Apache Kafka locally using Docker Compose.
- Understanding Kafka brokers, topics, and partitions.
- Creating and inspecting Kafka topics.
- Publishing events using the Kafka Console Producer.
- Consuming events using the Kafka Console Consumer.
- Monitoring Kafka containers and reviewing execution logs.
- Troubleshooting Docker Engine connectivity.

The laboratory establishes the foundation for further exercises involving **Python Kafka clients, consumer groups, event processing, and Spark Structured Streaming**.

---



 ```script
 docker compose config
 docker compose config --services
 docker compose up -d
 docker compose logs kafka --tail 50
 docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --version

 docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

 docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

 docker exec kafka-local /opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
 ```

- Kafka Producer → Topic → Consumer.
 ```
 docker exec -it kafka-local /opt/kafka/bin/kafka-console-consumer.sh --topic orders --bootstrap-server localhost:9092 --from-beginning
 ```

 ```
 {"order_id":101,"product":"Laptop","quantity":2}
 ```

 **R. Lisovenko**  
**Deutschland, November 2026**