-- Runs only on first initialization of the postgres-data Docker volume.
CREATE DATABASE airflow;
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS intermediate;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Stable raw table identities prevent re-runs from dropping dbt dependent views.
CREATE TABLE IF NOT EXISTS raw.production_orders (
    order_id TEXT, facility_id TEXT, line_id TEXT, product_id TEXT,
    production_date DATE, production_status TEXT, planned_units INTEGER
);
CREATE TABLE IF NOT EXISTS raw.machine_operations (
    order_id TEXT, operation_id TEXT, machine_id TEXT, operation_at TIMESTAMP,
    run_minutes INTEGER, downtime_minutes INTEGER, energy_consumption_kwh DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS raw.quality_inspections (
    order_id TEXT, inspection_id TEXT, inspected_units INTEGER,
    rejected_units INTEGER, inspection_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS raw.facilities (
    facility_id TEXT, facility_name TEXT, region TEXT
);
CREATE TABLE IF NOT EXISTS raw.production_lines (
    line_id TEXT, facility_id TEXT, line_name TEXT
);
CREATE TABLE IF NOT EXISTS raw.machines (
    machine_id TEXT, line_id TEXT, machine_type TEXT
);
CREATE TABLE IF NOT EXISTS raw.products (
    product_id TEXT, product_name TEXT, product_family TEXT
);
CREATE TABLE IF NOT EXISTS raw.maintenance_records (
    maintenance_id TEXT, machine_id TEXT, maintenance_date DATE,
    downtime_minutes INTEGER, maintenance_type TEXT
);
