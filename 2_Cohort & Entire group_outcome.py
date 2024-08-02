# Cohort & Entire group_outcome_extraction

# Step 1: Import necessary libraries and modules
import os
import openai
import pandas as pd
import json
import re
import time
from openai.error import ServiceUnavailableError

# Step 2: Set up OpenAI API credentials
openai.api_key = "Your API Key"

# Step 3: Read the abstracts from the text file
with open("/path/to/your/abstracts.txt", "r") as f:
    abstracts = f.read().split("Your Split Criteria")[:-1]

# Step 4: General instruction for the query
general_instruction = '''
Please carefully examine the provided abstracts and extract all relevant data elements, results, clinical findings, outcomes, or adverse events from each cohort. Organize the extracted information into tables for clarity.
# Specific prompt for this step can be shared upon request
'''

# Step 5: Query to extract study information
query_study_info = '''
Table 1: Study Details
# Specific prompt for this step can be shared upon request
'''

# Step 6: Query to extract outcomes information for arms/cohorts (Table 2)
query_outcomes_info1 = '''
Table 2: Clinical Findings
# Specific prompt for this step can be shared upon request
'''

# Step 7: Query to extract outcomes information for the entire group (Table 3)
query_outcomes_info2 = '''
Table 3: Clinical Findings of Entire Group
# Specific prompt for this step can be shared upon request
'''

# Step 8: Additional queries (placeholders)
query_outcomes_info4 = '''Custom queries for additional extraction (if needed).'''
query_outcomes_info5 = '''Custom queries for adverse events extraction (if needed).'''
query_outcomes_info6 = '''Custom queries for clinical study information extraction (if needed).'''
query_outcomes_info7 = '''Custom queries for formatting and presentation (if needed).'''

# Step 9: Combine all the prompt parts into a single string for 2 dataframes - "Study information & Outcome information"
max_retries = 10
retry_delay = 5

output_folder = "/path/to/output/folder"

for i, abstract in enumerate(abstracts):
    # Extract the abstract text
    abstract_text = abstract.split("\n", 1)[1].strip()

    # Step 4: General instruction for the query
    prompt = general_instruction + '\n' + f"[Abstract Text]: {abstract_text}" + '\n' + query_study_info + '\n' + query_outcomes_info1 + '\n' + query_outcomes_info2 + '\n' + query_outcomes_info4 + '\n' + query_outcomes_info5 + '\n' + query_outcomes_info6 + '\n' + query_outcomes_info7

    for j in range(max_retries):
        try:
            # Send the prompt to the OpenAI Chat API for response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            break  # Request succeeded, exit the loop
        except ServiceUnavailableError:
            print(f"API request failed. Retrying in {retry_delay} second(s)...")
            time.sleep(retry_delay)
    else:
        print("API request failed after maximum retries. Exiting...")
        # Handle the failure case or raise an exception

    # Get the response content
    response_content = response.choices[0].message.content

    # Write the response content to a text file
    output_file_path = os.path.join(output_folder, f"sample_result{i+1}_study.txt")
    with open(output_file_path, 'w') as f:
        f.write(response_content)

    print(f"Response saved to: {output_file_path}")


