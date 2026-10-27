# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: configure_pyspark.ps1
# Performed by: R. Lisovenko
# Started: 27.10.2026
#
# Description:
# Configure Python and network settings for local PySpark.
# ------------------------------------------------------------

# Resolve the project root relative to this script.
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

# Locate the Python executable in the project's virtual environment.
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

# Verify that the Python executable exists.
if (-not (Test-Path $pythonExe)) {
    throw "Python executable not found: $pythonExe"
}

# Configure Python for Spark worker processes.
$env:PYSPARK_PYTHON = $pythonExe

# Use the same Python interpreter for the Spark driver.
$env:PYSPARK_DRIVER_PYTHON = $pythonExe

# Bind Spark to the local loopback interface.
$env:SPARK_LOCAL_IP = "127.0.0.1"

# Verify PySpark configuration.
Write-Host "PYSPARK_PYTHON: $env:PYSPARK_PYTHON"
Write-Host "PYSPARK_DRIVER_PYTHON: $env:PYSPARK_DRIVER_PYTHON"
Write-Host "SPARK_LOCAL_IP: $env:SPARK_LOCAL_IP"