# Imports
import spacy
import pandas as pd
import os
from spellchecker import SpellChecker

nlp = spacy.load('en_core_web_sm')

ddo_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/ddo/OCR paper/ddo'
readable_csv_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/ddo/OCR paper/readable_v2.csv'
save_path = 'C:/Users/larak/OneDrive/Documents/History-Lab/ddo/OCR paper/readable_v3.csv'

def preprocess_ocr(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    ocr_text = "".join(lines[2:])
    return ocr_text

def calculate_percent_misspelled(text):
    doc = nlp(text)
    spell = SpellChecker()
    words = [token.text for token in doc if token.is_alpha]
    misspelled = spell.unknown(words)
    num_words = len(words)
    num_misspelled = len(misspelled)
    percent_misspelled = (num_misspelled / num_words) * 100 if num_words else 0
    return percent_misspelled

def add_feature_to_csv(readable_csv_path, ddo_path):
    df = pd.read_csv(readable_csv_path)
    percent_misspelled_list = []
    
    for filename in df['file']:
        print(filename)
        file_path = os.path.join(ddo_path, filename)
        if os.path.exists(file_path):
            ocr_text = preprocess_ocr(file_path)
            percent_misspelled = calculate_percent_misspelled(ocr_text)
        else:
            print(f"File {filename} not found in {ddo_path}.")
            percent_misspelled = 0
        percent_misspelled_list.append(percent_misspelled)
    
    df["percent_misspelled"] = percent_misspelled_list
    return df

def main():
    updated_df = add_feature_to_csv(readable_csv_path, ddo_path)
    updated_df.to_csv(save_path, index=False)
    print("Updated CSV saved to:", save_path)

if __name__ == "__main__":
    main()
