"""

This script processes flow log files to count tagged port-protocol combinations based on a provided lookup table,
as well as the count of unique port-protocol combinations.

"""

import csv
import sys
from collections import defaultdict
from CONSTANTS import protocol_mapping

def process_flow_logs(flow_log_file, lookup):
    """
        This function reads a given flow log file, extracts destination ports and protocol numbers, 
        maps the protocols to their respective protocol names, and categorizes them based on a provided lookup table. 

        It counts occurrences of each tagged port-protocol pair and records 
        overall frequency of port-protocol combinations. The function handles errors such as missing 
        or malformed log entries and ensures robustness against unexpected failures.

        Returns:
        - A dictionary mapping tags to their occurrence counts.
        - A dictionary mapping (port, protocol) pairs to their occurrence counts.
        - A count of untagged port-protocol occurrences.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    try:
        with open(flow_log_file, mode='r', encoding='ascii') as file:
            for line in file:
                parts = line.split()
                if len(parts) < 14:
                    raise Exception("Invalid row length in log file")  # Raise error for malformed data
                dst_port, protocol = parts[6], parts[7]
                protocol = protocol_mapping.get(int(protocol), "") # Mapped protocol number to protocol keyword
                key = (dst_port, protocol.lower()) # Converted protocol to lower case as matches are case insensitive
                if key in lookup:
                    tag_counts[lookup[key]] += 1
                else:
                    untagged_count += 1
                port_protocol_counts[key] += 1
    except FileNotFoundError:
        print(f"Error: Flow log file {flow_log_file} not found.")
        sys.exit(1)
    except Exception as err:
        print(f"An unexpected error occured: {err}")
        sys.exit(1)
    return tag_counts, port_protocol_counts, untagged_count

def load_lookup_table(lookup_file):
    """
        Loads a lookup table from a CSV file for mapping destination ports and protocols to tags.
        
        This function reads a given lookup file, processes each row, and stores the mappings in a dictionary. 
        Each entry in the dictionary uses a (destination port, protocol) tuple as a key and assigns it a corresponding tag.
        Case insensitivity is ensured by converting the protocol value to lowercase.

        The function handles errors such as missing 
        or malformed lookup file entries and ensures robustness against unexpected failures.

        Returns:
        - A dictionary where keys are (dst_port, protocol) pairs, and values are their corresponding tags.
    """
    lookup = {}
    try:
        with open(lookup_file, mode='r', encoding='ascii') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header for the csv file
            for row in reader:
                if len(row) < 3:
                    raise Exception("Invalid row length in log file")  # Raise error for malformed data
                dstport, protocol, tag = row
                lookup[(dstport, protocol.lower())] = tag  # Converted protocol to lower case as matches are case insensitive
    except FileNotFoundError:
        print(f"Error: Lookup file {lookup_file} not found.")
        sys.exit(1)
    except Exception as err:
        print(f"An unexpected error occured: {err}")
        sys.exit(1)
    return lookup

def write_output(tag_counts, port_protocol_counts, untagged_count, output_file):
    """
        Writes the processed flow log analysis results to an output file.

        This function takes the tag counts, port-protocol combination counts, and the number of untagged 
        entries and writes them to a specified output file in a structured format. 

        The output includes:
        - A section listing tag counts, showing how many times each tag appears.
        - A separate section detailing the count of each (port, protocol) pair.
        - A final entry for the number of untagged occurrences.

        Parameters:
        - tag_counts (dict): Mapping of tags to their respective counts.
        - port_protocol_counts (dict): Mapping of (port, protocol) pairs to their occurrence counts.
        - untagged_count (int): Count of occurrences without a corresponding tag.
        - output_file (str): Path to the output file where results will be saved.
    """
    with open(output_file, mode='w', encoding='ascii') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n\n")
        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    """
        Main function for parsing and processing flow logs.

        This script takes three command-line arguments:
            - A flow log file containing network flow data.
            - A lookup file for mapping certain flow data.
            - An output file where the results will be saved.

        The function loads a lookup table, processes the flow logs to count various tags, 
        port-protocols combinations, then writes the results to the specified output file.

        Usage:
            python logParser.py <flow_log_file> <lookup_file> <output_file>

        Exits with status 1 if the incorrect number of arguments is provided.
    """
    if len(sys.argv) != 4:
        print("Usage: python logParser.py <flow_log_file> <lookup_file> <output_file>")
        sys.exit(1)
    flow_log_file = sys.argv[1]
    lookup_file = sys.argv[2]
    output_file = sys.argv[3]
    lookup = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts, untagged_count = process_flow_logs(flow_log_file, lookup)
    write_output(tag_counts, port_protocol_counts, untagged_count, output_file)
    print(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()