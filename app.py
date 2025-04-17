import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender import RecipeRecommender
from search import search_by_name, search_by_ingredients, search_by_category, search_by_filters, display_recipe, display_recommendations  # Import display_recipe

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Recipe_cleaned.csv")
    df = df.dropna(subset=["image_url", "ingredients_name", "name"])
    return df

df = load_data()
recommender = RecipeRecommender(df)

# Titre principal
st.title("🍽️ Recommandateur de Recettes")

# Barre de navigation
page = st.sidebar.selectbox("Navigation", ["Accueil", "Rechercher par nom", "What's in your kitchen?", "Popular", "Recommandations"])

if page == "Accueil":
    st.subheader("🔥 Here's some food I recommend you")
    random_recipes = df.sample(9)

    cols = st.columns(3)
    for i, (idx, row) in enumerate(random_recipes.iterrows()):
        with cols[i % 3]:
            try:
                response = requests.get(row["image_url"], timeout=5)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content)).resize((300, 300))
                    st.image(image)
                else:
                    st.image("https://via.placeholder.com/300", caption="Image non dispo")
            except:
                st.image("https://via.placeholder.com/300", caption="Image non dispo")
            st.write(f"**{row['name']}**")
            total_time = int(row['prep_time (in mins)']) + int(row['cook_time (in mins)'])
            st.write(f"Temps total: {total_time} minutes")

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

elif page == "Recommandations":
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
            all_similar = all_similar.drop_duplicates(subset="name")
            all_similar = all_similar[~all_similar["name"].isin(matching_recipes["name"])]

            if not all_similar.empty:
                st.markdown("---")
                st.subheader("📌 Recettes similaires à ce que vous avez cherché :")
                display_recommendations(all_similar.head(10))  # Top 5 suggestions
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
