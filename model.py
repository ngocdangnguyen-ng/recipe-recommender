import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Charger les données nettoyées
file_path = "Food_Recipe_cleaned.csv"
df_cleaned = pd.read_csv(file_path)

# 1️⃣ Analyse descriptive
print("Statistiques générales des recettes :")
print(df_cleaned.describe())  # Statistiques générales
print("\nRépartition des types de cuisine :")
print(df_cleaned["cuisine"].value_counts())  # Répartition des types de cuisine
print("\nDurée moyenne de préparation :", df_cleaned["prep_time (in mins)"].mean())  # Durée moyenne de préparation
print("\nNombre moyen d'ingrédients par recette :", df_cleaned["ingredients_name"].apply(lambda x: len(str(x).split(','))).mean())  # Nombre moyen d'ingrédients

# 2️⃣ Visualisation des ingrédients les plus utilisés
all_ingredients = df_cleaned["ingredients_name"].dropna().str.split(',').explode()
ingredient_counts = Counter(all_ingredients)
common_ingredients = ingredient_counts.most_common(10)
ingredients, counts = zip(*common_ingredients)

plt.figure(figsize=(10,5))
sns.barplot(x=list(ingredients), y=list(counts))
plt.xticks(rotation=45)
plt.title("Top 10 des ingrédients les plus utilisés")
plt.show()

# 3️⃣ Identification des recettes les plus populaires
if "rating" in df_cleaned.columns:
    print("\nTop 10 des recettes les mieux notées :")
    print(df_cleaned.sort_values(by="rating", ascending=False).head(10))
else:
    print("\nLa colonne 'rating' n'existe pas dans le dataset.")

# 4️⃣ Corrélations entre ingrédients et notes moyennes (si la colonne rating existe)
if "rating" in df_cleaned.columns:
    correlation = df_cleaned.groupby("ingredients_name")["rating"].mean().sort_values(ascending=False)
    print("\nIngrédients associés aux meilleures notes :")
    print(correlation.head(10))

# 5️⃣ Création de graphiques et tableaux récapitulatifs
plt.figure(figsize=(10,5))
sns.histplot(df_cleaned["prep_time (in mins)"], bins=20, kde=True)
plt.title("Distribution des temps de préparation")
plt.xlabel("Temps de préparation (minutes)")
plt.ylabel("Nombre de recettes")
plt.show()

plt.figure(figsize=(8,8))
df_cleaned["cuisine"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Répartition des types de cuisine")
plt.ylabel("")
plt.show()

print("\nAnalyse terminée, les graphiques et résultats sont affichés.")
