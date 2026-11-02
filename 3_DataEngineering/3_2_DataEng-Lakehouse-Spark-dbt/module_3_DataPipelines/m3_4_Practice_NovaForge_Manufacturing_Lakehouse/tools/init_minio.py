"""Create the training warehouse bucket; retry until MinIO is ready."""
import os
import time
from minio import Minio

client = Minio(
    "minio:9000",
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False,
)
for attempt in range(1, 31):
    try:
        if not client.bucket_exists("warehouse"):
            client.make_bucket("warehouse")
        print("Bucket ready: warehouse")
        break
    except Exception as exc:
        if attempt == 30:
            raise
        print(f"Waiting for MinIO ({attempt}/30): {exc}")
        time.sleep(2)
