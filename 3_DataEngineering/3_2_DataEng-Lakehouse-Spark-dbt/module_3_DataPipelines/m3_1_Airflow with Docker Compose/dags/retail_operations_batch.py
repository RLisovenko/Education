
from airflow.sdk import dag, task
from datetime import datetime
import csv
import os


INPUT_FILE = "/opt/airflow/data/operations_raw.csv"
OUTPUT_FILE = "/opt/airflow/output/operations_processed.csv"


@dag(
    dag_id="retail_operations_batch",
    schedule=None,
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["batch", "operations"],
)
def retail_operations_batch():

    # --------------------------------------------------
    # 1. EXTRACT
    # --------------------------------------------------
    @task
    def extract():
        records = []

        with open(INPUT_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

        print(f"Extracted {len(records)} records")
        return records

    # --------------------------------------------------
    # 2. VALIDATE
    # --------------------------------------------------
    @task
    def validate(records):
        if not records:
            raise ValueError("No records found")

        required_fields = [
            "record_id",
            "source_system",
            "category",
            "quantity",
            "amount",
            "status",
        ]

        for record in records:
            for field in required_fields:
                if field not in record or not str(record[field]).strip():
                    raise ValueError(
                        f"Missing or empty field: {field}"
                    )

            try:
                quantity = int(record["quantity"])
                amount = float(record["amount"])
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid numeric data: {record}"
                ) from exc

            if quantity <= 0 or amount < 0:
                raise ValueError(
                    f"Invalid quantity or amount: {record}"
                )

        print(f"Validated {len(records)} records")
        return records

    # --------------------------------------------------
    # 3. TRANSFORM
    # --------------------------------------------------
    @task
    def transform(records):
        transformed_records = []

        for record in records:
            transformed_record = {
                "record_id": int(record["record_id"]),
                "source_system": record["source_system"].strip().upper(),
                "category": record["category"].strip(),
                "quantity": int(record["quantity"]),
                "amount": f'{float(record["amount"]):.2f}',
                "status": record["status"].strip().upper(),
            }

            transformed_records.append(transformed_record)

        print(
            f"Transformed {len(transformed_records)} records"
        )

        return transformed_records

    # --------------------------------------------------
    # 4. LOAD
    # --------------------------------------------------
    @task
    def load(records):
        if not records:
            raise ValueError("No records to load")

        os.makedirs(
            os.path.dirname(OUTPUT_FILE),
            exist_ok=True
        )

        with open(OUTPUT_FILE, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=records[0].keys()
            )

            writer.writeheader()
            writer.writerows(records)

        print(f"Loaded {len(records)} records to {OUTPUT_FILE}")
        return len(records)

    # --------------------------------------------------
    # 5. QUALITY CHECK
    # --------------------------------------------------
    @task
    def quality_check(loaded_count):
        if loaded_count <= 0:
            raise ValueError("No records were loaded")

        if not os.path.exists(OUTPUT_FILE):
            raise FileNotFoundError("Output file was not created")

        print(f"Quality check passed for {loaded_count} records")

    # --------------------------------------------------
    # TASK DEPENDENCIES
    # --------------------------------------------------
    extracted = extract()
    validated = validate(extracted)
    transformed = transform(validated)
    loaded = load(transformed)
    quality_check(loaded)


retail_operations_batch()
