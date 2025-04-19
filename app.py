import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender import RecipeRecommender
from search import search_by_ingredients, search_by_filters, display_recipe

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Recipe_cleaned.csv")
    df = df.dropna(subset=["image_url", "ingredients_name", "name"])  # On s'assure que les colonnes essentielles ne contiennent pas de valeurs manquantes
    return df

df = load_data()
recommender = RecipeRecommender(df)

# Barre de navigation
page = st.sidebar.selectbox("Navigation", ["Home", "What's in your kitchen?", "Recommandations"])

if page == "Home":
    st.header("👋 Welcome to your recipe assistant !")
    st.write("Use the menu on the left to search or get recommendations.")

elif page == "What's in your kitchen?":
    st.header("What's in your kitchen?")
    ingredients = st.text_input("Enter up to 3 ingredients separated by commas:", "")

    if st.button("Find recipes"):
        ingredient_list = [i.strip().lower() for i in ingredients.split(',') if i.strip()]
        filtered_recipes = df[df['ingredients_name'].apply(lambda x: all(ing in x.lower() for ing in ingredient_list))]

        if filtered_recipes.empty:
            st.warning("Aucune recette trouvée avec ces ingrédients !")
        else:
            st.success(f"{len(filtered_recipes)} recette(s) trouvée(s)")

            # Filtres supplémentaires (appliqués après la recherche initiale)
            st.subheader("🔍 Affiner les résultats :")
            col1, col2 = st.columns(2)
            with col1:
                difficulty = st.selectbox("Temps de préparation", ["All", "Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"])
                diets = st.selectbox("Type de régime", ["All", "Non Vegetarian", "Vegetarian", "Eggtarian"])
            with col2:
                meal = st.selectbox("Type de plat", ["All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"])
                cuisine = st.selectbox("Cuisine", ["All", "Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"])

            # Appliquer les filtres sur les résultats trouvés
            filtered_recipes = search_by_filters(filtered_recipes, difficulty, diets, meal, cuisine, return_df=True)

            # Affichage
            for _, row in filtered_recipes.iterrows():
                display_recipe(row)


# app.py
elif page == "Recommandations":
    st.header("Recommandations")
    query = st.text_input("Enter a recipe name or keyword :")

    if st.button("Recommend"):
        if not query:
            st.error("Please enter a keyword.")
        else:
            # Étape 1 : Rechercher les plats contenant le mot
            mask = df["name"].str.contains(query, case=False, na=False)
            matching_recipes = df[mask]

            if matching_recipes.empty:
                st.warning("No recipes found containing this word.")
            else:
                st.success(f"{len(matching_recipes)} recipe(s) found containing '{query}':")
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
                st.error("The 'name' column is missing in similar recipes.")

           # Vérification correcte d'empty sur un DataFrame
            if not all_similar.empty:
                st.markdown("---")
                st.subheader("📌 Recipes similar to what you searched for:")
                for _, row in all_similar.head(10).iterrows():  # Affichage des 10 premières suggestions
                    display_recipe(row)
            else:
                st.info("No similar recipe to recommend.")

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
