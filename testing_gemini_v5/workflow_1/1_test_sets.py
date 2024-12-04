import pandas as pd
import json
import itertools

# Load the CSV file
csv_path = '/Users/fymor/Documents/BTT AI Studio/Relativity1A_Testing/testing_gemini_v5/Relativity1A_Question_Template.csv'
data = pd.read_csv(csv_path)

# Separate data by Question Number
travel_data = data[data['Question Number'] == 1]
project_data = data[data['Question Number'] == 2]
relocation_data = data[data['Question Number'] == 3]

# Generate all combinations
def generate_all_combinations():
    test_sets = []

    # Group data by categories
    categories = data['Group'].unique()
    
    for category in categories:
        travel_entries = travel_data[travel_data['Group'] == category]
        project_entries = project_data[project_data['Group'] == category]
        relocation_entries = relocation_data[relocation_data['Group'] == category]

        # Extract answers and templates
        travel_answers = list(zip(travel_entries['Answer'], travel_entries['template']))
        project_answers = list(zip(project_entries['Answer'], project_entries['template']))
        relocation_answers = list(zip(relocation_entries['Answer'], relocation_entries['template']))

        # Generate Cartesian product of answers for the given category
        combinations = itertools.product(travel_answers, project_answers, relocation_answers)

        # Generate set names and append to the test_sets list
        prefix = {
            'Parental/Childcare': 'c',
            'Other Caregiving': 'oc',
            'Professional Growth': 'pg',
            'Personal Commitments': 'pe',
            'Dummy Response': 'd',
            'Combined Responsibilities': 'cr'
        }.get(category, 'unknown')

        for i, (travel, project, relocation) in enumerate(combinations, start=1):
            set_name = f"{prefix}{i}"
            test_sets.append({
                "set": set_name,
                "category": category,
                "travel": {
                    "answer": travel[0],
                    "template": travel[1]
                },
                "project": {
                    "answer": project[0],
                    "template": project[1]
                },
                "relocation": {
                    "answer": relocation[0],
                    "template": relocation[1]
                }
            })

    return test_sets

# Generate all combinations
all_test_sets = generate_all_combinations()

# Save the test sets to a JSON file
output_file = 'all_possible_test_sets_with_templates.json'
with open(output_file, 'w') as f:
    json.dump(all_test_sets, f, indent=2)

print(f"Generated {len(all_test_sets)} test sets saved to {output_file}")
#print the number of total test sets
print("Total number of test sets: ", len(all_test_sets))