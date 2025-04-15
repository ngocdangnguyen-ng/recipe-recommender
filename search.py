import streamlit as st

def search_by_name(df, recipe_name):
    recommendations = df[df["name"].str.contains(recipe_name, case=False, na=False)]
    if not recommendations.empty:
        st.write("### Recettes similaires :")
        for index, row in recommendations.iterrows():
            display_recipe(row)
    else:
        st.warning("Aucune recette similaire trouvée ! Essayez un autre nom.")

def search_by_ingredients(df, ingredients):
    if ingredients:
        ingredient_list = ingredients.split(',')
        filtered_recipes = df[df['ingredients_name'].apply(lambda x: all(ingredient.strip().lower() in x.lower() for ingredient in ingredient_list))]
        if not filtered_recipes.empty:
            st.write("### Recettes trouvées :")
            for index, row in filtered_recipes.iterrows():
                display_recipe(row)
        else:
            st.warning("Aucune recette trouvée avec ces ingrédients ! Essayez d'autres ingrédients.")
    else:
        st.warning("Veuillez entrer des ingrédients pour la recherche.")

def display_recipe(row):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if pd.notna(row["image_url"]):
                st.image(row["image_url"], width=150)  # Taille de l'image ajustée
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
                    st.image(row["image_url"], caption=row["name"], width=300)  # Taille de l'image ajustée
