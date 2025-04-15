import streamlit as st
import pandas as pd
from model import recommend_recipes  # On importe la fonction corrigée

# 🔹 Charger les données dès l'ouverture du site
@st.cache_data
def load_data():
    return pd.read_csv("Food_Recipe_cleaned.csv")  # Chargement auto

df = load_data()  # On stocke les données

# 🔹 Interface utilisateur
st.title("🍽️ Recommandateur de Recettes")

# 🔎 Recherche de recettes similaires
recipe_name = st.text_input("Entrez un nom de recette :", "")
if st.button("Rechercher"):
    recommendations = recommend_recipes(df, recipe_name)
    if not recommendations.empty:
        st.write("Recettes similaires :")
        for index, row in recommendations.iterrows():
            with st.expander(row["name"]):
                st.write("**Description :**", row["description"])
                st.write("**Cuisine :**", row["cuisine"])
                st.write("**Course :**", row["course"])
                st.write("**Diet :**", row["diet"])
                st.write("**Ingrédients :**", row["ingredients_name"])
                st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                st.write("**Temps de préparation :**", row["prep_time (in mins)"], "minutes")
                st.write("**Temps de cuisson :**", row["cook_time (in mins)"], "minutes")
                st.write("**Instructions :**", row["instructions"])
                if pd.notna(row["image_url"]):
                    st.image(row["image_url"], caption=row["name"])
    else:
        st.warning("Aucune recette similaire trouvée ! Essayez un autre nom.")
