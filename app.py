import streamlit as st
import pandas as pd

# Importer les fonctions depuis vos autres fichiers Python
from scrub import clean_data
from explore import explore_data
from model import recommend_recipes

# Fonction de collecte des données
def collect_data():
    uploaded_file = st.file_uploader("Télécharger le fichier CSV des recettes", type=["csv"])
    
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Voici un aperçu des données :")
        st.write(data.head())
        return data
    return None

# Fonction principale
def main():
    st.title("Système de recommandation de recettes")
    
    step = st.sidebar.selectbox("Sélectionner l'étape", ["Collecte des données", "Nettoyage des données", "Exploration des données", "Modélisation", "Recommandations"])
    
    # Collecte des données
    if step == "Collecte des données":
        st.subheader("Collecte des données")
        data = collect_data()
    
    # Nettoyage des données
    if step == "Nettoyage des données" and data is not None:
        st.subheader("Nettoyage des données")
        cleaned_data = clean_data(data)
        st.write("Données nettoyées :")
        st.write(cleaned_data.head())
    
    # Exploration des données
    if step == "Exploration des données" and 'cleaned_data' in locals():
        st.subheader("Exploration des données")
        stats, visuals = explore_data(cleaned_data)
        st.write(stats)
        st.pyplot(visuals)
    
    # Modélisation
    if step == "Modélisation" and 'cleaned_data' in locals():
        st.subheader("Création du modèle de recommandation")
        model = recommend_recipes(cleaned_data)
        st.write("Modèle créé avec succès.")
    
    # Recommandations
    if step == "Recommandations" and 'model' in locals():
        st.subheader("Obtenir des recommandations de recettes")
        dish = st.text_input("Entrez un plat pour obtenir une recommandation")
        if st.button("Obtenir la recommandation"):
            recommended_recipes = model(dish)
            st.write("Recettes recommandées :")
            st.write(recommended_recipes)

if __name__ == "__main__":
    main()
