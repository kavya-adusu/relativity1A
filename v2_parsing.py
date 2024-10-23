import json

# Function to parse the JSON structure
def parse_gemini_response(data):
    parsed_data = []
    
    # Iterate over each entry in the list
    for entry in data:
        for candidate in entry.get('candidates', []):
            for part in candidate.get('content', {}).get('parts', []):
                text = part.get('text', '')
                
                # Ensure the text is properly formatted
                if '"filled_sentence":' in text and '"recruiter_sentiment":' in text:
                    # Extracting filled_sentence, recruiter_sentiment, and argument_why
                    start_filled_sentence = text.find('"filled_sentence":') + len('"filled_sentence":')
                    end_filled_sentence = text.find('",', start_filled_sentence)
                    filled_sentence = text[start_filled_sentence:end_filled_sentence].strip().strip('"')
                    
                    start_sentiment = text.find('"recruiter_sentiment":') + len('"recruiter_sentiment":')
                    end_sentiment = text.find('",', start_sentiment)
                    recruiter_sentiment = text[start_sentiment:end_sentiment].strip().strip('"')
                    
                    start_argument_why = text.find('"argument_why":') + len('"argument_why":')
                    end_argument_why = text.find('\n}', start_argument_why)
                    argument_why = text[start_argument_why:end_argument_why].strip().strip('"')
                    
                    # Add extracted data to the parsed_data list
                    parsed_data.append({
                        "filled_sentence": filled_sentence,
                        "recruiter_sentiment": recruiter_sentiment,
                        "argument_why": argument_why
                    })
    
    return parsed_data

# Function to load JSON data from a file
def load_json_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return None

# Example: load the JSON file and parse it
filename = "v2_testing.json"  # Replace with the path to your JSON file
data = load_json_from_file(filename)

if data:
    # Call the function to parse the data
    parsed_results = parse_gemini_response(data)

    # Print the parsed results
    for result in parsed_results:
        print(f"Filled Sentence: {result['filled_sentence']}")
        print(f"Recruiter Sentiment: {result['recruiter_sentiment']}")
        print(f"Argument Why: {result['argument_why']}")
        print("\n---\n")
else:
    print("No data to process.")
