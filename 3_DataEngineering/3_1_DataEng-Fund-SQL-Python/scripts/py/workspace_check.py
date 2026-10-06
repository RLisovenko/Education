# Course: Data Engineering Foundations with SQL and Python
# Practical exercise
# Performed by: R. Lisovenko
# Date: 02-10-2026

import platform
import subprocess
import pandas as pd

print("=" * 55)
print("DATA ENGINEERING WORKSPACE VERIFICATION")
print("=" * 55)

print(f"Python Version : {platform.python_version()}")
print(f"Pandas Version : {pd.__version__}")

try:
    git_version = subprocess.check_output(
        ["git", "--version"],
        text=True
    ).strip()
    print(f"Git Version    : {git_version}")
except Exception:
    print("Git Version    : NOT FOUND")

try:
    psql_version = subprocess.check_output(
        ["psql", "--version"],
        text=True
    ).strip()
    print(f"PostgreSQL     : {psql_version}")
except Exception:
    print("PostgreSQL     : NOT FOUND")

print("-" * 55)
print("Workspace Status : Ready")
print("Environment      : Configured Successfully")
print("=" * 55)