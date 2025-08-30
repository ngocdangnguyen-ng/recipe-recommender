import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

# Load the cleaned data
file_path = os.path.join("data", "cleaned", "Food_Recipe_cleaned.csv")
df_cleaned = pd.read_csv(file_path)

# Descriptive analysis
print("General recipe statistics:")
print(df_cleaned.describe())  # General statistics
print("\nCuisine type distribution:")
print(df_cleaned["cuisine"].value_counts())  # Cuisine type distribution
print("\nAverage preparation time:", df_cleaned["prep_time (in mins)"].mean())  # Average preparation time
print("\nAverage number of ingredients per recipe:", df_cleaned["ingredients_name"].apply(lambda x: len(str(x).split(','))).mean())  # Average number of ingredients

# Visualization of most used ingredients
all_ingredients = df_cleaned["ingredients_name"].dropna().str.split(',').explode()
ingredient_counts = Counter(all_ingredients)
common_ingredients = ingredient_counts.most_common(10)
ingredients, counts = zip(*common_ingredients)

plt.figure(figsize=(10,5))
sns.barplot(x=list(ingredients), y=list(counts))
plt.xticks(rotation=45)
plt.title("Top 10 Most Used Ingredients")
plt.show()

# Identification of most popular recipes
if "rating" in df_cleaned.columns:
    print("\nTop 10 Highest Rated Recipes:")
    print(df_cleaned.sort_values(by="rating", ascending=False).head(10))
else:
    print("\nThe 'rating' column does not exist in the dataset.")

# Correlations between ingredients and average ratings (if rating column exists)
if "rating" in df_cleaned.columns:
    correlation = df_cleaned.groupby("ingredients_name")["rating"].mean().sort_values(ascending=False)
    print("\nIngredients associated with the highest ratings:")
    print(correlation.head(10))

# Create summary charts and tables
plt.figure(figsize=(10,5))
sns.histplot(df_cleaned["prep_time (in mins)"], bins=20, kde=True)
plt.title("Distribution of Preparation Times")
plt.xlabel("Preparation Time (minutes)")
plt.ylabel("Number of Recipes")
plt.show()

plt.figure(figsize=(8,8))
df_cleaned["cuisine"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Cuisine Type Distribution")
plt.ylabel("")
plt.show()

import streamlit as st

def explore_data(df):
    st.write("General statistics:")
    st.write(df.describe())
    st.write("Cuisine type distribution:")
    st.write(df["cuisine"].value_counts())

print("\nAnalysis complete. Charts and results are displayed.")