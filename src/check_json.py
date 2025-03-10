#!/usr/bin/env python
"""
Check the JSON file to make sure it was generated correctly.
"""

import json
import os
from pathlib import Path

# Handle both running from project root and from src directory
if Path("data").exists():
    data_dir = Path("data")
else:
    data_dir = Path("..") / "data"

# Get the first JSON file in the data directory
json_files = list(data_dir.glob("*.json"))

if not json_files:
    print("No JSON files found in the data directory")
    exit(1)

json_file = json_files[0]
print(f"Checking file: {json_file}")

# Load the JSON file
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print the top-level keys
print("\nTop-level keys:")
for key in data.keys():
    print(f"- {key}")

# Print some sample data from each section
print("\nSample performance data:")
for key, value in list(data['performance'].items())[:3]:
    print(f"- {key}: {value}")

print("\nSample trades analysis data:")
for key, value in list(data['trades_analysis'].items())[:3]:
    print(f"- {key}: {value}")

print("\nSample risk performance ratios data:")
for key, value in list(data['risk_performance_ratios'].items())[:3]:
    print(f"- {key}: {value}")

print("\nSample trades data (first trade):")
if data['trades']:
    print(data['trades'][0])

print("\nSample properties data:")
for key, value in list(data['properties'].items())[:5]:
    print(f"- {key}: {value}")

print("\nJSON file looks good!") 