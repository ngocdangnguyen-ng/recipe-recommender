import pandas as pd
import os
# Load the raw CSV file from the correct path
raw_data_path = os.path.join("data", "raw", "Food_Recipe.csv")
df = pd.read_csv(raw_data_path)

# Show the first rows of the dataset
print("Data preview:")
print(df.head())

# Show general information about the dataset
print("\nGeneral information about the dataset:")
print(df.info())

# Show the distribution of cuisine types
print("\nCuisine type distribution:")
print(df["cuisine"].value_counts())

# Save the cleaned data to the correct path
cleaned_data_path = os.path.join("data", "cleaned", "Food_Recipe_cleaned.csv")
df.to_csv(cleaned_data_path, index=False)
print(f"\nCleaned data has been saved as '{cleaned_data_path}'.")

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df
