#Preprocessing _Table format_single TXT file


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
with open("Your txt file", "r") as f:
     abstracts = f.read().split("Your split criteria")[:-1]


# Step 4: General instruction for the query
general_instruction = '''
Please carefully review the provided table format information. The table format was broken and unorganized during conversions from word file to txt file, and I want to reconstruct and organize the table format information.
Your primary goal is to create a reconstructed and well-organized table format information. 
During this task, must include all data elements and values and DO NOT exclude any information of table format.

'''


# Step 5: Combine all the prompt parts into a single string for 2 dataframes - "Study information & Outcome information"
max_retries = 10
retry_delay = 5

output_folder = " "

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



