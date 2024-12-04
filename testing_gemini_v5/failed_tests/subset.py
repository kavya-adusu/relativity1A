import json
import pandas as pd

# Load the JSON file
input_file = '/mnt/data/test_sets_cleaned.json'
output_file = 'test_sets_10_per_category_corrected.json'

# Load the cleaned JSON into a DataFrame
with open(input_file, 'r') as f:
    data = json.load(f)

# Convert JSON to a DataFrame
df = pd.json_normalize(data)

# Ensure the category column exists
if 'category' not in df.columns:
    raise ValueError("Category column not found in the input JSON")

# Subset the dataset to include only 10 entries per category
subset_df = df.groupby('category').head(10)

# Convert the subset DataFrame back into the desired JSON format
result_json = []
for _, row in subset_df.iterrows():
    result_json.append({
        "set": row["set"],
        "category": row["category"],
        "travel": {
            "answer": row["travel.answer"],
            "template": row["travel.template"]
        },
        "project": {
            "answer": row["project.answer"],
            "template": row["project.template"]
        },
        "relocation": {
            "answer": row["relocation.answer"],
            "template": row["relocation.template"]
        }
    })

# Save the JSON file
with open(output_file, 'w') as f:
    json.dump(result_json, f, indent=4)

print(f"Subsetted JSON file saved to: {output_file}")
