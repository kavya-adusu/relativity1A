import pandas as pd
import os

def aggregate_csvs(input_files, output_file):
    """
    Aggregates multiple CSV files into one and saves the combined result to a new file.

    Parameters:
    input_files (list of str): List of paths to the CSV files.
    output_file (str): Path to save the aggregated CSV file.
    """
    try:
        # Initialize an empty list to store dataframes
        dataframes = []
        
        # Read and append each CSV to the list
        for file in input_files:
            if os.path.exists(file):
                df = pd.read_csv(file)
                dataframes.append(df)
                print(f"Loaded {file} with {len(df)} rows.")
            else:
                print(f"File not found: {file}")
        
        # Concatenate all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"Aggregated data contains {len(combined_df)} rows from {len(input_files)} files.")

        # Save the combined dataframe to the output file
        combined_df.to_csv(output_file, index=False)
        print(f"Combined CSV saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_files = [
        "testing_gemini_v5/aggregate_results_workflow_1/results_20241204_101002.csv",
        "testing_gemini_v5/aggregate_results_workflow_1/results_20241204_123502.csv",
        "testing_gemini_v5/aggregate_results_workflow_1/trial_workflow_1_results.csv"  # Add as many file paths as you want
    ]
    output_file = "aggregated_output.csv"
    aggregate_csvs(input_files, output_file)
