#Cohort & Entire group_outcome_extraction_81023




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
with open("/Users/doniabenachour/Documents/GPT-literatures_review/Full articles_906'23/bb2121_MM_NoT.txt", "r") as f:
     #abstracts = f.read().split("[Indexed for MEDLINE]")[:-1]  # Split the file by "[Indexed for MEDLINE]" to get individual abstracts
     #abstracts = f.read().split("American Society of Clinical Oncology")[:-1] #Split the file by "American Society of Clinical Oncology" to get individual abstracts (ASCO) 
     abstracts = f.read().split("American Society of Hematology")[:-1] #Split the file by "American Society of Hematology" to get individual abstracts (ASH) 


# Step 4: General instruction for the query7
general_instruction = '''
Please carefully examine the provided abstracts, which contain data elements, clinical study information, results, clinical findings, outcomes, or adverse events from various clinical trial studies. Also, the provided abstracts include details about the study design, data collection, patient follow-up, and treatment-related information in the context of clinical trials.  These pieces of information include values expressed as digit numbers, percentages, ranges, 95% confidence interval (CI) ranges, grades, Hazard ratios (HR), or p-values. Your task is to extract all the relevant data elements, results, clinical findings, outcomes, or adverse events from each cohort, which may involve different drugs or doses, along with their corresponding values.
Your primary goal is to organize the extracted information into two tables, ensuring a clear and comprehensive representation of the data. To achieve clarity and consistency, please present all responses in a computational and table format, with each piece of information separated into new cells, lines, or rows. This approach will facilitate easy comprehension and allow for efficient analysis of the data.

'''

# Step 5: Query to extract study information
query_study_info = '''
Table 1: Study Details
Organize the following information from each abstract into a table format:
1. Study Description: Provide a brief description or title of the study.
2. Registry Number: Specify the registry number associated with the clinical trial (e.g., NCT numbers). If abstract has multiple Registry Number, please provide me with the response in a computational format, with each response separated by a new line or row.
3. Study Duration: Provide the duration of the study. 
4. Study Location(s): Specify the location(s) where the study was conducted.
5. Trial Phase: Indicate the phase of the clinical trial.
6. Study Design: Specify the study design, such as randomized or non-randomized trials.
7. Masking: Identify if the trial is open-label, single-blind, or double-blind.
8. Patient Segment: Describe the target condition or patient population.
9. Intervention: Explain the intervention used in the study, including the dose if applicable. 
10. Total Participating Patients: Provide the number of patients who participated in the study.
11. Demographic Information: Include details such as age, sex, median age, or relevant medical history. Please provide me with the response in a computational format, with each response separated by a new line or row.
Please format the table with the first column as "Study Description" and the second column as "Value".

'''

# Step 6: Query to extract outcomes information for arms/cohorts (Table 2)
query_outcomes_info1 = '''
Table 2: Clinical Findings
In Table 2, organize all relevant information of data elements, results, clinical findings, outcomes, or adverse events from each abstract in a tabular format. The column headers will be as follows: "Clinical Findings," "Arm1 (or Cohort 1)," "Arm2 (or Cohort 2)," "Arm3 (or Cohort 3)," and so on. The rows under the "Clinical Findings" column will consist of all relevant information of data elements, results, clinical findings, outcomes, or adverse events. Place the corresponding values for each row and column in their respective cells.
1. Registry Number: Specify the registry number associated with the clinical trial (e.g., NCT numbers).
2. Cohort Size: Include the size of each arm or sub-cohort.
3. Intervention for Each Arm: Explain the intervention and dose information assigned to each arm or sub-cohort in the clinical trial study.
4. clinical study information: provide important details about data collection, patient follow-up, and treatment-related information if available (e.g., Time of Data Cut-off, Time of primary analysis, Duration of exposure (DOE), Duration of Follow-up).
5. All relevant information of data elements, results, clinical findings, outcomes, or adverse events.
6. Adverse Events: Please list all adverse events separately in separate cells, lines, or rows. For each adverse event, provide the corresponding grade information, the number of patients affected, percentage of patients affected, ranges, 95% confidence interval (CI) ranges, grades, Hazard ratios (HR), or p-values in separate cells, lines, or rows, even if they belong to the same adverse event. Each adverse event should be listed in a separate cell, line, or row.
Please ensure to populate the table accurately with the extracted data and use appropriate formatting to ensure clarity and readability.Additionally, please ensure clear separation between the value and range of any Adverse Events in the response. Present each Value or Range in a separate cell, line, or row to maintain clarity and facilitate easy comprehension of the data. This approach will allow for a comprehensive representation of the adverse events and their associated details, enabling efficient analysis and evaluation.

'''

# Step 7: Query to extract outcomes information for the entire group (Table 3)
query_outcomes_info2 = '''
Table 3: Clinical Findings of Entire group
Table 3 is optional. DO NOT create Table 3 if the cohort of this study is the entire group. 
Irrespective of the presence of distinct arms or cohorts, If the entire group provides relevant information encompassing data elements, results, clinical findings, outcomes, or adverse events, create a separate table labeled as Table 3. The column headers should be "Clinical Findings" and "Entire Group". Under the "Clinical Findings" column, array all pertinent data regarding data elements, results, clinical findings, outcomes, or adverse events. Corresponding values for Entire Group of row and column should be situated within the respective cells.
1. Intervention for Entire Group: Elaborate on the intervention and dosage particulars designated for Entire Group within the clinical trial study.
2. Entire Group Size: Encompass the quantification of Entire Group of patients.
3. Clinical Study Information: Furnish crucial particulars concerning data compilation, patient follow-up, and treatment-related specifics, where applicable (e.g., Time of Data Cut-off, Time of Primary Analysis, Duration of Exposure [DOE], Duration of Follow-up).
4. Relevant Data Elements, Results, Clinical Findings, Outcomes, or Adverse Events: All pertinent information concerning data elements, outcomes, clinical findings, results, or adverse events.
5. Adverse Events: List all adverse events distinctly in separate cells, lines, or rows. For each adverse event, present corresponding grade data, the count of affected patients, the percentage of affected patients, ranges, 95% Confidence Interval (CI) ranges, grades, Hazard Ratios (HR), or p-values in individual cells, lines, or rows, even if they pertain to the same adverse event. Each adverse event should be segregated within its distinct cell, line, or row.
'''



query_outcomes_info4 = '''
Possible elements of clinical findings and outcomes: These are possible elements of clinical findings and outcome but not limited to them. Exclusively include any elements mentioned in the provided abstract. Any elements not mentioned in the provided abstract must be excluded from Table 2.
If any elements are mentioned in the provided abstract, extract their all-digit number, Percentage, Range (lower bound ~ upper bound), Median, Median 95% Confidential Interval (CR), 95% CI Range (lower bound ~ upper bound), Hazard ratio (HR) Standard Risk (SR) range (lower bound ~ upper bound), P-value, Time of Data Cutoff (Analysis Cutoff Date), baseline, or cycle.
These are possible elements :Time of Data Cut-off, Time of primary analysis, Duration of exposure (DOE), Duration of Follow-up, Prior Line of Therapy (LOT), Prior treatment, Median Treatment, Range of Treatment, Time of Data Cutoff (Analysis Cutoff Date) of Treatment, Overall Survival Rate (OSR) , Overall Survival (OS), Progression free survival (PFS), Overall Response Rate (ORR), Objective Response Rate (ORR), Response, Stringent Complete Response (sCR), Complete Response (CR),  Very Good Partial Response (VGPR), Very Good Partial Response (VGPR) or Better, Partial Response (PR), Partial Response (PR) or Better, Minimal Residual Disease (MRD), Stable Disease (SD), Progressive Disease (PD), Disease Control Rate (DCR), Duration of Response (DOR),health-related quality of life (HRQoL),patient-reported outcome (PRO),or global health status (GHS).

'''

query_outcomes_info5 = '''
Possible elements of adverse events: These are possible elements of adverse events but not limited to them. Exclusively include any elements mentioned in the provided abstract. Any elements not mentioned in the provided abstract must be excluded from Table 2.
 If any elements are mentioned in the provided abstract, provide the corresponding grade information, the number of patients affected, percentage of patients affected, ranges, 95% confidence interval (CI) ranges, grades, Hazard ratios (HR), or p-values in separate cells, lines, or rows, even if they belong to the same adverse event. Each adverse event should be listed in a separate cell, line, or row.

These are possible elements of adverse events: 
1. Hematological adverse events: Anemia, Febrile neutropenia, Neutropenia, Thrombocytopenia.
2. non-Hematological adverse events: Infections, Cough, Pyrexia, Fatigue, Upper respiratory tract infection, Back pain. 
3. Cytokine Release Syndrome
4. Neurologic Toxic Effects
Other possible elements of adverse events: Seizures, Skin reactions, Diarrhea, Dizziness, Hypotension, Hypertension, Nausea, Vomiting, Constipation, Renal toxicity, Edema, Cataract, Pulmonary disorder, Dyspnoea

'''

query_outcomes_info6 = '''
Possible elements of clinical study information: These are possible elements of clinical study information but not limited to them. Exclusively include any elements mentioned in the provided abstract. Any elements not mentioned in the provided abstract must be excluded from Table 2.
If any elements are mentioned in the provided abstract, extract their all-digit number, Percentage, Range (lower bound ~ upper bound), Median, Median 95% Confidential Interval (CR), 95% CI Range (lower bound ~ upper bound), Hazard ratio (HR) Standard Risk (SR) range (lower bound ~ upper bound), P-value, Time of Data Cutoff (Analysis Cutoff Date), baseline, or cycle.

These are possible elements: Time of Data Cut-off, Time of primary analysis, Duration of exposure (DOE), Duration of Follow-up, Prior Line of Therapy (LOT), Prior treatment, Median Treatment, Range of Treatment, Time of Data Cutoff (Analysis Cutoff Date) of Treatment.

'''
query_outcomes_info7 = '''
**IMPORTANT:**
Please present all responses of Table 2 in a tabular format, with each response separated by a new cell, line, or row. Additionally, please ensure to separate all digit numbers, percentages, ranges, 95% confidence interval (CI) ranges, grades, Hazard ratios (HR), or p-values, and put them into separate cells, lines, or rows. Follow these guidelines for several examples:
1) For values like '5 (42%)' in the table, please split it into two cells/lines/rows, one with '5' and another with '42%'.
2) For values like '20% (n=2)' in the table, please split it into two cells/lines/rows, one with '20%' and another with '2'.
3) For values like '7 cycles (1~26)' in the table, please split it into two cells/lines/rows, one with '7 cycles' and another with '1-26'.
By adhering to this format, we can ensure that the data is presented clearly and comprehensively, making it easier to analyze and interpret the information.

'''


# Step 9: Combine all the prompt parts into a single string for 2 dataframes - "Study information & Outcome information"
max_retries = 10
retry_delay = 5

output_folder = "/Users/doniabenachour/Documents/GPT-literatures_review/Full articles_906'23/Output9"

for i, abstract in enumerate(abstracts):
    # Extract the abstract text
    abstract_text = abstract.split("\n", 1)[1].strip()

    # Step 4: General instruction for the query
    prompt = general_instruction + '\n' + f"[Abstract Text]: {abstract_text}" + '\n' + query_study_info + '\n' + query_outcomes_info1+ '\n' + query_outcomes_info2+ '\n'  + query_outcomes_info4 + '\n'+ query_outcomes_info5 + query_outcomes_info6 + '\n'+ query_outcomes_info7 



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
