# Databases and SQL for Data Science with Python

- **Completed by:** R. Lisovenko
- **Study period:** January–March 2026

Educational repository containing SQL and Python exercises, hands-on labs, and course work from the IBM **Databases and SQL for Data Science with Python** course.

## Course Information

- **Course:** Databases and SQL for Data Science with Python
- **Platform:**
- **Certificate:** [View IBM / Coursera Certificate](docs/Databases_SQL_DataScience_Python_Certificate_2026-03-09.pdf) · [Verify](https://coursera.org/verify/0AOWRHFFFMZ0) 
- **Completed by:** Ruslan Lisovenko
- **Study period:** January – March 2026
- **Repository:** Practical exercises, labs, SQL scripts, Python code, and Jupyter notebooks completed during the course

The repository focuses on practical database work: writing SQL queries, creating and modifying relational tables, analyzing data, connecting Python to databases, and applying SQL techniques to real-world datasets.

## Course Topics

### Module 1 — Getting Started with SQL
- Relational databases and basic database concepts
- `SELECT`
- `COUNT`
- `DISTINCT`
- `LIMIT`
- `INSERT`
- `UPDATE`
- `DELETE`
- Filtering results with `WHERE`

### Module 2 — Relational Databases and Tables
- Relational database concepts
- DDL vs. DML
- Creating tables
- `CREATE TABLE`
- `ALTER`
- `DROP`
- `TRUNCATE`
- Loading data with SQL scripts
- Relational model constraints

### Module 3 — Intermediate SQL
- String patterns and ranges
- `LIKE`
- Sorting with `ORDER BY`
- Grouping with `GROUP BY`
- Built-in database functions
- Date and time functions
- Aggregate functions
- Subqueries and nested `SELECT`
- Querying multiple tables

### Module 4 — Accessing Databases with Python
- Connecting Python applications to databases
- Python DB-API
- SQL Magic in Jupyter notebooks
- SQLite
- Creating tables from Python
- Loading and querying data
- Analyzing SQL results with Python

### Module 5 — Real-World Data Analysis
- Working with real-world datasets
- Exploring table and column metadata
- Writing analytical SQL queries
- Combining SQL and Python for data analysis
- Final database querying assignment

### Module 6 — Advanced SQL for Data Engineering
- Views
- Stored procedures
- ACID transactions
- `COMMIT` and `ROLLBACK`
- `INNER JOIN`
- `LEFT / RIGHT / OUTER JOIN`
- Querying related tables

## Technologies

- SQL
- Python
- SQLite
- IBM Db2
- Jupyter Notebook
- Relational Databases

## Skills Practiced

- Database design fundamentals
- Data Definition Language (DDL)
- Data Manipulation Language (DML)
- SQL filtering, sorting, and grouping
- Aggregate and built-in functions
- Subqueries
- Multi-table queries and joins
- Transactions
- Views and stored procedures
- Database access from Python
- SQL-based data analysis

## Repository Purpose

DataScience-SQL-Python/
├── notebooks/    # .ipynb
├── sql/          # .sql
├── csv/          # initial data
├── DB/           # databases
├── docs/         # documents
└── README.md

This repository is part of my practical training in **Data Engineering, Backend Development, and Data Science**.

The exercises demonstrate hands-on experience with relational databases, SQL query development, Python database access, and analysis of structured datasets.

## Laboratory Notebooks and SQL Scripts

The notebooks contain course instructions, practical exercises, and
working notes. They cover SQL fundamentals, database access from Python,
and analysis of real-world datasets.

### SQL Fundamentals — Course Root

| Notebook | Purpose |
|---|---|
| `k3_L1_Select.ipynb` | Retrieve and filter data using SELECT queries. |
| `k3_L2_COUNT_DISTINCT_LIMIT.ipynb` | Count records, retrieve unique values, and limit query results. |
| `k3_L3_ins_upd_del.ipynb` | Practice inserting, updating, and deleting records. |
| `k2_L4_CREAT_ALTER_TRUNCATE_DROP.ipynb` | Practice creating, changing, emptying, and removing tables. The original k2 prefix is retained. |
| `k3_L5_SQL_Scripts.ipynb` | Work with SQL script files containing sequences of database commands. |
| `k3_L6_str_pattern_sort_group.ipynb` | Practice string matching, sorting, and grouping query results. |
| `k3_L7_BuiltInFunct_Date.ipynb` | Explore aggregate, string, numeric, and date functions. |
| `k3_L8_Sub_queries.ipynb` | Practice nested queries and subqueries. |
| `k3_L9_Multi_Tbl.ipynb` | Query data from multiple tables. |

### Python and Data Analysis — Course Root

| Notebook or group | Purpose |
|---|---|
| `k3_m4_L1_Cr_tbl_ins_query.ipynb` and its `_2` variant | Create database tables, insert and query records, and retrieve results into pandas. |
| `k3_m4_L2_SQL_magic.ipynb` | Access databases directly from notebook cells using SQL magic commands. |
| `k3_m4_L3_RealDataSet.ipynb` | Practice analyzing a real-world dataset with SQL and Python. |
| `k3_m5_L1_real world data-set.ipynb` | Explore Chicago public school data using SQL. |
| `k3_m5_L3_final.ipynb` | Complete a SQLite querying assignment using Chicago socioeconomic, school, and crime datasets. |
| `k3_m6_Views_SP.ipynb` | Contains laboratory material on working with SQL views in MySQL. |

### Laboratory Materials — Lab Folder

| File or group | Purpose |
|---|---|
| `m4_L1_Insert_Update_SQLite.ipynb` | Create and access a SQLite database from Python and retrieve query results into pandas. |
| `m4_L2_SQLmagic_SQlite.ipynb` | Use SQL magic commands with SQLite. |
| `m4_L3Analyzing_SQLite.ipynb` | Load and analyze Chicago socioeconomic data in SQLite. |
| `m4_L4_ibm_db_py.ipynb` | Connect to IBM Db2 from Python using the ibm_db library. |
| `m4_L5_ibm_db_Querying.ipynb` | Create tables, insert records, and query IBM Db2 from Python. |
| `m4_L6_ibm_SQLmagic.ipynb` | Access databases using SQL magic in the IBM Db2 laboratory context. |
| `m4_L7_.ipynb` | Analyze Chicago socioeconomic data using IBM Db2. |
| `m5_L1_RealDataPractice-v5_sqlite_Learner.ipynb` | Load Chicago public school data into SQLite, inspect metadata, and practice analytical queries. |
| `m5_L12._mitSysDbRealDataPractice-v5._option.ipynb` | Explore the corresponding public school dataset workflow using IBM Db2. |
| `mod5_L2_final_project.ipynb` | Final assignment notebook for loading and querying three Chicago datasets in SQLite. |
| `m6_lab1-instructions.md` | Instructions for creating, updating, and dropping MySQL views using an HR database. |

### SQL Script Files

| Script | Purpose |
|---|---|
| `sp_k3_L5_1_drop_tbl.sql` | Drop existing medical practice tables and recreate their structure. Despite its name, it includes both DROP and CREATE statements. |
| `sp_k3_L5_2_alter_tbl.sql` | Empty MEDICAL_DEPARTMENTS and change the DEPT_NAME column definition. |
| `sp_k3_L6_cr_tbl.sql` | Create HR practice tables for employees, job history, jobs, departments, and locations. |
| `sp_k3_L7_PETRESCUE-CREATE.sql` | Recreate the PETRESCUE table and insert sample records for function and date exercises. |
| `sp_k3_L8_Script_Create_Tables.sql` | Create HR tables used in subquery exercises. |
| `SQL_script/HR_Database_Create_Tables_Script.sql` | Drop and recreate the HR practice tables. |

The `sp_` filename prefix is part of the original naming convention.
These files contain SQL statements; the prefix does not mean that they
define stored procedures.

### Supporting Files

- `csv/` — datasets organized by laboratory or module.
- `DB/` and `.db` files in the course root — local databases used during exercises.
- `docs/` — course documentation, reference materials, and a certificate.

The exercises use different database systems, including SQLite, MySQL,
and IBM Db2. SQL syntax and connection requirements depend on the
individual laboratory. Some setup scripts drop tables or clear data
before preparing the exercise.

## Course

**IBM — Databases and SQL for Data Science with Python**  
Cours: https://github.com/RLisovenko/Databases/tree/db/edu-SQL-DataScience-Python

---

*Educational and practice repository.*
