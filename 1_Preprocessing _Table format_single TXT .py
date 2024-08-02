#Preprocessing _Table format_single TXT file_81723


# Step 1: Import necessary libraries and modules
import os
import openai
import pandas as pd
import json
import re
import time
from openai.error import ServiceUnavailableError

# Step 2: Set up OpenAI API credentials
openai.api_key = "Your API key"

# Step 3: Read the abstracts from the text file
with open("/Users/doniabenachour/Documents/GPT-literatures_review/Full articles_906'23/bb2121_MM_Tables.txt", "r") as f:
     #abstracts = f.read().split("[Indexed for MEDLINE]")[:-1]  # Split the file by "[Indexed for MEDLINE]" to get individual abstracts
     abstracts = f.read().split("American Society of Clinical Oncology")[:-1] #Split the file by "American Society of Clinical Oncology" to get individual abstracts (ASCO) 


# Step 4: General instruction for the query
general_instruction = '''
Please carefully review the provided table format information. The table format was broken and unorganized during conversions from word file to txt file, and I want to reconstruct and organize the table format information.
Your primary goal is to create a reconstructed and well-organized table format information. 
During this task, must include all data elements and values and DO NOT exclude any information of table format.

'''


# Step 7: Combine all the prompt parts into a single string for 2 dataframes - "Study information & Outcome information"
max_retries = 10
retry_delay = 5

output_folder = "/Users/doniabenachour/Documents/GPT-literatures_review/Full articles_906'23/Preprocess_Tables"

for i, abstract in enumerate(abstracts):
    # Extract the abstract text
    abstract_text = abstract.split("\n", 1)[1].strip()

    # Step 4: General instruction for the query
    prompt = general_instruction + '\n' + f"[Abstract Text]: {abstract_text}" 


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



