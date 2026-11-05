# Module 2 — Streaming Processing with PySpark

**Course:** Streaming Data Pipelines with Kafka and Spark  
**Platform:** Coursera  
**Provider:** Edureka  
**Prepared:** 05 November 2026  
**Location:** Deutschland  
**Executor:** R. Lisovenko  
**Status:** Course materials organized — learning and practical verification pending.

## 1. Module Overview

Build streaming transformations using PySpark Structured Streaming: event-time and windowing, stateful processing, late-arriving events, Kafka sources, output modes, checkpoints, and safe sinks.

## 2. Learning Objectives

- Explain Structured Streaming as incremental processing on DataFrames.
- Distinguish processing time from event time and use windowed aggregations.
- Describe stateful versus stateless operations and watermark handling for late data.
- Read Kafka events, parse schemas, filter and enrich streaming records.
- Choose appropriate output modes, checkpoints, and idempotent sink strategies for recovery.

## 3. Official Course Materials

| # | Type | Lesson / Assessment | Duration | Status |
|---:|---|---|---:|---|
| 1 | Video | [Spark Structured Streaming Fundamentals](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/f8ESJ/spark-structured-streaming-fundamentals) | 5 min | Not started |
| 2 | Video | [Event Time, Windows, and Late Data](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/xkudP/event-time-windows-and-late-data) | 4 min | Not started |
| 3 | Reading | [Stateful and Stateless Stream Processing](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/rVeKA/stateful-and-stateless-stream-processing) | 10 min | Not started |
| 4 | Video | [Reading Kafka Events with Structured Streaming](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/HYI9r/reading-kafka-events-with-structured-streaming) | 4 min | Not started |
| 5 | Video | [Filtering and Enriching Streaming Data](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/MXR4C/filtering-and-enriching-streaming-data) | 3 min | Not started |
| 6 | Practice | [Knowledge Check: Streaming Processing with PySpark](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/assignment-submission/l5qWB/knowledge-check-streaming-processing-with-pyspark) | 6 min | Not started |
| 7 | Video | [Creating Windowed Streaming Aggregations](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/HLHhG/creating-windowed-streaming-aggregations) | 3 min | Not started |
| 8 | Video | [Using Checkpoints for Stream Recovery](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/6ifif/using-checkpoints-for-stream-recovery) | 5 min | Not started |
| 9 | Video | [Streaming Outputs, Checkpoints, and Recovery](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/lecture/kNvn8/streaming-outputs-checkpoints-and-recovery) | 4 min | Not started |
| 10 | Reading | [Streaming Sink Design and Idempotent Writes](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/supplement/RBXee/streaming-sink-design-and-idempotent-writes) | 10 min | Not started |
| 11 | Dialogue | [Reflecting on Reliable Streaming Data Pipeline](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/coach/FImTH/reflecting-on-reliable-streaming-data-pipeline) | 10 min | Not started |
| 12 | Graded | [Streaming Processing with PySpark](https://www.coursera.org/learn/streaming-data-pipelines-kafka-spark/assignment-submission/Y68Wy/streaming-processing-with-pyspark) | 15 min | Not started |

**Note:** Durations and materials reflect the Coursera syllabus supplied on 05 November 2026. Dates and availability are controlled by Coursera.

## 4. Key Concepts — Study Notes

### Structured Streaming model

Spark Structured Streaming processes incoming events through DataFrame-based transformations. Many queries run as **micro-batches**; continuous processing is a separate capability with restrictions.

### Time, windows, and state

| Term | Meaning |
|---|---|
| Processing time | Time when Spark processes an event. |
| Event time | Timestamp associated with when the event occurred. |
| Window | Time interval used to aggregate or group events. |
| Watermark | Threshold used to bound late-event handling and retained state for supported operations; behavior depends on query and output mode. |
| Stateless operation | Per-record transformation without stored state (e.g., filtering). |
| Stateful operation | Requires information across records or batches (e.g., windowed aggregation). |

### Recovery essentials

- **Checkpoint location:** persists stream progress and relevant state for recovery; keep it stable and durable for a given query.
- **Output modes:** `append`, `update`, and `complete` have different semantics and sink/query compatibility.
- **Idempotent sink:** prevent duplicate output when a batch is retried, especially when using `foreachBatch`.
- **Kafka offsets:** track consumption progress as part of the streaming execution and recovery design.


## 5. Practical Exercises and Evidence

Planned (not yet executed): connect a Spark Structured Streaming reader to Kafka; parse JSON events; filter invalid records; compute event-time windows and watermarks; write results with a stable checkpoint and verify restart behavior.

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
