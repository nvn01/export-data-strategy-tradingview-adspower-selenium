# TradingView Strategy Report Parser

This directory contains scripts to parse TradingView strategy report Excel files and convert them to JSON format.

## Scripts

- `parse_data.py`: Main script to parse all Excel files in the data directory and convert them to JSON
- `test-parse.py`: Test script to parse a single Excel file
- `check_json.py`: Script to check the generated JSON files
- `analyze_excel.py`: Script to analyze the structure of the Excel files

## Usage

### Parse all Excel files

```bash
# From the project root
poetry run python src/parse_data.py

# Or from the src directory
cd src
poetry run python parse_data.py
```

### Parse a single Excel file

```bash
# From the project root
poetry run python src/test-parse.py

# Or from the src directory
cd src
poetry run python test-parse.py
```

### Check the generated JSON files

```bash
# From the project root
poetry run python src/check_json.py

# Or from the src directory
cd src
poetry run python check_json.py
```

## JSON Structure

The generated JSON files have the following structure:

```json
{
  "file_name": "Original Excel file name",
  "performance": {
    "metric_name": {
      "all_usdt": value,
      "all_percent": value,
      "long_usdt": value,
      "long_percent": value,
      "short_usdt": value,
      "short_percent": value
    },
    ...
  },
  "trades_analysis": {
    "metric_name": {
      "all_usdt": value,
      "all_percent": value,
      ...
    },
    ...
  },
  "risk_performance_ratios": {
    "metric_name": {
      "all_usdt": value,
      "all_percent": value,
      ...
    },
    ...
  },
  "trades": [
    {
      "trade_number": number,
      "entries": [
        {
          "trade_#": number,
          "type": "Entry long/short",
          "signal": "Signal name",
          "date_time": "Date and time",
          "price_usdt": price,
          "contracts": number,
          "profit_usdt": profit,
          "profit_percent": percent,
          ...
        },
        ...
      ],
      "exits": [
        {
          "trade_#": number,
          "type": "Exit long/short",
          "signal": "Signal name",
          ...
        },
        ...
      ]
    },
    ...
  ],
  "properties": {
    "property_name": "value",
    ...
  }
}
```

## Database Integration

The JSON files can be easily imported into a database system. Each top-level key can be mapped to a table:

- `performance`: Performance metrics table
- `trades_analysis`: Trades analysis metrics table
- `risk_performance_ratios`: Risk performance ratios table
- `trades`: Trades table with related entries and exits tables
- `properties`: Properties table

This structure makes it easy to query and analyze the data using SQL or other database tools.
