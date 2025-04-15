import streamlit as st
import pandas as pd
from search import search_by_name, search_by_ingredients, search_by_category

# Charger les données dès l'ouverture du site
@st.cache_data
def load_data():
    return pd.read_csv("Food_Recipe_cleaned.csv")  # Chargement auto

df = load_data()  # On stocke les données

# Interface utilisateur
st.title("🍽️ Recommandateur de Recettes")

# Barre de navigation
page = st.sidebar.selectbox("Navigation", ["Accueil", "Rechercher par nom", "What's in your kitchen?", "Popular"])

if page == "Accueil":
    st.write("Bienvenue sur le Recommandateur de Recettes ! Utilisez la barre de navigation pour commencer.")
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
elif page == "Popular":
    st.header("Popular Recipes")
    category = st.selectbox("Choisissez une catégorie :", ["Easy Dinner", "Under 30 Minutes", "Chicken", "Breakfast", "Desserts"])
    if st.button("Rechercher"):
        search_by_category(df, category)

# Ajouter des boutons pour les filtres
st.sidebar.header("Filtres")
difficulty = st.sidebar.radio("Difficulty", ["Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"])
diets = st.sidebar.radio("Diets", ["Non Vegetarian", "Vegetarian", "Eggtarian"])
meal = st.sidebar.radio("Meal", ["Dinner", "Breakfast", "Snack"])
cuisine = st.sidebar.radio("Cuisine", ["Japanese", "Indian", "Italian"])

if st.sidebar.button("Appliquer les filtres"):
    search_by_filters(df, difficulty, diets, meal, cuisine)

# Ajouter du style CSS personnalisé
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
