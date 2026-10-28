# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: configure_java.ps1
# Performed by: R. Lisovenko
# Started: 27.10.2026
#
# Description:
# Configure Java JDK 17 for Apache Spark on Windows.
# ------------------------------------------------------------

# Set the Java installation directory.
$env:JAVA_HOME = "C:\dev_soft\Java\jdk-17"

# Add Java binaries to the current PowerShell session PATH.
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

# Verify Java configuration.
Write-Host "JAVA_HOME: $env:JAVA_HOME"
java -version
javac -version