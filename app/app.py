import streamlit as st
import pandas as pd
from src.models.recommender import RecipeRecommender
from src.utils.search import search_by_filters, display_recipe

 # Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Recipe_cleaned.csv")
    df = df.dropna(subset=["image_url", "ingredients_name", "name"])
    return df

df = load_data()
recommender = RecipeRecommender(df)

# Navigation
page = st.sidebar.selectbox("Navigation", ["Home", "What's in your kitchen?", "Recommendations"])

 # Utility functions
def apply_filters(df, difficulty, diets, meal, cuisine):
    filtered = df.copy()
    if difficulty != "All":
    # Check that time columns exist
        if "prep_time (in mins)" in filtered.columns and "cook_time (in mins)" in filtered.columns:
            time_limit = {
                "Under 1 Hour": 60,
                "Under 45 Minutes": 45,
                "Under 30 Minutes": 30
            }.get(difficulty)
            filtered = filtered[
                (filtered["prep_time (in mins)"] + filtered["cook_time (in mins)"]) <= time_limit
            ]
    if diets != "All" and "diet" in filtered.columns:
        filtered = filtered[filtered["diet"].str.contains(diets, case=False, na=False)]
    if meal != "All" and "course" in filtered.columns:
        filtered = filtered[filtered["course"].str.contains(meal, case=False, na=False)]
    if cuisine != "All" and "cuisine" in filtered.columns:
        filtered = filtered[filtered["cuisine"].str.contains(cuisine, case=False, na=False)]
    return filtered


def show_recommendations(query, df, recommender, difficulty, diets, meal, cuisine):
    # Clean non-breaking spaces in DataFrame
    df['name'] = df['name'].apply(lambda x: x.replace('\u00A0', ' ') if isinstance(x, str) else x)

    # Search recipes by keyword
    mask = df["name"].str.contains(query, case=False, na=False)
    matching_recipes = df[mask]

    # Apply filters to found recipes
    filtered_matching_recipes = apply_filters(matching_recipes, difficulty, diets, meal, cuisine)

    if filtered_matching_recipes.empty:
        st.warning("No recipes found containing this word after applying filters.")
    else:
        st.success(f"{len(filtered_matching_recipes)} recipe(s) found containing '{query}' and matching filters:")
        for _, row in filtered_matching_recipes.iterrows():
            display_recipe(row)

    # Prepare similar recommendations from filtered recipes
    all_similar = pd.DataFrame()
    for _, row in filtered_matching_recipes.iterrows():
        similar = recommender.get_similar_recipes(row["name"])
        all_similar = pd.concat([all_similar, similar])

    # Remove duplicates and exclude already displayed recipes
    if "name" in all_similar.columns:
        all_similar = all_similar.drop_duplicates(subset="name")
        all_similar = all_similar[~all_similar["name"].isin(filtered_matching_recipes["name"])]
    else:
        st.error("The 'name' column is missing in similar recipes.")

    # Apply filters to similar recommendations
    filtered_similar = apply_filters(all_similar, difficulty, diets, meal, cuisine)

    if not filtered_similar.empty:
        st.markdown("---")
        st.subheader("📌 Filtered recommendations:")
        for _, row in filtered_similar.head(10).iterrows():
            display_recipe(row)
    else:
        st.info("No similar recipe to recommend after applying filters.")


# Page: Home
if page == "Home":
    st.markdown("## 🍽️ Recipe Recommendation Based on Your Preferences")

    # Dropdown menu for filters
    with st.expander("🔧 Show filters"):
        difficulty = st.selectbox("Difficulty", ["All", "Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"], key="filter_diff")
        diets = st.selectbox("Diets", ["All", "Non Vegetarian", "Vegetarian", "Eggtarian"], key="filter_diets")
        meal = st.selectbox("Meal", ["All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"], key="filter_meal")
        cuisine = st.selectbox("Cuisine", ["All", "Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"], key="filter_cuisine")

    # No need for a text field, force a default value
    query = " "  # or "all" depending on your implementation

    # Display recommendations after click
    if st.button("🍲 Show Recommendations"):
        show_recommendations(query, df, recommender, difficulty, diets, meal, cuisine)

            
# Page: What's in your kitchen?
elif page == "What's in your kitchen?":
    st.header("What's in your kitchen?")
    st.write("Find recipes based on what you already have at home!")

    ingredients = st.text_input("Enter up to 3 ingredients separated by commas:", "")

    if st.button("Find recipes"):
        ingredient_list = [ing.strip().lower() for ing in ingredients.split(",") if ing.strip()]
        filtered = df[df['ingredients_name'].apply(lambda x: all(ing in x.lower() for ing in ingredient_list))]

        if not filtered.empty:
            st.success(f"{len(filtered)} recipes found with those ingredients.")
            st.session_state['filtered_recipes'] = filtered
        else:
            st.warning("No recipes found with those ingredients.")
            st.session_state['filtered_recipes'] = pd.DataFrame()

    if 'filtered_recipes' in st.session_state and not st.session_state['filtered_recipes'].empty:
        filtered_df = st.session_state['filtered_recipes']

        difficulty = st.selectbox("Difficulty", ["All", "Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"])
        diets = st.selectbox("Diets", ["All", "Non Vegetarian", "Vegetarian", "Eggtarian"])
        meal = st.selectbox("Meal", ["All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"])
        cuisine = st.selectbox("Cuisine", ["All", "Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"])

        result = apply_filters(filtered_df, difficulty, diets, meal, cuisine)

        if not result.empty:
            for _, row in result.iterrows():
                display_recipe(row)
        else:
            st.warning("No recipes match the selected filters.")

# Page: Recommendations
elif page == "Recommendations":
    st.header("Recommendations")
    query = st.text_input("Enter a recipe name or keyword:")

    # Filters to apply
    difficulty = st.selectbox("Difficulty", ["All", "Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"], key="rec_difficulty")
    diets = st.selectbox("Diets", ["All", "Non Vegetarian", "Vegetarian", "Eggtarian"], key="rec_diets")
    meal = st.selectbox("Meal", ["All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"], key="rec_meal")
    cuisine = st.selectbox("Cuisine", ["All", "Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"], key="rec_cuisine")

    if st.button("Recommend"):
        if not query:
            st.error("Please enter a keyword.")
        else:
            show_recommendations(query, df, recommender, difficulty, diets, meal, cuisine)

 # Custom style
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6347;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #FF6347;
        border-radius: 8px;
        padding: 10px;
    }
    .stRadio>div>div>div>label {
        background-color: #FF6347;
        color: white;
        padding: 10px 20px;
        font-size: 14px;
        margin: 4px 2px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)
