# README

## Overview

`logParser.py` is a Python script that parses flow log data, counts occurrences of tagged destination port-protocol combinations based on a provided lookup table, and outputs a summary of both tag counts and unique port-protocol combination counts.

The script requires two input files:
- A **flow log file** containing network flow data.
- A **lookup table (CSV file)** that maps destination ports and protocols to specific tags.

The script outputs a summary file that lists:
1. **Tag counts**: How many times each tag appears in the flow log file.
2. **Port-protocol combination counts**: The frequency of each (destination port, protocol) pair.

## Assumptions -
- **Custom Flow Log Formats Not Supported:** Only **AWS Flow Log Version 2** (default format) is supported.
- **Lookup Table Format:** The lookup table CSV contains only the following three columns in this exact order: (`dstport`, `protocol`, `tag`)
- **First Row as Headers:** The first row of the lookup file contains column names (`dstport`, `protocol`, `tag`).
- **Case Insensitivity:** Matching of protocols is case insensitive. (e.g., `TCP` is treated the same as `tcp`.)
- **Malformed Rows Handling:**
    - Any row in the flow log file or lookup table that does not conform to the expected format the script **raises an error** and stops execution.
- **Destination Port & Protocol Pairs:** The script returns a count of occurrences for each **unique (DestinationPort, Protocol) pair** in the flow logs.

## Requirements

- Python 3.x
- The script uses only built-in modules (`csv`, `sys`, `collections`).

## Input Files

### **1. Flow Log File**
A plain-text file containing AWS flow logs in **Version 2** format.

### **2. Lookup Table (CSV File)**
A CSV file containing **three columns**:
- `dstport` (destination port)
- `protocol`
- `tag`

## How to Run

1. Clone or download the repository.
2. Ensure **Python 3.x** is installed.
3. Prepare the **flow log file** and **lookup table CSV**.
4. Run the script using the following command:
python logParser.py <flow_log_file> <lookup_file> <output_file>

- `<flow_log_file>`: Path to the flow log file.
- `<lookup_file>`: Path to the CSV lookup file.
- `<output_file>`: Path to save the results.

### **Example Usage:**

python logParser.py flow_logs.txt lookup_table.csv output_results.txt

## Tests:

The script has been tested with:
- **Valid Flow Logs & Lookup Table**: The expected tag and port-protocol counts are correctly generated.
- **Malformed Entries**: The script **raises an error** when encountering invalid lines instead of ignoring them.
- **Case Insensitivity**: Protocol names (`tcp`, `UDP`, etc.) are correctly matched in a case-insensitive manner.
