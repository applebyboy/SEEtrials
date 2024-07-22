#4txt_files_To_oneTxTfile (Table_included)_Final Try 90423

# Step 1: Import necessary libraries and modules
import os
import openai
import time
from openai.error import ServiceUnavailableError

# Step 2: Set up OpenAI API credentials
openai.api_key = "Your API key"

# Step 3: Define the folder paths for the input text files and the output folder
folder1_path = "/Users/doniabenachour/Documents/GPT-literatures_review/Best_CT_Outcomes_81723/ASCO_165set/1/4"
folder2_path = "/Users/doniabenachour/Documents/GPT-literatures_review/Best_CT_Outcomes_81723/ASCO_165set/2/4"
folder3_path = "/Users/doniabenachour/Documents/GPT-literatures_review/Best_CT_Outcomes_81723/ASCO_165set/3/4"
folder4_path = "/Users/doniabenachour/Documents/GPT-literatures_review/Best_CT_Outcomes_81723/ASCO_165set/4/4"
output_folder = "/Users/doniabenachour/Documents/GPT-literatures_review/Best_CT_Outcomes_81723/ASCO_165set/C4"

# Step 4: General instruction for the query
general_instruction = '''
- You have extracted information from the same abstract using four different instructions, resulting in the creation of four distinct TXT files.
- Each file contains a mixture of overlapping and non-overlapping columns, accompanied by their corresponding values.
- Your primary objective is to compose a new TXT file that retains shared information across the files and incorporates non-overlapping columns and their respective values from all four files.
- Ensure the inclusion of all numeric values or percentages within cells or parentheses, even in cases of overlapping columns.
- Incorporate non-overlapping "arms" and their associated values, provided that the values for these arms are wholly non-overlapping.
- If values for all arms are entirely overlapping, treat them as identical and refrain from duplicating them.
'''


# Step 5: Query to Combine Outcomes Information
query_outcomes_info1 = '''
- If each TXT file has only one cohort with similar names, Cohort 1, or Arm1 and these individual cohorts have the same cohort size, intervention for each arm, or clinical study information, they should be treated as the same cohort.
- Ensure that shared information across the files is retained and incorporate non-overlapping columns and their respective values from all four files.
'''

# Step 5: Loop through each text file in the folders
for filename in os.listdir(folder1_path):
    if filename.endswith(".txt"):
        # Step 6: Read the content from the text files in each folder
        file_paths = [
            os.path.join(folder_path, filename) for folder_path in [folder1_path, folder2_path, folder3_path, folder4_path]
        ]
        
        file_contents = []
        for file_path in file_paths:
            with open(file_path, "r") as f:
                file_contents.append(f.read())

        # Step 7: Combine the prompts for the API request
        prompt = general_instruction + '\n'
        for i, file_content in enumerate(file_contents):
            prompt += f"[File {i+1} Content]: {file_content}" + '\n'

        max_retries = 100
        retry_delay = 50

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
            except ServiceUnavailableError as e:
                print(f"API request failed. Retrying in {retry_delay} second(s)...")
                print(f"Error: {e}")
                time.sleep(retry_delay)
        else:
            print("API request failed after maximum retries. Exiting...")
            # Handle the failure case or raise an exception

        # Get the response content
        response_content = response.choices[0].message['content']

        # Write the response content to a text file
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_result.txt")
        with open(output_file_path, 'w') as f:
            f.write(response_content)

        print(f"Response saved to: {output_file_path}")
