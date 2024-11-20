import os
import pandas as pd

def aggregate_csv_files(input_folder, output_file):
    """
    Aggregates all CSV files in the specified folder into a single CSV file.

    Args:
    - input_folder (str): The path to the folder containing the CSV files to aggregate.
    - output_file (str): The path to the resulting aggregated CSV file.
    """
    # List to store DataFrames from all CSV files
    data_frames = []

    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):  # Check if the file is a CSV
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_path}")
            df = pd.read_csv(file_path)
            data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    aggregated_data = pd.concat(data_frames, ignore_index=True)

    # Save the aggregated DataFrame to a new CSV file
    aggregated_data.to_csv(output_file, index=False)

    print(f"Aggregated CSV file saved at: {output_file}")


# Example usage
input_folder = '/Users/fymor/Documents/BTT AI Studio/Relativity1A_Testing/testing_gemini_v4/results'  # Replace with the path to your folder containing the CSV files
output_file = 'aggregated_results.csv'  # Replace with the desired output file name

aggregate_csv_files(input_folder, output_file)