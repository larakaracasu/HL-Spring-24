# Estimating CER for OCR documents

This project develops, trains, and evaluates a series of ML models to predict the Character Error Rate (CER) of OCR-ed text documents. The final best model is a Support Vector Regression model that uses various lexical features to make estimations.

## How It Works

1. **Feature Extraction**: The program extracts various features from text files, such as readability scores, lexical diversity, and character frequency deviations.
2. **Model Prediction**: Using a pre-trained model, the program predicts the CER based on the extracted features.
3. **Output**: The results are saved to a CSV file or displayed in the terminal.

## Features

- **Readability Scores**: Flesch Reading Ease and Flesch-Kincaid Grade.
- **Lexical Diversity**: Using the LexicalRichness package.
- **Character Frequencies**: Squared and absolute deviations from expected frequencies.
- **Paired Letter Analysis**: Emphasizes common OCR misrecognitions.
- **Percentages**: Alphabetic, numeric, and punctuation character percentages.
- **Misspelled Words**: Percentage of misspelled words and interaction with lexical diversity.

### Features Used

- `fk_ocr`: Flesch-Kincaid score
- `substitution_hhi`: Substitution Herfindahl-Hirschman Index (paired letter analysis)
- `percent_numeric`: Percentage of numeric characters
- `squared_letter_devs`: Squared deviations from expected letter frequencies
- `misspelled_interaction`: Interaction between lexical complexity and percentage of misspelled words
- `flesch_ocr`: Flesch Reading Ease score
- `absolute_letter_devs`: Absolute deviations from expected letter frequencies
- `percent_punctuation`: Percentage of punctuation characters
- `percent_alphabetic`: Percentage of alphabetic characters
- `percent_misspelled`: Percentage of misspelled words

## Setup Instructions

To set up the environment:
1. Download the `predict_cer` folder from DropBox.
2. Navigate to that folder locally.
3. Create a virtual environment:
   
```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can run the program in two ways:

#### Single File Prediction
To print out the prediction for a single file in the terminal:

```bash
python predict_cer.py <absolute path to OCR text file>
```

The program will print the predicted CER of the file to your terminal.

#### Batch Prediction
To generate a CSV of prediction data for a directory of text files:

```bash
python predict_cer.py <absolute path to the directory containing text files>
```

The program will output a CSV named predicted_cer_results.csv in your working directory.
