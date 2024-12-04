import json

# File paths
input_file_path = 'testing_gemini_v5/workflow_2/all_test_sets_with_labels.json'
output_file_path = 'all_test_sets_with_labels_cleaned.json'
# Load the JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Function to clean escaped quotes
def clean_escaped_quotes(obj):
    if isinstance(obj, str):
        # Remove leading and trailing quotes if present
        return obj.strip('"').replace('\\"', '"').replace("\\'", "'")
    elif isinstance(obj, list):
        return [clean_escaped_quotes(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_escaped_quotes(value) for key, value in obj.items()}
    else:
        return obj

# Clean the data
cleaned_data = clean_escaped_quotes(data)

# Write the cleaned JSON to a new file
with open(output_file_path, 'w') as file:
    json.dump(cleaned_data, file, indent=4)

print(f"Cleaned JSON saved to {output_file_path}")

# Verify cleaned data
for entry in cleaned_data[:5]:  # Print first 5 entries for debugging
    print(entry)
#print total of cleaned test sets
print(f"Total test sets: {len(cleaned_data)}")
