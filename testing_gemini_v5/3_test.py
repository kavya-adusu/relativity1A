import google.generativeai as genai
import json
import csv
import random
from datetime import datetime
import time
from collections import defaultdict


# Configure Gemini API
genai.configure(api_key='AIzaSyBycfSa4F_1Mvw1I3nF2s3JYnYAS5Ynhtg')
model = genai.GenerativeModel('gemini-pro')

def test_candidate_responses(travel_answer, project_answer, relocation_answer):
    prompt = (
        'You will be evaluating a candidate in the hiring process for a Sales Engineering Role. For context, there will be a question and then an answer from a candidate. '
        'Task: Rate them 1-4 based on the following scale for their answer: '
        'Score 1 - Strong "No" (Poor Fit) '
        'Interpretation: The model and evaluators are very confident that this candidate does not meet the necessary criteria for the role. There are significant mismatches in skills, experience, or alignment with core job requirements.'
        'Action: This candidate would not move forward in the process.'
        'Score 2 - "Low Potential" (Requires Additional Review) '
        'Interpretation: There is some alignment with the job role, but not enough to confidently move the candidate forward. There may be notable gaps in essential skills or experience, or concerns that require a second opinion.'
        'Action:  This candidate might be considered if additional criteria are met, but the application requires further scrutiny by another reviewer.'
        'Score 3 - "Moderate Fit" (Potential with Additional Support) '
        'Interpretation: The model and evaluators believe this candidate has a strong potential fit but may need further review to confirm alignment. The candidate demonstrates skills and experience relevant to the role but may require additional insights from a hiring manager or technical lead.'
        'Action: This candidate could proceed, but ideally after a hiring manager’s approval.'
        'Score 4 - Strong "Yes" (Excellent Fit) '
        'Interpretation: High confidence in the candidate’s suitability for the role. The candidate clearly aligns with the role’s requirements and stands out as a strong match. There is a very low likelihood of any red flags or concerns.'
        'Action: This candidate should move to the next round without hesitation, as they are considered an ideal fit.'
        f'Question 1: "This job requires 25% travel; will you be able to do this?" '
        f'Response: {travel_answer} '
        f'Question 2: "We are a fast-paced environment where priorities can shift quickly. Could you tell me about a time when you had to deliver a high-stakes project under pressure?" '
        f'Response: {project_answer} '
        f'Question 3: "Would you consider accepting this role at a different location?" '
        f'Response: {relocation_answer} '
        'Provide your response in this exact JSON format: {"score": <single score 1-4>, "reasoning": "<brief explanation>"}.'
    )
    try:
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0))
        if response and response.text.strip():
            return json.loads(response.text)
        else:
            print("No valid response from the API.")
            return None
    except Exception as e:
        print(f"Error in test_candidate_responses: {e}")
        return None

# Evaluate a single candidate
def evaluate_candidate(test_set):
    try:
        travel_answer = test_set["travel"]["answer"]
        project_answer = test_set["project"]["answer"]
        relocation_answer = test_set["relocation"]["answer"]
        
        result = test_candidate_responses(travel_answer, project_answer, relocation_answer)
        if result:
            return {
                "set": test_set["set"],
                "category": test_set["category"],
                "travel_template": test_set["travel"]["template"],
                "project_template": test_set["project"]["template"],
                "relocation_template": test_set["relocation"]["template"],
                "score": result.get("score"),
                "reasoning": result.get("reasoning"),
            }
        else:
            return None
    except Exception as e:
        print(f"Error processing {test_set['set']}: {e}")
        return None

# Subset test sets to include `n` items per category
def subset_test_sets(test_sets, n=10):
    grouped_by_category = defaultdict(list)
    for test_set in test_sets:
        category = test_set["category"]
        grouped_by_category[category].append(test_set)
    
    sampled_sets = []
    for category, sets in grouped_by_category.items():
        sampled_sets.extend(random.sample(sets, min(n, len(sets))))
    return sampled_sets

# Run tests with rate limiting
def run_tests():
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load test sets
    input_file = "test_sets_cleaned.json"
    with open(input_file, 'r', encoding='utf-8') as f:
        test_sets = json.load(f)
    
    # Subset test sets (10 from each category)
    test_sets_subset = subset_test_sets(test_sets, n=10)
    print(f"Running tests on {len(test_sets_subset)} test sets.")

    request_count = 0
    max_requests_per_minute = 10

    for test_set in test_sets_subset:
        if request_count >= max_requests_per_minute:
            print("Rate limit reached, waiting for 60 seconds...")
            time.sleep(60)
            request_count = 0
        
        result = evaluate_candidate(test_set)
        if result:
            results.append(result)
            request_count += 1

    # Save results to JSON
    output_file = f"aggregated_results_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")
    
    # Convert to CSV
    convert_to_csv(output_file)

# Convert JSON results to CSV
def convert_to_csv(json_file):
    csv_file = json_file.replace(".json", ".csv")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["set", "category", "travel_template", "project_template", "relocation_template", "score", "reasoning"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    
    print(f"CSV file created at {csv_file}")

if __name__ == "__main__":
    run_tests()