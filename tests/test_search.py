import pandas as pd
import pytest
from src.utils.search import search_by_ingredients, search_by_filters

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

def test_search_by_ingredients_found(capsys):
    df = sample_data()
    search_by_ingredients(df, "chicken", use_streamlit=False)
    captured = capsys.readouterr()
    assert "Recipes found" in captured.out
    assert "Chicken Curry" in captured.out

def test_search_by_ingredients_not_found(capsys):
    df = sample_data()
    search_by_ingredients(df, "fish", use_streamlit=False)
    captured = capsys.readouterr()
    assert "No recipes found" in captured.out

def test_search_by_ingredients_empty(capsys):
    df = sample_data()
    search_by_ingredients(df, "", use_streamlit=False)
    captured = capsys.readouterr()
    assert "Please enter ingredients for search" in captured.out

def test_search_by_filters_found(capsys):
    df = sample_data()
    search_by_filters(df, "Under 1 Hour", "All", "All", "All")
    captured = capsys.readouterr()
    assert "Chicken Curry" in captured.out or "Veggie Pasta" in captured.out

def test_search_by_filters_not_found(capsys):
    df = sample_data()
    search_by_filters(df, "Under 5 Minutes", "All", "All", "All")
    captured = capsys.readouterr()
    assert "No recipes found" in captured.out

def test_search_by_filters_return_df():
    df = sample_data()
    result = search_by_filters(df, "Under 1 Hour", "All", "All", "All", return_df=True)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
