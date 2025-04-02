import pandas as pd

# Charger le fichier CSV
file_path = "Food_Recipe.csv"
df = pd.read_csv(file_path)

# Afficher les premières lignes du jeu de données
print("Aperçu des données :")
print(df.head())

# Afficher les informations générales sur le dataset
print("\nInformations générales sur le dataset :")
print(df.info())

# Afficher la distribution des types de cuisine
print("\nRépartition des types de cuisine :")
print(df["cuisine"].value_counts())

# Enregistrer les données brutes pour référence
df.to_csv("Food_Recipe_raw.csv", index=False)
print("\nLes données brutes ont été enregistrées sous 'Food_Recipe_raw.csv'.")




#Charge le fichier Food_Recipe.csv en DataFrame.
#Affiche aperçu des données (premières lignes, types de colonnes).
#montre la répartition des types de cuisine.
#Enregistre une copie brute du dataset (Food_Recipe_raw.csv) pour référence.
