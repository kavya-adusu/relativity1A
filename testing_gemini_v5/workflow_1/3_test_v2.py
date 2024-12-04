import google.generativeai as genai
import json
import csv
import os
import time
from datetime import datetime

# Configure Gemini API
#genai.configure(api_key='AIzaSyBycfSa4F_1Mvw1I3nF2s3JYnYAS5Ynhtg')
genai.configure(api_key='AIzaSyAbnrOck7dRNPm0lgmcuu13SJjDFinMobw')
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
    retries = 3
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0))
            if response and response.text.strip():
                return json.loads(response.text)
            else:
                print("No valid response from the API.")
                return None
        except json.JSONDecodeError:
            print(f"JSONDecodeError: Unable to parse response on attempt {attempt + 1}")
        except genai.errors.ApiQuotaError:
            print("API quota exceeded. Pausing for 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"Error in test_candidate_responses on attempt {attempt + 1}: {e}")
            time.sleep(5)
    print("Max retries reached. Skipping this test case.")
    return None

# Function to evaluate a single candidate
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
    except Exception as e:
        print(f"Error evaluating candidate in set {test_set['set']}: {e}")
    return None

# Save results to CSV
def save_to_csv(results, csv_file):
    write_header = not os.path.exists(csv_file)  # Check if the file already exists
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["set", "category", "travel_template", "project_template", "relocation_template", "score", "reasoning"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for entry in results:
            writer.writerow(entry)

# Run tests in batches
def run_tests_in_batches(input_file, batch_size=15, max_requests_per_minute=10):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            test_sets = json.load(f)
        
        processed_sets = set()
        total_sets = len(test_sets)
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"results_{timestamp}.csv"

        print(f"Total test sets: {total_sets}")

        while len(processed_sets) < total_sets:
            batch = [
                ts for ts in test_sets
                if ts["set"] not in processed_sets
            ][:batch_size]

            print(f"Processing batch of {len(batch)} sets...")

            request_count = 0
            batch_results = []
            for test_set in batch:
                if request_count >= max_requests_per_minute:
                    print("Rate limit reached. Pausing for 60 seconds...")
                    time.sleep(60)
                    request_count = 0
                
                result = evaluate_candidate(test_set)
                if result:
                    batch_results.append(result)
                    processed_sets.add(test_set["set"])
                    request_count += 1

            # Save batch results to CSV
            if batch_results:
                save_to_csv(batch_results, csv_file)
                print(f"Saved batch results to {csv_file}.")
                results.extend(batch_results)

            print(f"Processed {len(processed_sets)}/{total_sets} sets.")
        
        print(f"All results saved to {csv_file}")

    except Exception as e:
        print(f"Error in run_tests_in_batches: {e}")

if __name__ == "__main__":
    input_file = "all_test_sets_cleaned.json"
    run_tests_in_batches(input_file)