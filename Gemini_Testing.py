import pandas as pd
import requests
import json
import os
import time

# Use your API key directly here
api_key = "AIzaSyBeodUTs77FjS9kGGLT6Ptr_l7ath351jc"  

# Function to call the API and get sentiment with exponential backoff, from a recruiter's perspective
def get_sentiment_as_recruiter(template, api_key, max_retries=5):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""As a recruiter, evaluate the following candidate statement: '{template}'.
                        Classify the sentiment of the statement from a recruiter's perspective, and explain why it would affect your decision to hire or offer flexibility to this candidate.
                        Please respond in the following JSON format:
                        {{
                            "filled_sentence": "The candidate's statement.",
                            "recruiter_sentiment": "positive | neutral | negative",
                            "argument_why": "Explain why this statement would affect the candidate's hiring chances or flexibility options."
                        }}
                        """
                    }
                ]
            }
        ]
    }

    retries = 0
    backoff_time = 1  # Start with a 1-second wait
    
    while retries < max_retries:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception if status code is not 2xx
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Rate limited. Waiting {backoff_time} seconds before retrying...")
                time.sleep(backoff_time)
                backoff_time *= 2  # Exponential backoff
                retries += 1
            else:
                print(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    print("Max retries exceeded.")
    return None

# Function to read sentence templates from CSV file
def load_templates_from_csv(filename):
    df = pd.read_csv(filename)
    return df['Sentence'].tolist()

# Function to store results in a JSON file
def store_results_in_json(data, filename="v2_testing.json"):
    # Check if file exists, if not, create it
    if os.path.exists(filename):
        with open(filename, 'r+') as file:
            # Load existing data and append new data
            existing_data = json.load(file)
            existing_data.append(data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
    else:
        # If file doesn't exist, create a new one
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

# Load templates from CSV
templates = load_templates_from_csv('sentence_templates.csv')

# Running the sentiment classification for each template once
for template in templates:
    result = get_sentiment_as_recruiter(template, api_key)
    
    if result:
        print("Result received, storing in JSON file.")
        store_results_in_json(result)  # Store the result in a JSON file
    else:
        print("Failed to retrieve result.")

# Print message indicating where the results are stored
print("Results stored in results.json file.")
