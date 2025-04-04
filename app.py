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
        st.write(recommendations)
    else:
        st.warning("Aucune recette similaire trouvée ! Essayez un autre nom.")
