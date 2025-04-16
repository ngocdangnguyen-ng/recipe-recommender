import streamlit as st
import pandas as pd

def search_by_name(df, name):
    results = df[df["name"].str.contains(name, case=False, na=False)]

    if results.empty:
        st.warning("Aucune recette trouvée.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            st.subheader(row["name"])
            st.write(row["description"])

            if st.button(f"Ajouter aux favoris - name_{i}", key=f"fav_name_{i}"):
                recipe_dict = row.to_dict()
                if recipe_dict not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe_dict)
                    st.success("Ajouté aux favoris !")
                else:
                    st.info("Déjà dans vos favoris.")

def search_by_ingredients(df, ingredients_str):
    ingredients = [i.strip().lower() for i in ingredients_str.split(",")]
    mask = df["ingredients_name"].apply(lambda x: any(ing in str(x).lower() for ing in ingredients))

    results = df[mask]

    if results.empty:
        st.warning("Aucune recette trouvée.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            st.subheader(row["name"])
            st.write("**Ingrédients :**", row["ingredients_name"])
            st.write(row["description"])

            if st.button(f"Ajouter aux favoris - ing_{i}", key=f"fav_ing_{i}"):
                recipe_dict = row.to_dict()
                if recipe_dict not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe_dict)
                    st.success("Ajouté aux favoris !")
                else:
                    st.info("Déjà dans vos favoris.")

def search_by_category(df, category):
    results = df[df["category"] == category]

    if results.empty:
        st.warning("Aucune recette trouvée pour cette catégorie.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            st.subheader(row["name"])
            st.write(row["description"])

            if st.button(f"Ajouter aux favoris - cat_{i}", key=f"fav_cat_{i}"):
                recipe_dict = row.to_dict()
                if recipe_dict not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe_dict)
                    st.success("Ajouté aux favoris !")
                else:
                    st.info("Déjà dans vos favoris.")

def search_by_filters(df, difficulty, diet, meal, cuisine):
    results = df[
        (df["difficulty"] == difficulty)
        & (df["diet"] == diet)
        & (df["course"] == meal)
        & (df["cuisine"] == cuisine)
    ]

    if results.empty:
        st.warning("Aucune recette trouvée avec ces filtres.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            st.subheader(row["name"])
            st.write("**Cuisine :**", row["cuisine"])
            st.write("**Temps de préparation :**", row["prep_time (in mins)"], "minutes")
            st.write("**Temps de cuisson :**", row["cook_time (in mins)"], "minutes")
            st.write(row["description"])

            if st.button(f"Ajouter aux favoris - filt_{i}", key=f"fav_filt_{i}"):
                recipe_dict = row.to_dict()
                if recipe_dict not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe_dict)
                    st.success("Ajouté aux favoris !")
                else:
                    st.info("Déjà dans vos favoris.")
