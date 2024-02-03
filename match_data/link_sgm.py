import os
import re
import csv

source_directory = 'C:/Users/larak/OneDrive/Documents/History-Lab/full_truth_folder'
csv_file_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/spring-24/complete_sgms.csv'

# Extract SGM id and record id from SGM
def extract_fields(sgm_content):
    record_id_match = re.search(r'<!--Record id (\d+)-->', sgm_content)
    page_start_match = re.search(r'<!--Page start (\d+)-->', sgm_content)
    
    record_id = record_id_match.group(1) if record_id_match else None
    sgm_id = page_start_match.group(1)[:6] if page_start_match else None
    
    return sgm_id, record_id

# Write to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['sgm_id', 'record_id'])  # Writing header row
    
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.sgm') or file.endswith('.SGM'):
                print(file)
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='latin-1') as f:
                    sgm = f.read()
                    sgm_id, record_id = extract_fields(sgm)
                    if sgm_id and record_id:
                        csv_writer.writerow([sgm_id, record_id]) 

print(f'Data extracted and saved to {csv_file_path}')
