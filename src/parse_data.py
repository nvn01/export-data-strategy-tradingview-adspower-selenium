#!/usr/bin/env python
"""
Parse TradingView strategy report Excel files and convert them to JSON format.

This script reads Excel files from the data directory, extracts information from
multiple sheets (Performance, Trades analysis, Risk performance ratios, List of trades, 
and Properties), and saves the data as JSON files in the same directory.
"""

import pandas as pd
import os
import json
import glob
from pathlib import Path


def clean_column_name(col_name):
    """Clean column names to make them more JSON-friendly."""
    if pd.isna(col_name):
        return "unnamed"
    return str(col_name).strip().lower().replace(" ", "_").replace("/", "_").replace("%", "percent")


def parse_performance_sheet(df):
    """Parse the Performance sheet and return a structured dictionary."""
    # The Performance sheet has a specific structure with metrics in the first column
    result = {}
    
    # Process each row
    for _, row in df.iterrows():
        metric_name = row.iloc[0]
        if pd.isna(metric_name):
            continue
            
        metric_name = clean_column_name(metric_name)
        values = {}
        
        # Extract values for All, Long, and Short
        if not pd.isna(row.get('All USDT', pd.NA)):
            values['all_usdt'] = row.get('All USDT', None)
        if not pd.isna(row.get('All %', pd.NA)):
            values['all_percent'] = row.get('All %', None)
        if not pd.isna(row.get('Long USDT', pd.NA)):
            values['long_usdt'] = row.get('Long USDT', None)
        if not pd.isna(row.get('Long %', pd.NA)):
            values['long_percent'] = row.get('Long %', None)
        if not pd.isna(row.get('Short USDT', pd.NA)):
            values['short_usdt'] = row.get('Short USDT', None)
        if not pd.isna(row.get('Short %', pd.NA)):
            values['short_percent'] = row.get('Short %', None)
            
        result[metric_name] = values
        
    return result


def parse_trades_analysis_sheet(df):
    """Parse the Trades analysis sheet and return a structured dictionary."""
    # Similar approach to performance sheet
    result = {}
    
    for _, row in df.iterrows():
        metric_name = row.iloc[0]
        if pd.isna(metric_name):
            continue
            
        metric_name = clean_column_name(metric_name)
        values = {}
        
        # Extract values for All, Long, and Short
        if not pd.isna(row.get('All USDT', pd.NA)):
            values['all_usdt'] = row.get('All USDT', None)
        if not pd.isna(row.get('All %', pd.NA)):
            values['all_percent'] = row.get('All %', None)
        if not pd.isna(row.get('Long USDT', pd.NA)):
            values['long_usdt'] = row.get('Long USDT', None)
        if not pd.isna(row.get('Long %', pd.NA)):
            values['long_percent'] = row.get('Long %', None)
        if not pd.isna(row.get('Short USDT', pd.NA)):
            values['short_usdt'] = row.get('Short USDT', None)
        if not pd.isna(row.get('Short %', pd.NA)):
            values['short_percent'] = row.get('Short %', None)
            
        result[metric_name] = values
        
    return result


def parse_risk_performance_ratios_sheet(df):
    """Parse the Risk performance ratios sheet and return a structured dictionary."""
    # Similar approach to performance sheet
    result = {}
    
    for _, row in df.iterrows():
        metric_name = row.iloc[0]
        if pd.isna(metric_name):
            continue
            
        metric_name = clean_column_name(metric_name)
        values = {}
        
        # Extract values for All, Long, and Short
        if not pd.isna(row.get('All USDT', pd.NA)):
            values['all_usdt'] = row.get('All USDT', None)
        if not pd.isna(row.get('All %', pd.NA)):
            values['all_percent'] = row.get('All %', None)
        if not pd.isna(row.get('Long USDT', pd.NA)):
            values['long_usdt'] = row.get('Long USDT', None)
        if not pd.isna(row.get('Long %', pd.NA)):
            values['long_percent'] = row.get('Long %', None)
        if not pd.isna(row.get('Short USDT', pd.NA)):
            values['short_usdt'] = row.get('Short USDT', None)
        if not pd.isna(row.get('Short %', pd.NA)):
            values['short_percent'] = row.get('Short %', None)
            
        result[metric_name] = values
        
    return result


def parse_list_of_trades_sheet(df):
    """Parse the List of trades sheet and return a list of trade dictionaries."""
    # Convert DataFrame to list of dictionaries
    trades = []
    
    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Group by trade number to combine entry and exit
    trade_groups = df.groupby('trade_#')
    
    for trade_num, group in trade_groups:
        trade_data = {
            'trade_number': int(trade_num),
            'entries': [],
            'exits': []
        }
        
        # Process each row in the group
        for _, row in group.iterrows():
            row_dict = row.to_dict()
            
            # Remove NaN values
            row_dict = {k: v for k, v in row_dict.items() if not pd.isna(v)}
            
            # Categorize as entry or exit
            if 'entry' in str(row_dict.get('type', '')).lower():
                trade_data['entries'].append(row_dict)
            elif 'exit' in str(row_dict.get('type', '')).lower():
                trade_data['exits'].append(row_dict)
        
        trades.append(trade_data)
    
    return trades


def parse_properties_sheet(df):
    """Parse the Properties sheet and return a dictionary of properties."""
    properties = {}
    
    for _, row in df.iterrows():
        if pd.isna(row['name']) or pd.isna(row['value']):
            continue
            
        key = clean_column_name(row['name'])
        value = row['value']
        properties[key] = value
    
    return properties


def parse_excel_to_json(excel_file):
    """Parse a TradingView strategy report Excel file and convert it to a JSON structure."""
    print(f"Processing {excel_file}...")
    
    # Load the Excel file
    xl = pd.ExcelFile(excel_file)
    
    # Initialize the result dictionary
    result = {
        'file_name': os.path.basename(excel_file),
        'performance': {},
        'trades_analysis': {},
        'risk_performance_ratios': {},
        'trades': [],
        'properties': {}
    }
    
    # Process each sheet
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name)
        
        if sheet_name == 'Performance':
            result['performance'] = parse_performance_sheet(df)
        elif sheet_name == 'Trades analysis':
            result['trades_analysis'] = parse_trades_analysis_sheet(df)
        elif sheet_name == 'Risk performance ratios':
            result['risk_performance_ratios'] = parse_risk_performance_ratios_sheet(df)
        elif sheet_name == 'List of trades':
            result['trades'] = parse_list_of_trades_sheet(df)
        elif sheet_name == 'Properties':
            result['properties'] = parse_properties_sheet(df)
    
    return result


def save_json(data, output_file):
    """Save data as a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Saved JSON to {output_file}")


def main():
    """Main function to process all Excel files in the data directory."""
    # Get all Excel files in the data directory
    # Handle both running from project root and from src directory
    if Path("data").exists():
        data_dir = Path("data")
    else:
        data_dir = Path("..") / "data"
        
    excel_files = list(data_dir.glob("*.xlsx"))
    
    if not excel_files:
        print("No Excel files found in the data directory")
        return
    
    print(f"Found {len(excel_files)} Excel files to process")
    
    # Process each Excel file
    for excel_file in excel_files:
        try:
            # Parse Excel to JSON
            json_data = parse_excel_to_json(excel_file)
            
            # Create output file path (same name but with .json extension)
            output_file = data_dir / f"{excel_file.stem}.json"
            
            # Save JSON file
            save_json(json_data, output_file)
            
        except Exception as e:
            print(f"Error processing {excel_file}: {e}")
    
    print("Processing complete!")


if __name__ == "__main__":
    main() 