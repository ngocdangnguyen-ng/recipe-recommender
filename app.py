import streamlit as st
import pandas as pd
import numpy as np
import os

# Importer les fonctions depuis vos autres fichiers Python
from obtain import collect_data
from scrub import clean_data
from explore import explore_data
from model import recommend_recipes

# Configuration de l'application Streamlit
st.title("Système de recommandation de recettes")

# Sidebar pour choisir l'étape
step = st.sidebar.selectbox("Sélectionner l'étape", ["Collecte des données", "Nettoyage des données", "Exploration des données", "Modélisation", "Recommandations"])

# Collecte des données
if step == "Collecte des données":
    st.subheader("Collecte des données")
    # Affichage des options et récupération des données
    if st.button("Collecter les données"):
        data = collect_data()
        st.write("Données collectées :")
        st.write(data.head())  # Afficher un aperçu des données

# Nettoyage des données
elif step == "Nettoyage des données":
    st.subheader("Nettoyage des données")
    # Affichage de la donnée brute avant nettoyage
    if 'data' in locals():
        st.write("Données avant nettoyage :")
        st.write(data.head())
        # Nettoyage
        if st.button("Nettoyer les données"):
            cleaned_data = clean_data(data)
            st.write("Données nettoyées :")
            st.write(cleaned_data.head())  # Afficher les données nettoyées
    else:
        st.write("Aucune donnée disponible. Veuillez d'abord collecter les données.")

# Exploration des données
elif step == "Exploration des données":
    st.subheader("Exploration des données")
    if 'cleaned_data' in locals():
        # Exploration des données
        st.write("Données nettoyées prêtes pour l'exploration :")
        st.write(cleaned_data.head())
        if st.button("Explorer les données"):
            stats, visuals = explore_data(cleaned_data)
            st.write(stats)
            st.pyplot(visuals)  # Afficher les graphiques de l'exploration
    else:
        st.write("Aucune donnée nettoyée disponible. Veuillez d'abord nettoyer les données.")

# Modélisation du système de recommandation
elif step == "Modélisation":
    st.subheader("Modélisation du système de recommandation")
    if 'cleaned_data' in locals():
        # Modélisation du système de recommandation
        st.write("Modélisation en cours...")
        if st.button("Créer le modèle"):
            model = recommend_recipes(cleaned_data)
            st.write("Modèle créé avec succès.")
    else:
        st.write("Aucune donnée nettoyée disponible. Veuillez d'abord nettoyer les données.")

# Recommandations
elif step == "Recommandations":
    st.subheader("Obtenir des recommandations de recettes")
    if 'model' in locals():
        # Demander à l'utilisateur un plat pour obtenir une recommandation
        dish = st.text_input("Entrez un plat (ex: 'Pâtes') pour obtenir une recommandation de recettes similaires")
        if st.button("Obtenir la recommandation"):
            recommended_recipes = model(dish)
            st.write("Recettes recommandées :")
            st.write(recommended_recipes)
    else:
        st.write("Le modèle n'est pas encore créé. Veuillez d'abord créer le modèle.")
