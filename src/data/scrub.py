import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the raw CSV file
file_path = os.path.join("data", "raw", "Food_Recipe.csv")
df = pd.read_csv(file_path)

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Remove rows with missing values
df_cleaned = df.dropna()

# Check and remove duplicates
duplicates = df_cleaned.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")
df_cleaned = df_cleaned.drop_duplicates()

# Check for outliers in 'prep time'
plt.figure(figsize=(8, 5))
sns.boxplot(x=df_cleaned["prep_time (in mins)"])
plt.title("Boxplot of Preparation Time")
plt.savefig("prep_time_boxplot.png")

# Remove outliers in 'prep time' using IQR method
Q1 = df_cleaned["prep_time (in mins)"].quantile(0.25)
Q3 = df_cleaned["prep_time (in mins)"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_cleaned = df_cleaned[(df_cleaned["prep_time (in mins)"] >= lower_bound) & (df_cleaned["prep_time (in mins)"] <= upper_bound)]

# Save the cleaned dataset
cleaned_path = os.path.join("data", "cleaned", "Food_Recipe_cleaned.csv")
df_cleaned.to_csv(cleaned_path, index=False)
print(f"\nCleaned data has been saved as '{cleaned_path}'.")

def clean_data(df):
    df_cleaned = df.dropna().drop_duplicates()
    return df_cleaned
