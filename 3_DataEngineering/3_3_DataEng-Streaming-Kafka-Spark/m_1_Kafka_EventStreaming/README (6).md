# Module 1 — Event Streaming with Apache Kafka

**Course:** Streaming Data Pipelines with Kafka and Spark  
**Platform:** Coursera  
**Provider:** Edureka  
**Prepared:** 05 November 2026  
**Location:** Deutschland  
**Executor:** R. Lisovenko  
**Status:** Course materials organized — learning and practical verification pending.

## 1. Module Overview

Explore event-driven architectures and reliable event processing with Apache Kafka: events, producers, consumers, topics, partitions, ordering, consumer groups, offsets, retention, compaction, and replay.

## 2. Learning Objectives

- Explain batch processing versus event-driven streaming and identify suitable use cases.
- Describe Kafka brokers, topics, partitions, producers, consumers, offsets, and consumer groups.
- Explain how event keys affect partition assignment and per-partition ordering.
- Compare at-most-once, at-least-once, and exactly-once processing guarantees and their practical limitations.
- Describe retention, log compaction, replay, and the impact of consumer lag.

## 3. Official Course Materials

| # | Type | Lesson / Assessment | Duration | Status |
|---:|---|---|---:|---|
| 1 | Video | [Specialization Introduction](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/xnOXP/specialization-introduction) | 5 min | Not started |
| 2 | Video | [Course Introduction](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/NbSC8/course-introduction) | 3 min | Not started |
| 3 | Reading | [Course Syllabus: Streaming Data Pipelines with Kafka and Spark](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/VOFiV/course-syllabus-streaming-data-pipelines-with-kafka-and-spark) | 10 min | Not started |
| 4 | Video | [Streaming Data and Event-Driven Architecture](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/YMpsX/streaming-data-and-event-driven-architecture) | 4 min | Not started |
| 5 | Reading | [Event Design, Keys, and Ordering in Streaming Systems](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/bIM8Y/event-design-keys-and-ordering-in-streaming-systems) | 10 min | Not started |
| 6 | Video | [Apache Kafka Core Concepts](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/qVIsC/apache-kafka-core-concepts) | 4 min | Not started |
| 7 | Reading | [Kafka Delivery Semantics and Message Processing Guarantees](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/DjHDo/kafka-delivery-semantics-and-message-processing-guarantees) | 10 min | Not started |
| 8 | Video | [Running Apache Kafka Locally](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/I5vjJ/running-apache-kafka-locally) | 4 min | Not started |
| 9 | Practice | [Knowledge Check: Building Streaming Data Pipelines with Kafka](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/assignment-submission/Zr3rZ/knowledge-check-building-streaming-data-pipelines-with-kafka) | 6 min | Not started |
| 10 | Video | [Producing Events with Python](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/Hpaqn/producing-events-with-python) | 3 min | Not started |
| 11 | Video | [Consuming Events with Python](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/6tAJe/consuming-events-with-python) | 3 min | Not started |
| 12 | Video | [Working with Kafka Partitions and Consumer Groups](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/Fak2l/working-with-kafka-partitions-and-consumer-groups) | 5 min | Not started |
| 13 | Reading | [Kafka Retention, Compaction, and Replay](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/Zfcw9/kafka-retention-compaction-and-replay) | 10 min | Not started |
| 14 | Graded | [Event Streaming with Apache Kafka](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/assignment-submission/joMz3/event-streaming-with-apache-kafka) | — | Not started |

**Note:** Durations and materials reflect the Coursera syllabus supplied on 05 November 2026. Dates and availability are controlled by Coursera.

## 4. Key Concepts — Study Notes

### Streaming vs. batch processing

- **Batch processing:** data is collected and processed in bounded runs.
- **Event streaming:** producers continuously publish events and consumers process them independently.
- Kafka stores event records durably according to configured retention; it is more than a transient message queue.

### Kafka vocabulary

| Concept | Working definition |
|---|---|
| Producer | Publishes event records to a Kafka topic. |
| Broker | Kafka server that stores partition logs and serves clients. |
| Topic | Named stream of records, divided into partitions. |
| Partition | Ordered append-only log; ordering is guaranteed within a partition, not across a whole topic. |
| Event key | Used by the default partitioner to consistently route records with the same key (subject to configuration). |
| Consumer group | Consumers cooperating to process partitions of a topic. |
| Offset | Position of a record within its partition. |
| Retention | Determines how long or how much log data is kept. |
| Log compaction | Retains the latest value per key, subject to Kafka's compaction behavior. |
| Replay | Reading previously retained records by changing/using consumer offsets. |

### Delivery and reliability

- **At-most-once:** records may be lost, but are not intentionally processed again.
- **At-least-once:** records are retried, so duplicate processing is possible.
- **Exactly-once:** requires coordinated producer/processing/sink guarantees; it is not automatic for arbitrary external side effects.
- Plan for idempotent processing, offset management, and observability.


## 5. Practical Exercises and Evidence

Planned (not yet executed): start a minimal local Kafka environment; create a topic; publish synthetic events from Python; consume with separate consumer groups; test partition assignment, offsets, and replay.

**Execution status:** Not yet executed. Do not describe proposed commands, screenshots, or results as verified.

### Evidence Log

| Date | Activity | Result | Evidence |
|---|---|---|---|
| — | Course materials prepared | Completed | This README |
| — | Practical demonstration | Pending | `pic/` (to be added) |
| — | Assessment | Pending | Coursera result (to be added) |

## 6. Terminology to Review

- Record new technical terminology, key diagrams, and short English explanations here as lessons progress.
- Keep PowerShell/Docker commands and actual outputs together with their corresponding troubleshooting steps.
- Save authentic screenshots under `../pic/` and reference them with relative links.

## 7. Module Checklist

- [x] Course material index prepared
- [ ] Watch all module videos
- [ ] Complete all required readings
- [ ] Complete the practice assessment
- [ ] Perform and document any practical work
- [ ] Complete the graded assessment
- [ ] Review and finalize notes

---

**Prepared by R. Lisovenko — Deutschland, 05 November 2026.**
