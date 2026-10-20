# All Building Structured Data Processing Workflow

Practical exercises for building a structured and reliable data processing workflow.

This project continues the Data Engineering course exercises and focuses on organizing raw shipment data, validating data quality, cleaning invalid records, standardizing values, and preparing trusted output for downstream processing.

## Executor

- Performed by: R. Lisovenko
- Created: 20-10-2026

## Scenario 4: Building a Structured Data Processing Workflow

Imagine you have just joined NorthStar Logistics as a junior data engineer.

Every morning, regional hubs submit shipment records that are used by operations teams to monitor deliveries across the network.

Today's incoming file contains valid records, but it also includes:

- missing destination details
- incomplete delivery statuses
- invalid package weights
- inconsistent hub formatting
- a duplicate shipment

The goal is to build a structured processing workflow that identifies these issues, cleans and standardizes the data, removes duplicates, and produces a reliable dataset for downstream operational reporting.

#  Prepaire  section
1. load raw data
2. validate issues
3. copy raw → clean
4. fix missing values
5. fix invalid numeric values
6. standardize text
7. remove duplicates
8. final validation
## Inspect Raw Shipment Data

- Displays the contents of the source CSV file before processing.
- This helps verify that the raw file exists and review its structure and values.

```powershell
Get-Content data\raw\daily_shipments.csv
```

The file contains:

- valid shipment records
- missing destination values
- missing delivery status
- invalid package weights
- inconsistent hub formatting
- a duplicate shipment ID

## Create Raw Shipments Table

- Creates the `shipments_raw` table for loading the unprocessed shipment data from `daily_shipments.csv`.
- The table keeps the source values before validation and cleaning.

```sql
CREATE TABLE shipments_raw (
    shipment_id VARCHAR(20),
    origin_hub VARCHAR(100),
    destination_hub VARCHAR(100),
    package_weight NUMERIC(10,2),
    delivery_status VARCHAR(50),
    shipment_date DATE
);
```

- Verify the table structure:

```text
\d shipments_raw
```

## Load Raw Shipment Data

- Loads the raw shipment CSV file into the `shipments_raw` table.
- `CSV HEADER` skips the first row containing column names.

```text
\copy shipments_raw FROM 'data/raw/daily_shipments.csv' DELIMITER ',' CSV HEADER;
```

Expected result:

```text
COPY 12
```

- Verifies the number of loaded shipment records.

```sql
SELECT COUNT(*) AS loaded_shipments
FROM shipments_raw;
```

Expected result:

```text
loaded_shipments
----------------
12
```

## Validate Raw Shipment Data

- Performs a summary quality check on the raw shipment dataset.
- Counts missing destinations, missing delivery statuses, and invalid package weights.

```sql
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN destination_hub IS NULL OR destination_hub = '' THEN 1 ELSE 0 END) AS missing_destinations,
    SUM(CASE WHEN delivery_status IS NULL OR delivery_status = '' THEN 1 ELSE 0 END) AS missing_statuses,
    SUM(CASE WHEN package_weight <= 0 THEN 1 ELSE 0 END) AS invalid_weights
FROM shipments_raw;
```

For our file, expected result:

```text
total_records | missing_destinations | missing_statuses | invalid_weights
--------------+----------------------+------------------+----------------
12            | 1                    | 1                | 2
```

## Check Duplicate Shipments

- Identifies duplicated `shipment_id` values in the raw shipment data.
- `GROUP BY shipment_id` groups identical IDs, and `HAVING COUNT(*) > 1` returns only duplicates.

```sql
SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM shipments_raw
GROUP BY shipment_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
shipment_id | duplicate_count
------------+----------------
SH1005      | 2
```

## Create Clean Shipments Table

- Creates a new `shipments_clean` table as a copy of all records from `shipments_raw`.
- This keeps the raw source data unchanged while allowing cleaning and transformation in a separate table.

```sql
CREATE TABLE shipments_clean AS
SELECT *
FROM shipments_raw;
```

Expected result:

```text
SELECT 12
```

- `SELECT 12` means 12 rows were copied into the new `shipments_clean` table.


## Create Clean Shipments Table
- raw = source of truth
- clean = working / processed layer

- Creates a new `shipments_clean` table as a copy of all records from `shipments_raw`.
- This keeps the raw source data unchanged while allowing cleaning and transformation in a separate table.

```sql
CREATE TABLE shipments_clean AS
SELECT *
FROM shipments_raw;
```

Expected result:

```text
SELECT 12
```

- `SELECT 12` means 12 rows were copied into the new `shipments_clean` table.

## Verify Working Table

- Verifies that all raw shipment records were copied into the `shipments_clean` working table.
- `COUNT(*)` confirms the number of rows available for cleaning and transformation.

```sql
SELECT COUNT(*) AS working_rows
FROM shipments_clean;
```

Expected result:

```text
working_rows
------------
12
```

## Fix Missing Destination Hubs

- Replaces missing or empty `destination_hub` values with the standard placeholder `Unknown Hub`.
- This keeps the record while making the missing destination explicit.

```sql
UPDATE shipments_clean
SET destination_hub = 'Unknown Hub'
WHERE destination_hub IS NULL
   OR destination_hub = '';
```

Expected result:

```text
UPDATE 1
```

## Fix Missing Delivery Statuses

- Replaces missing or empty `delivery_status` values with the standard placeholder `Unknown`.
- This keeps the shipment record while making the missing status explicit.

```sql
UPDATE shipments_clean
SET delivery_status = 'Unknown'
WHERE delivery_status IS NULL
   OR delivery_status = '';
```

Expected result:

```text
UPDATE 1
```

## Fix Negative Package Weights

- Converts negative `package_weight` values to positive values using `ABS()`.
- Only rows with a negative weight are updated.

```sql
UPDATE shipments_clean
SET package_weight = ABS(package_weight)
WHERE package_weight < 0;
```

Expected result:

```text
UPDATE 1
```

## Fix Zero Package Weights

- Replaces `package_weight = 0` with a default value of `1`.
- This ensures every shipment has a positive package weight.
```sql
SELECT *
FROM shipments_clean
WHERE package_weight = 0;
```
```sql
UPDATE shipments_clean
SET package_weight = 1
WHERE package_weight = 0;
```

Expected result:

```text
UPDATE 1
```
```sql
SELECT
    shipment_id,
    package_weight
FROM shipments_raw
WHERE shipment_id = 'SH1010';
```
'''sql
SELECT 'raw' AS source, shipment_id, package_weight
FROM shipments_raw
WHERE shipment_id = 'SH1010'

UNION ALL

SELECT 'clean' AS source, shipment_id, package_weight
FROM shipments_clean
WHERE shipment_id = 'SH1010';
'''

- raw = source of truth
- clean = working / processed layer

## Standardize Hub Names

- Removes leading/trailing spaces and converts hub names to title case.

```sql
UPDATE shipments_clean
SET origin_hub = INITCAP(TRIM(origin_hub));
```

Expected result:

```text
UPDATE 12
```

```sql
UPDATE shipments_clean
SET destination_hub = INITCAP(TRIM(destination_hub));
```

Expected result:

```text
UPDATE 12
```

## Remove Duplicate Shipments

- Removes duplicate rows from `shipments_clean` while keeping one record for each `shipment_id`.
- `ctid` is PostgreSQL's internal row identifier.
- `MIN(ctid)` keeps one physical row from each duplicate group.

```sql
DELETE FROM shipments_clean
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM shipments_clean
    GROUP BY shipment_id
);
```

Expected result:

```text
DELETE 1
```

- Verifies that no duplicate shipment IDs remain.

```sql
SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM shipments_clean
GROUP BY shipment_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
0 rows
```

```sql
DELETE FROM shipments_clean
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM shipments_clean
    GROUP BY shipment_id
);
```

```sql
SELECT
    COUNT(*) AS final_records,
    SUM(CASE WHEN destination_hub IS NULL OR destination_hub = '' THEN 1 ELSE 0 END) AS missing_destinations,
    SUM(CASE WHEN delivery_status IS NULL OR delivery_status = '' THEN 1 ELSE 0 END) AS missing_statuses,
    SUM(CASE WHEN package_weight <= 0 THEN 1 ELSE 0 END) AS invalid_weights
FROM shipments_clean;
```

## Verify Duplicate Removal

- Confirms that no duplicate `shipment_id` values remain after cleaning.

```sql
SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM shipments_clean
GROUP BY shipment_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
0 rows
```

- `0 rows` confirms that duplicate shipment records were successfully removed.

## Shipment Count by Delivery Status

- Groups cleaned shipment records by `delivery_status`.
- `COUNT(*)` calculates how many shipments belong to each status.
- `ORDER BY shipment_count DESC` shows the most common status first.

```sql
SELECT
    delivery_status,
    COUNT(*) AS shipment_count
FROM shipments_clean
GROUP BY delivery_status
ORDER BY shipment_count DESC;
```

Expected result:

```text
delivery_status | shipment_count
----------------+---------------
Delivered       | 5
In Transit      | 3
Pending         | 2
Unknown         | 1
```

## Shipment Summary by Destination Hub

- Groups cleaned shipment records by `destination_hub`.
- `COUNT(*)` calculates the number of shipments for each destination.
- `SUM(package_weight)` calculates the total shipment weight for each destination.
- Results are ordered by shipment count from highest to lowest.

```sql
SELECT
    destination_hub,
    COUNT(*) AS shipment_count,
    SUM(package_weight) AS total_weight
FROM shipments_clean
GROUP BY destination_hub
ORDER BY shipment_count DESC, destination_hub;
```

Expected result:

```text
destination_hub | shipment_count | total_weight
----------------+----------------+-------------
Mumbai          | 2              | 18.90
Pune            | 2              | 16.20
Ahmedabad       | 1              | 10.00
Bengaluru       | 1              | 14.70
Chennai         | 1              | 9.80
Delhi           | 1              | 7.50
Hyderabad       | 1              | 11.30
Kolkata         | 1              | 5.00
Unknown Hub     | 1              | 8.00
```

## Overall Shipment Statistics

- Calculates overall statistics for the cleaned shipment dataset.
- `COUNT(*)` returns the total number of shipments.
- `SUM(package_weight)` returns the total package weight.
- `AVG(package_weight)` returns the average package weight.

```sql
SELECT
    COUNT(*) AS total_shipments,
    SUM(package_weight) AS total_package_weight,
    AVG(package_weight) AS average_package_weight
FROM shipments_clean;
```

Expected result:

```text
total_shipments | total_package_weight | average_package_weight
----------------+----------------------+-----------------------
11              | 101.40               | 9.2181818181818182
```

## Export Processed Shipment Data

- Exports the cleaned and validated shipment dataset from PostgreSQL to a processed CSV file.
- Records are ordered by `shipment_id`.
- `CSV HEADER` includes column names in the exported file.

```text
\copy (SELECT * FROM shipments_clean ORDER BY shipment_id) TO 'data/processed/processed_shipments.csv' DELIMITER ',' CSV HEADER;
```

Expected result:

```text
COPY 11
```

- `COPY 11` confirms that 11 cleaned shipment records were exported successfully.

## Verify Exported Processed File

- Displays the exported processed CSV file directly in PowerShell.
- This verifies that the cleaned shipment data was written successfully.

```powershell
Get-Content data\processed\processed_shipments.csv
```

## -------------------------Workflow

```text
Raw Shipment Data
        ↓
Schema and Data Validation
        ↓
Missing Value Checks
        ↓
Invalid Value Checks
        ↓
Data Cleaning
        ↓
Standardization
        ↓
Duplicate Removal
        ↓
Final Quality Validation
        ↓
Trusted Processed Data
```

## Project Structure

```text
05_1_All-Building-Structured-Data-Processing-Workflow/
├─ data/
│  ├─ raw/
│  └─ processed/
├─ docs/
├─ notebooks/
├─ output/
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  └─ sql/
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ Scenario
```

## Source Data

The source shipment file will be stored in:

```text
data/raw/daily_shipments.csv
```

## Main Objectives

- inspect incoming shipment data
- identify missing and invalid values
- standardize inconsistent text values
- correct or handle invalid records
- remove duplicate shipments
- validate the cleaned dataset
- save trusted data for downstream processing

## Course Sections

### Building a Structured Data Processing Workflow

Design and implement a clear sequence of validation, cleaning, transformation, and quality-control steps.

### Practice Project: Building a Reliable Data Processing Pipeline

Apply the workflow to a complete practical data-processing scenario.

### Defending Pipeline Reliability

Explain and justify the validation, error-handling, and reliability decisions used in the pipeline.