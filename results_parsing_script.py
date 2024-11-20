# Description: this script is run after the test script is run to go from
# json -> csv
import json
import csv

def parse_json_to_csv(input_file, output_file):
    """
    Parses the input JSON file and saves the relevant data to a CSV file.
    
    Args:
    - input_file (str): The path to the input JSON file.
    - output_file (str): The path to save the output CSV file.
    """
    # Load the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Open the CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['set_name', 'score', 'reasoning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write each entry to the CSV
        for entry in data:
            writer.writerow({
                'set_name': entry['set_name'],
                'score': entry['score'],
                'reasoning': entry['reasoning']
            })

    print(f"CSV file has been created at {output_file}")

# Example usage
input_file = 'recruiting_bias_results_20241119_210541.json'  # Replace with your JSON file path
output_file = 'recruiting_bias_results_20241119_210541.csv'    # Replace with your desired CSV file path

parse_json_to_csv(input_file, output_file)
