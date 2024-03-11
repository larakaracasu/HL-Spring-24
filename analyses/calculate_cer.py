# Imports
import os
import pandas as pd
import pymysql
import editdistance
import re

# Goal: Calculate CERs for the linked GT / OCR pairs

# Function to calculate CER
def calculate_cer(reference, hypothesis):
    # Ensure both inputs are strings
    reference, hypothesis = str(reference), str(hypothesis)
    # Avoid division by zero
    if len(reference) == 0: return 1
    distance = editdistance.eval(reference, hypothesis)
    cer = distance / len(reference)
    return cer

# Function to preprocess ground truth body
def preprocess_gt(gt_text):
    return re.sub(r'[\r\n\t]+', ' ', gt_text)

# Function to preprocess OCR text body
def preprocess_ocr(ocr_text):
    return "".join(ocr_text[2:])

# Initialize file paths
ddo_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/ddo/OCR paper/ddo'
readable_csv_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/ddo/OCR paper/readable.csv'

# Retrieve truth documents from MySQL
query = 'select id, body, sgm_id from docs;'
conn = pymysql.connect(host='history-lab.org', user='de_reader', password='XreadF403', db='declassification_ddrs')
cursor = conn.cursor()
cursor.execute(query)
docs = cursor.fetchall()
cursor.close(),
conn.close()
truth_df = pd.DataFrame(docs,columns=['id','body','sgm_id'])
truth_df['sgm_id'] = pd.to_numeric(truth_df['sgm_id']) # This truth df has id, body, sgm_id, but not record_id (the link)
complete_sgms_df = pd.read_csv('C:/Users/larak/OneDrive/Documents/History-Lab/spring-24/complete_sgms.csv') # We can add record_id
truth_df = pd.merge(truth_df, complete_sgms_df, on='sgm_id') # df containing truth data, sgm_id, and record_id

# Preprocess 'body' so that \n are converted a single space, for uniformity with OCR text
truth_df['body'] = truth_df['body'].apply(preprocess_gt)

# Retrieve OCR documents from local path
ddof = os.listdir(ddo_path)

# To store the OCR data including file name, OCR number, and file body
ocr_data = []

# Loop through each file in the OCR data directory
for filename in ddof:
    ocr = int(filename[-10:-4]) # Extract the OCR number from the filename
    file_path = os.path.join(ddo_path, filename)

    # Add preprocessed OCR text
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    file_contents = "".join(lines[2:])

    # Append the filename, OCR number, and file contents
    ocr_data.append([filename, ocr, file_contents])

# Convert the list into a DataFrame
ocr_df = pd.DataFrame(ocr_data, columns=['ocr_file', 'ocr', 'ocr_body'])

# Merge OCR df with truth df
final_df = pd.merge(truth_df, ocr_df, left_on='record_id', right_on='ocr')

# Clean final_df
final_df.drop(columns=['ocr'], inplace=True) # Drop the 'ocr' column
final_df.rename(columns={'body': 'truth_body'}, inplace=True) # Rename 'body' column to 'truth_body'

# final_df contains the ground truth and OCR bodies. We can calculate CER and add it as a column.
final_df['CER'] = final_df.apply(lambda row: calculate_cer(row['truth_body'], row['ocr_body']), axis=1)

# Merge with existing CSV of matched pairs
readable_df = pd.read_csv(readable_csv_path)
print(readable_df)

merged_df = pd.merge(readable_df, final_df[['ocr_file', 'CER']], left_on='file', right_on='ocr_file')
merged_df.drop('ocr_file', axis=1, inplace=True)
print(merged_df)

merged_df.to_csv('readable_v2.csv')
