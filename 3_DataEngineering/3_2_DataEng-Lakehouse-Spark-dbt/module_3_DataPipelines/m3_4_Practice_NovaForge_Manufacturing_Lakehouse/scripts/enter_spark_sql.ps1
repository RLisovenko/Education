# Interactive Spark SQL session. Execute from PowerShell.
docker exec -it novaforge-spark /opt/spark/bin/spark-sql --master "local[2]" --conf spark.jars.ivy=/tmp/.ivy2 --packages "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.postgresql:postgresql:42.7.5"
