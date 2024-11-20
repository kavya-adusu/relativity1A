import pandas as pd
import json
import random

# Load the CSV file
csv_path = 'Relativity1A_Question_Template - Sheet1.csv'
data = pd.read_csv(csv_path)

# Filter data by groups for easy selection
childcare_group = data[data['Group'].str.contains('Childcare', na=False)]
caregiving_group = data[data['Group'].str.contains('Caregiving', na=False)]
professional_group = data[data['Group'].str.contains('Professional', na=False)]
personal_group = data[data['Group'].str.contains('Personal', na=False)]
dummy_group = data[data['Group'].str.contains('Dummy', na=False)]

# Function to randomly select an answer for each profile type
def get_random_answer(group):
    if not group.empty:
        return group.sample(1, replace=True).iloc[0]['Answer']
    return "No relevant answer available."

# Create extensive structured test cases
test_sets = []

# Generate more variations for each group
num_variations = 10  # Increase this number to generate more test sets

# Childcare Examples
for i in range(1, num_variations + 1):
    test_sets.append({
        "name": f"childcare_{i}",
        "travel": get_random_answer(childcare_group),
        "project": get_random_answer(childcare_group),
        "relocation": get_random_answer(childcare_group)
    })

# Personal/Professional examples
for i in range(1, num_variations + 1):
    test_sets.append({
        "name": f"professional_{i}",
        "travel": get_random_answer(professional_group),
        "project": get_random_answer(professional_group),
        "relocation": get_random_answer(professional_group)
    })
    test_sets.append({
        "name": f"personal_{i}",
        "travel": get_random_answer(personal_group),
        "project": get_random_answer(personal_group),
        "relocation": get_random_answer(personal_group)
    })

# Mixed examples (Combining Childcare with other groups)
for i in range(1, num_variations + 1):
    test_sets.append({
        "name": f"mixed_{i}",
        "travel": get_random_answer(random.choice([childcare_group, caregiving_group])),
        "project": get_random_answer(professional_group),
        "relocation": get_random_answer(random.choice([childcare_group, personal_group]))
    })

# Dummy control
for i in range(1, num_variations + 1):
    test_sets.append({
        "name": f"dummy_{i}",
        "travel": get_random_answer(dummy_group),
        "project": get_random_answer(dummy_group),
        "relocation": get_random_answer(dummy_group)
    })

# Print the number of test sets generated and save them to JSON
print(f"Generated {len(test_sets)} test sets.")

# Print a sample of test sets for verification
for case in test_sets[:5]:  # Print the first 5 for quick verification
    print(json.dumps(case, indent=2))

# Save test sets to a JSON file
output_file = 'test_sets_profiles_expanded.json'
with open(output_file, 'w') as f:
    json.dump(test_sets, f, indent=2)

print(f"\nTest sets saved to {output_file}")

import json
import re

def clean_json_file(input_file, output_file):
    """
    Cleans up unnecessary escape characters and formats strings properly in a JSON file.
    
    Args:
    - input_file (str): The path to the input JSON file.
    - output_file (str): The path to save the cleaned JSON file.
    """
    # Load the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Recursive function to clean strings within nested structures
    def clean_item(item):
        if isinstance(item, str):
            # Use regex to remove leading and trailing quotes and backslashes
            item = re.sub(r'\\', '', item)
            item = item.replace('\u201c', '"').replace('\u201d', '"')
            return item.strip('"')
        elif isinstance(item, dict):
            return {key: clean_item(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [clean_item(element) for element in item]
        else:
            return item

    # Clean the entire data structure
    cleaned_data = clean_item(data)

    # Save the cleaned data back to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Cleaned JSON data saved to {output_file}")
    return cleaned_data

# Example usage
input_path = 'test_sets_profiles_final.json'
output_path = 'test_sets_profiles_cleaned.json'
cleaned_data = clean_json_file(input_path, output_path)

# Print cleaned JSON for verification
for case in cleaned_data:
    print(json.dumps(case, indent=2, ensure_ascii=False))
