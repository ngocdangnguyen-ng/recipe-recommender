import streamlit as st

import pandas as pd  # Assurez-vous que pandas est importé


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


def search_by_category(df, category):

    if category == "Easy Dinner":

        filtered_recipes = df[df["course"].str.contains("dinner", case=False, na=False)]

    elif category == "Under 30 Minutes":

        filtered_recipes = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 30]

    elif category == "Chicken":

        filtered_recipes = df[df["ingredients_name"].str.contains("chicken", case=False, na=False)]

    elif category == "Breakfast":

        filtered_recipes = df[df["course"].str.contains("breakfast", case=False, na=False)]

    elif category == "Desserts":

        filtered_recipes = df[df["course"].str.contains("dessert", case=False, na=False)]

    

    if not filtered_recipes.empty:

        st.write(f"### Recettes pour la catégorie {category} :")

        for index, row in filtered_recipes.iterrows():

            display_recipe(row)

    else:

        st.warning(f"Aucune recette trouvée pour la catégorie {category} !")


def search_by_filters(df, difficulty, diets, meal, cuisine):
    if difficulty == "All":
        filtered_recipes = df
    elif difficulty == "Under 1 Hour":
        filtered_recipes = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 60]
    elif difficulty == "Under 45 Minutes":
        filtered_recipes = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 45]
    elif difficulty == "Under 30 Minutes":
        filtered_recipes = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 30]

    if diets != "All":
        filtered_recipes = filtered_recipes[filtered_recipes["diet"].str.contains(diets, case=False, na=False)]
    if meal != "All":
        filtered_recipes = filtered_recipes[filtered_recipes["course"].str.contains(meal, case=False, na=False)]
    if cuisine != "All":
        filtered_recipes = filtered_recipes[filtered_recipes["cuisine"].str.contains(cuisine, case=False, na=False)]

    if not filtered_recipes.empty:
        st.write(f"### Recettes pour les filtres sélectionnés :")
        for index, row in filtered_recipes.iterrows():
            display_recipe(row)
    else:
        st.warning("Aucune recette trouvée pour les filtres sélectionnés !")

def display_recipe(row):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if pd.notna(row.get("image_url")):
                st.image(row["image_url"], width=150)  # Taille de l'image ajustée
        with col2:
            st.subheader(row.get("name", "Nom non disponible"))
            st.write("**Cuisine :**", row.get("cuisine", "Non spécifié"))
            st.write("**Temps de préparation :**", row.get("prep_time (in mins)", "Non spécifié"), "minutes")
            st.write("**Temps de cuisson :**", row.get("cook_time (in mins)", "Non spécifié"), "minutes")
            with st.expander("Voir tout"):
                st.write("**Description :**", row.get("description", "Non spécifié"))
                st.write("**Course :**", row.get("course", "Non spécifié"))
                st.write("**Diet :**", row.get("diet", "Non spécifié"))
                st.write("**Ingrédients :**", row.get("ingredients_name", "Non spécifié"))
                st.write("**Quantité des ingrédients :**", row.get("ingredients_quantity", "Non spécifié"))
                st.write("**Instructions :**", row.get("instructions", "Non spécifié"))
                if pd.notna(row.get("image_url")):
                    st.image(row["image_url"], caption=row.get("name", "Nom non disponible"), width=300)  # Taille de l'image ajustée

def display_recommendations(results):
    num_results = 9  # Nombre de résultats à afficher initialement
    displayed_results = results.head(num_results)

    cols = st.columns(3)
    for i, (_, row) in enumerate(displayed_results.iterrows()):
        with cols[i % 3]:
            with st.container():
                image_url = row.get("image_url", "")
                if image_url:
                    try:
                        response = requests.get(image_url, timeout=5)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content)).resize((300, 300))
                            st.image(image)
                        else:
                            st.image("https://via.placeholder.com/300", caption="Image non dispo")
                    except requests.exceptions.RequestException:
                        st.image("https://via.placeholder.com/300", caption="Image non dispo")
                else:
                    st.image("https://via.placeholder.com/300", caption="Image non dispo")

                st.markdown(f"**{row['name']}**")
                total_time = int(row['prep_time (in mins)']) + int(row['cook_time (in mins)'])
                st.markdown(f"🕒 {total_time} minutes")
                if st.button(f"Voir tout - {row['name']}", key=f"btn_{row['name']}"):
                    st.write(f"### {row['name']}")
                    st.write(f"**Cuisine**: {row['cuisine']}")
                    st.write(f"**Temps de préparation**: {row['prep_time (in mins)']} minutes")
                    st.write(f"**Temps de cuisson**: {row['cook_time (in mins)']} minutes")
                    st.write(f"**Ingrédients**: {row['ingredients_name']}")
                    st.write(f"**Description**: {row['description']}")
