import pandas as pd
import pytest
from src.models.recommender import RecipeRecommender

def sample_data():
    return pd.DataFrame({
        'name': ['Chicken Curry', 'Beef Stew', 'Veggie Pasta'],
        'ingredients_name': ['chicken, curry powder, onion', 'beef, potato, carrot', 'pasta, tomato, zucchini'],
        'image_url': ['', '', ''],
        'prep_time (in mins)': [15, 20, 10],
        'cook_time (in mins)': [30, 60, 20],
        'cuisine': ['Indian', 'French', 'Italian'],
        'description': ['Spicy chicken curry', 'Hearty beef stew', 'Vegetarian pasta'],
        'course': ['Main', 'Main', 'Main'],
        'diet': ['Non-Vegetarian', 'Non-Vegetarian', 'Vegetarian'],
        'ingredients_quantity': ['200g, 2tbsp, 1', '300g, 2, 1', '100g, 2, 1'],
        'instructions': ['Cook chicken...', 'Cook beef...', 'Cook pasta...']
    })

def test_get_similar_recipes():
    df = sample_data()
    recommender = RecipeRecommender(df)
    result = recommender.get_similar_recipes('Chicken Curry', top_n=2)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'name' in result.columns
    assert 'ingredients_name' in result.columns
    # Check that the recommended recipes are not the input recipe
    assert 'Chicken Curry' not in result['name'].values

def test_recipe_not_found():
    df = sample_data()
    recommender = RecipeRecommender(df)
    result = recommender.get_similar_recipes('Nonexistent Recipe')
    assert result.empty
