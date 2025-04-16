import streamlit as st
import pandas as pd

# Fonction d'ajout aux favoris
def add_to_favorites(recipe):
    if recipe not in st.session_state.favorites:
        st.session_state.favorites.append(recipe)
        st.success("Ajouté aux favoris !")
    else:
        st.info("Cette recette est déjà dans vos favoris.")

# Recherche par nom
def search_by_name(df, name):
    results = df[df["name"].str.contains(name, case=False, na=False)]
    
    if results.empty:
        st.warning("Aucune recette trouvée avec ce nom.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if pd.notna(row["image_url"]):
                        st.image(row["image_url"], width=150)
                with col2:
                    st.subheader(row["name"])
                    st.write("**Cuisine :**", row["cuisine"])
                    st.write("**Temps de préparation :**", row["prep_time (in mins)"], " minutes")
                    st.write("**Temps de cuisson :**", row["cook_time (in mins)"], " minutes")
                    with st.expander("Voir tout"):
                        st.write("**Description :**", row["description"])
                        st.write("**Course :**", row["course"])
                        st.write("**Diet :**", row["diet"])
                        st.write("**Ingrédients :**", row["ingredients_name"])
                        st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                        st.write("**Instructions :**", row["instructions"])
                    if st.button(f"Ajouter aux favoris - name_{i}", key=f"fav_name_{i}"):
                        add_to_favorites(row.to_dict())

# Recherche par ingrédients
def search_by_ingredients(df, ingredients_str):
    ingredients = [i.strip().lower() for i in ingredients_str.split(",")]
    mask = df["ingredients_name"].apply(lambda x: any(ing in str(x).lower() for ing in ingredients))

    results = df[mask]

    if results.empty:
        st.warning("Aucune recette trouvée avec ces ingrédients.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if pd.notna(row["image_url"]):
                        st.image(row["image_url"], width=150)
                with col2:
                    st.subheader(row["name"])
                    st.write("**Cuisine :**", row["cuisine"])
                    st.write("**Temps de préparation :**", row["prep_time (in mins)"], " minutes")
                    st.write("**Temps de cuisson :**", row["cook_time (in mins)"], " minutes")
                    with st.expander("Voir tout"):
                        st.write("**Description :**", row["description"])
                        st.write("**Course :**", row["course"])
                        st.write("**Diet :**", row["diet"])
                        st.write("**Ingrédients :**", row["ingredients_name"])
                        st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                        st.write("**Instructions :**", row["instructions"])
                    if st.button(f"Ajouter aux favoris - ing_{i}", key=f"fav_ing_{i}"):
                        add_to_favorites(row.to_dict())

# Recherche par catégorie
def search_by_category(df, category):
    results = df[df["course"].str.contains(category, case=False, na=False)]

    if results.empty:
        st.warning(f"Aucune recette trouvée pour la catégorie {category}.")
    else:
        for i, (_, row) in enumerate(results.iterrows()):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if pd.notna(row["image_url"]):
                        st.image(row["image_url"], width=150)
                with col2:
                    st.subheader(row["name"])
                    st.write("**Cuisine :**", row["cuisine"])
                    st.write("**Temps de préparation :**", row["prep_time (in mins)"], " minutes")
                    st.write("**Temps de cuisson :**", row["cook_time (in mins)"], " minutes")
                    with st.expander("Voir tout"):
                        st.write("**Description :**", row["description"])
                        st.write("**Course :**", row["course"])
                        st.write("**Diet :**", row["diet"])
                        st.write("**Ingrédients :**", row["ingredients_name"])
                        st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                        st.write("**Instructions :**", row["instructions"])
                    if st.button(f"Ajouter aux favoris - cat_{i}", key=f"fav_cat_{i}"):
                        add_to_favorites(row.to_dict())

# Recherche avec filtres (difficulté, régime, etc.)
def search_by_filters(df, difficulty, diet, meal, cuisine):
    filtered_df = df.copy()

    if difficulty:
        filtered_df = filtered_df[filtered_df["difficulty"] == difficulty]

    if diet:
        filtered_df = filtered_df[filtered_df["diet"].str.contains(diet, case=False, na=False)]

    if meal:
        filtered_df = filtered_df[filtered_df["course"].str.contains(meal, case=False, na=False)]

    if cuisine:
        filtered_df = filtered_df[filtered_df["cuisine"].str.contains(cuisine, case=False, na=False)]

    if filtered_df.empty:
        st.warning("Aucune recette trouvée avec ces filtres.")
    else:
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if pd.notna(row["image_url"]):
                        st.image(row["image_url"], width=150)
                with col2:
                    st.subheader(row["name"])
                    st.write("**Cuisine :**", row["cuisine"])
                    st.write("**Temps de préparation :**", row["prep_time (in mins)"], " minutes")
                    st.write("**Temps de cuisson :**", row["cook_time (in mins)"], " minutes")
                    with st.expander("Voir tout"):
                        st.write("**Description :**", row["description"])
                        st.write("**Course :**", row["course"])
                        st.write("**Diet :**", row["diet"])
                        st.write("**Ingrédients :**", row["ingredients_name"])
                        st.write("**Quantité des ingrédients :**", row["ingredients_quantity"])
                        st.write("**Instructions :**", row["instructions"])
                    if st.button(f"Ajouter aux favoris - filt_{i}", key=f"fav_filt_{i}"):
                        add_to_favorites(row.to_dict())
