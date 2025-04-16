import streamlit as st
import pandas as pd

def display_favorites():
    st.title("Mes recettes favorites")

    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            display_favorite_recipe(fav)
    else:
        st.info("Vous n'avez pas encore ajouté de recettes aux favoris.")

def display_favorite_recipe(recipe):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if pd.notna(recipe["image_url"]):
                st.image(recipe["image_url"], width=150)
        with col2:
            st.subheader(recipe["name"])
            st.write("**Cuisine :**", recipe["cuisine"])
            st.write("**Temps de préparation :**", recipe["prep_time (in mins)"], "minutes")
            st.write("**Temps de cuisson :**", recipe["cook_time (in mins)"], "minutes")
            with st.expander("Voir tout"):
                st.write("**Description :**", recipe["description"])
                st.write("**Course :**", recipe["course"])
                st.write("**Diet :**", recipe["diet"])
                st.write("**Ingrédients :**", recipe["ingredients_name"])
                st.write("**Quantité des ingrédients :**", recipe["ingredients_quantity"])
                st.write("**Instructions :**", recipe["instructions"])
                if pd.notna(recipe["image_url"]):
                    st.image(recipe["image_url"], caption=recipe["name"], width=300)
