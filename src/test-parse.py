#!/usr/bin/env python
"""
Test script to parse a single TradingView strategy report Excel file.
"""

import pandas as pd
import os
import json
import sys
from pathlib import Path
from parse_data import parse_excel_to_json, save_json

def main():
    """Test function to process a single Excel file."""
    # Get the first Excel file in the data directory
    # When running from src directory, data is one level up
    data_dir = Path("..") / "data"
    excel_files = list(data_dir.glob("*.xlsx"))
    
    if not excel_files:
        print("No Excel files found in the data directory")
        return
    
    # Process the first Excel file
    excel_file = excel_files[0]
    print(f"Processing {excel_file}...")
    
    try:
        # Parse Excel to JSON
        json_data = parse_excel_to_json(excel_file)
        
        # Create output file path (same name but with .json extension)
        output_file = data_dir / f"{excel_file.stem}.json"
        
        # Save JSON file
        save_json(json_data, output_file)
        
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error processing {excel_file}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 