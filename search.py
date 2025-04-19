import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

def search_by_ingredients(df, ingredients):

    if ingredients:

        ingredient_list = ingredients.split(',')

        filtered_recipes = df[df['ingredients_name'].apply(lambda x: all(ingredient.strip().lower() in x.lower() for ingredient in ingredient_list))]

        if not filtered_recipes.empty:

            st.write("### Recipes found: ")

            for index, row in filtered_recipes.iterrows():

                display_recipe(row)

        else:

            st.warning("No recipes found with these ingredients! Try other ingredients.")

    else:

        st.warning("Please enter ingredients for search.")
    
    if not filtered_recipes.empty:

        st.write(f"### Recipes for the category{category} :")

        for index, row in filtered_recipes.iterrows():

            display_recipe(row)

    else:

        st.warning(f"No recipes found for the category {category} !")


def search_by_filters(df, difficulty, diets, meal, cuisine, return_df=False):
    if difficulty != "All":
        if difficulty == "Under 1 Hour":
            df = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 60]
        elif difficulty == "Under 45 Minutes":
            df = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 45]
        elif difficulty == "Under 30 Minutes":
            df = df[(df["prep_time (in mins)"] + df["cook_time (in mins)"]) <= 30]

    if diets != "All":
        df = df[df["diet"].str.contains(diets, case=False, na=False)]
    if meal != "All":
        df = df[df["course"].str.contains(meal, case=False, na=False)]
    if cuisine != "All":
        df = df[df["cuisine"].str.contains(cuisine, case=False, na=False)]

    if return_df:
        return df

    if not df.empty:
        for _, row in df.iterrows():
            display_recipe(row)
    else:
        st.warning("No recipes found for the selected filters !")


def display_recipe(row):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if pd.notna(row.get("image_url")):
                try:
                    st.image(row["image_url"], width=150)  # Taille de l'image ajustée
                except Exception as e:
                    st.error(f"Error loading image : {str(e)}")
        with col2:
            st.subheader(row.get("name", "Name not available"))
            st.write("**Cuisine :**", row.get("cuisine", "Unspecified"))
            st.write("**Preparation time :**", row.get("prep_time (in mins)", "Unspecified"), "minutes")
            st.write("**Cooking time :**", row.get("cook_time (in mins)", "Unspecified"), "minutes")
            with st.expander("See all"):
                st.write("**Description :**", row.get("description", "Unspecified"))
                st.write("**Course :**", row.get("course", "Unspecified"))
                st.write("**Diet :**", row.get("diet", "Unspecified"))
                st.write("**Ingredients :**", row.get("ingredients_name", "Unspecified"))
                st.write("**Quantity of ingredients :**", row.get("ingredients_quantity", "Unspecified"))
                st.write("**Instructions :**", row.get("instructions", "Unspecified"))
                if pd.notna(row.get("image_url")):
                    try:
                        st.image(row["image_url"], caption=row.get("name", "Name not available"), width=300)  # Taille de l'image ajustée
                    except Exception as e:
                        st.error(f"Error loading image : {str(e)}")

