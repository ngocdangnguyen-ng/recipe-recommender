import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le fichier CSV
file_path = "Food_Recipe.csv"
df = pd.read_csv(file_path)

# Vérifier les valeurs manquantes
print("\nValeurs manquantes par colonne :")
print(df.isnull().sum())

# Supprimer les lignes avec des valeurs manquantes 
df_cleaned = df.dropna()

# Vérifier et supprimer les doublons
duplicates = df_cleaned.duplicated().sum()
print(f"\nNombre de lignes en double : {duplicates}")
df_cleaned = df_cleaned.drop_duplicates()

# Vérifier les outliers sur le temps de préparation ('prep time')
plt.figure(figsize=(8, 5))
sns.boxplot(x=df_cleaned["prep_time (in mins)"])
plt.title("Boxplot du temps de préparation")
plt.savefig("prep_time_boxplot.png")

# Suppression des outliers sur 'prep time' (méthode IQR)
Q1 = df_cleaned["prep_time (in mins)"].quantile(0.25)
Q3 = df_cleaned["prep_time (in mins)"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_cleaned = df_cleaned[(df_cleaned["prep_time (in mins)"] >= lower_bound) & (df_cleaned["prep_time (in mins)"] <= upper_bound)]

# Enregistrer le dataset nettoyé
df_cleaned.to_csv("~/Food_Recipe_cleaned.csv", index=False)
print("\nLes données nettoyées ont été enregistrées sous 'Food_Recipe_cleaned.csv'.")





#gestion des valeurs manquantes : Suppression des lignes incomplètes.
#Élimination des doublons : Suppression des entrées répétées.
#Détection des outliers sur prep time via un boxplot et suppression par la méthode IQR.
#Sauvegarde du dataset nettoyé sous Food_Recipe_cleaned.csv.
