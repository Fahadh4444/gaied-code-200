import requests
import json
import os

file_path = os.path.abspath("./model/topics_to_classify.json")  # Get absolute path
print("Looking for:", file_path)  # Debug print

with open(file_path, "r") as rules_file:
    rules = json.load(rules_file)

url = "http://localhost:11434/api/chat"

def llama3(email_body):
    # 🏷️ Formulate the complete prompt
    prompt = (
        "You are an expert in commercial lending services. Your task is to classify the given content into one or more request types and Sub Request Types provided in the topics_to_classify.json file"
        "The classification must maintain the hierarchy between request types and their associated sub-request types as specified in the topics_to_classify.json. "
        "Sub-request types should never be classified independently without their parent request type."
        " if there is a request type without any sub request type, then display only request type  "
        "For each classification, assign a score based on how well the content matches the key attributes relevant to these request types and sub request types. "
        "Prioritize context and the overall primary intent over isolated keywords. If multiple request types are present, determine the primary one based on "
        "the main action described. Classify and rank the email content by identifying the primary intent first and then secondary intents. "
        "Provide a confidence score for each classification and an explanation for why it was selected. "
        "Ensure that the response is formatted as a structured JSON object and The response should include the following fields: {request_type, sub_request_type, confidence, matched_attributes, extracted_sentences} for all classifications and also extract primary_classification. "        
        "\n\n"
        f"Rules: {json.dumps(rules, indent=2)}\n\n"
        f"Email Body:\n{email_body}"
    )
    data = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    # Print the entire response for debugging
    print("Raw Response:", response.json())

    # Handle response structure and errors
    try:
        # Extracting the nested "content" field from "message"
        return response.json()["message"]["content"]
    except KeyError:
        return "Error: Invalid response structure"