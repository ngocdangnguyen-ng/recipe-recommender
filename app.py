import streamlit as st
import pandas as pd

from obtain_data import load_data  # Tu dois avoir une fonction dans obtain_data.py
from scrub import clean_data
from explore import explore_data
from model import recommend_recipes

# Titre de l'app
st.title("🍽️ Recommandateur de Recettes")

# Étapes dans la barre latérale
step = st.sidebar.radio("Étapes du projet :", ["Obtain", "Scrub", "Explore", "Model"])

# Chargement des données CSV
if "data" not in st.session_state:
    st.session_state.data = None

# OBTAIN
if step == "Obtain":
    st.header("📥 Collecte des données")
    uploaded_file = st.file_uploader("Chargez le fichier foodrecipe.csv", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        st.session_state.data = df
        st.success("Données chargées avec succès")
        st.write(df.head())

# SCRUB
elif step == "Scrub":
    st.header("🧹 Nettoyage des données")
    if st.session_state.data is not None:
        cleaned_df = clean_data(st.session_state.data)
        st.session_state.data = cleaned_df
        st.write(cleaned_df.head())
    else:
        st.warning("Veuillez d'abord charger les données dans l'étape 'Obtain'.")

# EXPLORE
elif step == "Explore":
    st.header("🔍 Exploration des données")
    if st.session_state.data is not None:
        explore_data(st.session_state.data)  # doit contenir du code streamlit dans explore.py
    else:
        st.warning("Veuillez d'abord charger et nettoyer les données.")

# MODEL
elif step == "Model":
    st.header("🤖 Recommandation de recettes")
    if st.session_state.data is not None:
        recipe_name = st.text_input("Entrez le nom d’un plat :")
        if st.button("Recommander"):
            recommendations = recommend_recipes(st.session_state.data, recipe_name)
            st.write("Recettes similaires :")
            st.write(recommendations)
    else:
        st.warning("Veuillez d'abord charger et nettoyer les données.")
