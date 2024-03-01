import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv(r"C:\Users\larak\Downloads\readable_v2.csv")

# Extract required columns
X = df['CER']  # Independent variable

# For lexical complexity
Y_lexical_complexity_ocr = df['fk_ocr']  # Flesch-Kincaid score from OCR data

# For lexical diversity
Y_lexical_diversity_ocr = df['lex_ocr']  # Lexical diversity from OCR data

# Bivariate regression for lexical complexity vs CER
X_lex_complexity = sm.add_constant(X)  # Add a constant term to the independent variable
model_lex_complexity = sm.OLS(Y_lexical_complexity_ocr, X_lex_complexity).fit()

# Bivariate regression for lexical diversity vs CER
model_lex_diversity = sm.OLS(Y_lexical_diversity_ocr, X_lex_complexity).fit()

# Print regression summary
print("Regression Summary for Lexical Complexity (OCR) vs CER:")
print(model_lex_complexity.summary())
print("\nRegression Summary for Lexical Diversity (OCR) vs CER:")
print(model_lex_diversity.summary())

# Plot the regression lines
plt.figure(figsize=(10, 5))

# Plotting Lexical Complexity (OCR) vs CER
plt.subplot(1, 2, 1)
plt.scatter(X, Y_lexical_complexity_ocr, color='blue', label='Data')
plt.plot(X, model_lex_complexity.predict(X_lex_complexity), color='red', label='Regression Line')
plt.xlabel('CER')
plt.ylabel('Flesch-Kincaid Score (OCR)')
plt.title('Lexical Complexity (OCR) vs CER')
plt.legend()

# Plotting Lexical Diversity (OCR) vs CER
plt.subplot(1, 2, 2)
plt.scatter(X, Y_lexical_diversity_ocr, color='green', label='Data')
plt.plot(X, model_lex_diversity.predict(X_lex_complexity), color='orange', label='Regression Line')
plt.xlabel('CER')
plt.ylabel('Lexical Diversity (OCR)')
plt.title('Lexical Diversity (OCR) vs CER')
plt.legend()

plt.tight_layout()
plt.show()
