"""Optional educational lab: partitioning, wide/narrow transforms, shuffles and cache."""
from pyspark.sql.functions import col, count, sum as spark_sum
from common import spark_session

spark=spark_session("NovaForge_Explain_Spark_Execution")
try:
    df=spark.read.json("/opt/project/data/raw/machine_operations.jsonl")
    print("Source partitions:", df.rdd.getNumPartitions())
    narrowed=df.filter(col("run_minutes") > 0).select("machine_id","run_minutes","downtime_minutes")
    print("NARROW TRANSFORMATION: filter + select")
    narrowed.explain(True)
    shuffled=narrowed.groupBy("machine_id").agg(
        count("*").alias("operation_count"),
        spark_sum("run_minutes").alias("runtime_minutes"))
    print("WIDE TRANSFORMATION: groupBy (exchange/shuffle)")
    shuffled.explain(True)
    shuffled.cache()
    shuffled.show(truncate=False)
    shuffled.unpersist()
    print("SPARK EXECUTION PLAN DEMONSTRATION COMPLETED")
finally:
    spark.stop()
