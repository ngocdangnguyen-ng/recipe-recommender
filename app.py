import streamlit as st
import pandas as pd
from search import search_by_name, search_by_ingredients

# 🔹 Charger les données dès l'ouverture du site
@st.cache_data
def load_data():
    return pd.read_csv("Food_Recipe_cleaned.csv")  # Chargement auto

df = load_data()  # On stocke les données

# 🔹 Interface utilisateur
st.title("🍽️ Recommandateur de Recettes")

# Barre de recherche principale
search_option = st.selectbox("Que voulez-vous faire ?", ["Rechercher par nom", "What's in your kitchen?"])

if search_option == "Rechercher par nom":
    recipe_name = st.text_input("Entrez un nom de recette :", "")
    if st.button("Rechercher"):
        search_by_name(df, recipe_name)

elif search_option == "What's in your kitchen?":
    st.write("Find recipes based on what you already have at home!")
    ingredients = st.text_input("Enter up to 3 ingredients separated by commas:", "")
    if st.button("Find recipes"):
        search_by_ingredients(df, ingredients)
