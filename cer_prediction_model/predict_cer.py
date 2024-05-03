import spacy
from spellchecker import SpellChecker
import pandas as pd
from collections import Counter
import pickle
from pathlib import Path
import argparse
import textstat
from lexicalrichness import LexicalRichness

nlp = spacy.load("en_core_web_sm")

def calculate_readability_scores(text):
    flesch_score = textstat.flesch_reading_ease(text)
    fk_score = textstat.flesch_kincaid_grade(text)
    return flesch_score, fk_score

def calculate_lexical_diversity(text):
    lex = LexicalRichness(text)
    return lex.ttr  # Type-Token Ratio as a measure of lexical diversity

def calculate_interaction_term(fk_ocr, percent_misspelled):
    misspelled_interaction = fk_ocr * percent_misspelled
    return misspelled_interaction

def calculate_percent_misspelled(text):
    doc = nlp(text)
    spell = SpellChecker()
    words = [token.text for token in doc if token.is_alpha]
    misspelled = spell.unknown(words)
    num_words = len(words)
    num_misspelled = len(misspelled)
    percent_misspelled = (num_misspelled / num_words) * 100 if num_words else 0
    return percent_misspelled

def load_expected_frequencies(csv_filename):
    df = pd.read_csv(csv_filename)
    return dict(zip(df['letter'], df['percent_freq']))

def calculate_percent_alphanumeric(text):
    num_characters = len(text)
    num_alphabetic = sum(c.isalpha() for c in text)
    num_numeric = sum(c.isdigit() for c in text)
    num_punctuation = sum(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in text)
    return {
        'percent_alphabetic': (num_alphabetic / num_characters) * 100 if num_characters else 0,
        'percent_numeric': (num_numeric / num_characters) * 100 if num_characters else 0,
        'percent_punctuation': (num_punctuation / num_characters) * 100 if num_characters else 0
    }

def calculate_character_frequencies(text):
    total_chars = sum(c.isalpha() for c in text)
    char_counts = Counter(c for c in text.lower() if c.isalpha())
    frequencies = {letter: count / total_chars if total_chars else 0 for letter, count in char_counts.items()}
    return frequencies

letter_pairs = [('c', 'e'), ('i', 'l'), ('o', 'a'), ('v', 'u'), ('s', 'z'),
                ('g', 'q'), ('b', 'h'), ('n', 'm'), ('r', 'n'), ('d', 'b')]

def calculate_squared_deviations(observed_frequencies, expected_frequencies):
    return sum((observed_frequencies.get(letter, 0) - expected_frequencies.get(letter, 0)) ** 2 for letter in expected_frequencies)

def calculate_absolute_deviations(observed_frequencies, expected_frequencies):
    return sum(abs(observed_frequencies.get(letter, 0) - expected_frequencies.get(letter, 0)) for letter in expected_frequencies)

def calculate_paired_analysis(observed_frequencies, expected_frequencies, paired_letters):
    squared_paired_analysis = 0
    for letter1, letter2 in paired_letters:
        freq1 = observed_frequencies.get(letter1, 0)
        freq2 = observed_frequencies.get(letter2, 0)
        expected_freq1 = expected_frequencies.get(letter1, 0)
        expected_freq2 = expected_frequencies.get(letter2, 0)
        deviation1 = abs(freq1 - expected_freq1)
        deviation2 = abs(freq2 - expected_freq2)
        squared_paired_analysis += (deviation1 + deviation2) ** 2
    return squared_paired_analysis

def extract_features_from_text(text, expected_frequencies):
    flesch_score, fk_score = calculate_readability_scores(text)
    lexical_diversity = calculate_lexical_diversity(text)
    percent_features = calculate_percent_alphanumeric(text)
    percent_misspelled = calculate_percent_misspelled(text)
    misspelled_interaction = calculate_interaction_term(fk_score, percent_misspelled)
    observed_frequencies = calculate_character_frequencies(text)
    squared_deviations = calculate_squared_deviations(observed_frequencies, expected_frequencies)
    absolute_deviations = calculate_absolute_deviations(observed_frequencies, expected_frequencies)
    substitution_hhi = calculate_paired_analysis(observed_frequencies, expected_frequencies, letter_pairs)
    
    return {
        'lex_ocr': lexical_diversity,
        'fk_ocr': fk_score,
        'flesch_ocr': flesch_score,
        'percent_misspelled': percent_misspelled,
        **percent_features,
        'squared_letter_devs': squared_deviations,
        'absolute_letter_devs': absolute_deviations,
        'substitution_hhi': substitution_hhi,
        'misspelled_interaction': misspelled_interaction,
    }

def predict_cer(text_file, pipeline, expected_frequencies):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
    features = extract_features_from_text(text, expected_frequencies)
    features_df = pd.DataFrame([features])
    return pipeline.predict(features_df)

def load_pipeline(pipeline_path):
    with open(pipeline_path, 'rb') as file:
        return pickle.load(file)

def predict_cer(text, pipeline, expected_frequencies):
    features = extract_features_from_text(text, expected_frequencies)
    features_df = pd.DataFrame([features])
    return pipeline.predict(features_df)[0]

def load_pipeline(pipeline_path):
    with open(pipeline_path, 'rb') as file:
        return pickle.load(file)

def predict_cer(text_file, pipeline, expected_frequencies):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
    features = extract_features_from_text(text, expected_frequencies)
    features_df = pd.DataFrame([features])
    cer_prediction = pipeline.predict(features_df)
    return cer_prediction[0]

def process_input(input_path, pipeline, expected_frequencies):
    path = Path(input_path)
    if path.is_dir():
        results = []
        for file_path in path.glob('*.txt'):
            cer = predict_cer(str(file_path), pipeline, expected_frequencies)
            results.append({'filename': file_path.stem, 'predicted_cer': cer})
        results_df = pd.DataFrame(results)
        results_df.to_csv('predicted_cer_results.csv', index=False)
        print(f"Results saved to predicted_cer_results.csv")
    elif path.is_file():
        cer = predict_cer(input_path, pipeline, expected_frequencies)
        print(f"Predicted CER for {path.stem}: {cer}")
    else:
        print("Invalid file or directory path")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict CER from text files and output to CSV or terminal.")
    parser.add_argument('input_path', type=str, help="The path to a text file or a directory containing text files.")
    args = parser.parse_args()

    pipeline_path = 'model.pkl'
    expected_freq_path = 'expected_letter_distribution.csv'

    expected_frequencies = load_expected_frequencies(expected_freq_path)
    pipeline = load_pipeline(pipeline_path)

    process_input(args.input_path, pipeline, expected_frequencies)
