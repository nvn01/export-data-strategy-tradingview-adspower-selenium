import pandas as pd
import os
import json
from pathlib import Path

# Get the first Excel file in the data directory
data_dir = Path("data")
excel_files = list(data_dir.glob("*.xlsx"))

if not excel_files:
    print("No Excel files found in the data directory")
    exit(1)

sample_file = excel_files[0]
print(f"Analyzing file: {sample_file}")

# Load the Excel file
xl = pd.ExcelFile(sample_file)

# Print the sheet names
print(f"Sheet names: {xl.sheet_names}")

# For each sheet, print the structure
for sheet_name in xl.sheet_names:
    print(f"\n--- Sheet: {sheet_name} ---")
    df = pd.read_excel(xl, sheet_name)
    
    # Print the first few rows to understand the structure
    print(f"Shape: {df.shape}")
    print("First few rows:")
    print(df.head())
    
    # Print column names
    print("Column names:")
    print(df.columns.tolist())
    
    # For specific sheets, print more rows to better understand the structure
    if sheet_name in ["Trades analysis", "Risk performance ratios"]:
        print("\nMore rows for better understanding:")
        print(df.head(10)) 