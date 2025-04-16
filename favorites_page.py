import streamlit as st
import pandas as pd

# Initialisation des favoris
if "favorites" not in st.session_state:
    st.session_state.favorites = []

def display_recipe(row):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if pd.notna(row["image_url"]):
                st.image(row["image_url"], width=150)
        with col2:
            st.subheader(row["name"])
            st.write("**Cuisine :**", row["cuisine"])
            st.write("**Temps de préparation :**", row["prep_time (in mins)"], "minutes")
            st.write("**Temps de cuisson :**", row["cook_time (in mins)"], "minutes")
            with st.expander("Voir tout"):
                st.write("**Description :**", row["description"])
                st.write("**Course :**", row["course"])
                st.write("**Diet :**", row["diet"])
                st.write("**Ingrédients :**", row["ingredients_name"])
                st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                st.write("**Instructions :**", row["instructions"])
                if pd.notna(row["image_url"]):
                    st.image(row["image_url"], caption=row["name"], width=300)

def display_favorites():
    st.write("## Mes favoris")
    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            display_recipe(pd.Series(favorite))
    else:
        st.info("Aucune recette favorite pour le moment.")

# Affichage de la page des favoris
display_favorites()
