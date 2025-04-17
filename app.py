import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender import RecipeRecommender
from search import search_by_name, search_by_ingredients, search_by_filters, display_recipe

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Recipe_cleaned.csv")
    df = df.dropna(subset=["image_url", "ingredients_name", "name"])  # On s'assure que les colonnes essentielles ne contiennent pas de valeurs manquantes
    return df

df = load_data()
recommender = RecipeRecommender(df)

# Barre de navigation
page = st.sidebar.selectbox("Navigation", ["Accueil", "Rechercher par nom", "What's in your kitchen?", "Recommandations"])

if page == "Accueil":
    st.header("👋 Bienvenue sur votre assistant recettes !")
    st.write("Utilisez le menu à gauche pour rechercher ou obtenir des recommandations.")

elif page == "Rechercher par nom":
    st.header("Rechercher par nom")
    recipe_name = st.text_input("Entrez un nom de recette :", "")
    if st.button("Rechercher"):
        search_by_name(df, recipe_name)

elif page == "What's in your kitchen?":
    st.header("What's in your kitchen?")
    st.write("Find recipes based on what you already have at home!")
    ingredients = st.text_input("Enter up to 3 ingredients separated by commas:", "")
    if st.button("Find recipes"):
        search_by_ingredients(df, ingredients)

# app.py
elif page == "Recommandations":
    st.header("Recommandations")
    query = st.text_input("Entrez un nom de recette ou un mot-clé :")

    if st.button("Recommander"):
        if not query:
            st.error("Veuillez entrer un mot-clé.")
        else:
            # Étape 1 : Rechercher les plats contenant le mot
            mask = df["name"].str.contains(query, case=False, na=False)
            matching_recipes = df[mask]

            if matching_recipes.empty:
                st.warning("Aucune recette trouvée contenant ce mot.")
            else:
                st.success(f"{len(matching_recipes)} recette(s) trouvée(s) contenant '{query}' :")
                for _, row in matching_recipes.iterrows():
                    display_recipe(row)

            # Étape 2 : Recommandations basées sur les recettes trouvées
            all_similar = pd.DataFrame()

            for _, row in matching_recipes.iterrows():
                similar = recommender.get_similar_recipes(row["name"])
                all_similar = pd.concat([all_similar, similar])

            # Enlever les doublons et les recettes déjà affichées
            if "name" in all_similar.columns:
                all_similar = all_similar.drop_duplicates(subset="name")
                all_similar = all_similar[~all_similar["name"].isin(matching_recipes["name"])]
            else:
                st.error("La colonne 'name' est manquante dans les recettes similaires.")

           if not all_similar.empty:
                st.markdown("---")
                st.subheader("📌 Recettes similaires à ce que vous avez cherché :")
                for _, row in all_similar:  # Affichage des 10 premières suggestions
                    display_recipe(row)
            else:
                st.info("Aucune recette similaire à recommander.")

# Filtres
st.sidebar.header("Filtres")
difficulty = st.sidebar.radio("Difficulty", ["All", "Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"])
diets = st.sidebar.radio("Diets", ["All", "Non Vegetarian", "Vegetarian", "Eggtarian"])
meal = st.sidebar.radio("Meal", ["All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"])
cuisine = st.sidebar.radio("Cuisine", ["All", "Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"])
if st.sidebar.button("Appliquer les filtres"):
    search_by_filters(df, difficulty, diets, meal, cuisine)

# Style CSS personnalisé
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6347;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #FF6347;
        border-radius: 8px;
        padding: 10px;
    }
    .stRadio>div>div>div>label {
        background-color: #FF6347;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
