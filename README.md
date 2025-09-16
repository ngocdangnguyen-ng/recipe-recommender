# Recipe Recommender – Academic Project

## Project Overview
This project was developed as part of my coursework in **Projet Informatique** during my Computer Science program at **Aix-Marseille University**. The objective was to design and implement a modular recipe recommender system, practicing the full workflow of data-driven application development: from exploratory data analysis and feature engineering to model development, evaluation, and deployment.

**Objective:**
To create a robust recipe recommendation system using a large international cuisine dataset, enabling users to discover recipes based on ingredients, dietary preferences, cuisine, and more.

## Key Results
| Functionality                | Description                                      | Notes                          |
|------------------------------|--------------------------------------------------|---------------------------------|
| Ingredient Search            | Find recipes by available ingredients            | Case-insensitive, multi-input   |
| Filter-Based Search          | Filter recipes by time, diet, cuisine, course    | Supports combinations          |
| Recommendation Engine        | Suggest similar recipes using ML models          | Cosine similarity, vectorized   |
| Performance                  | Fast, scalable, real-time search                 | Optimized for large datasets    |
| Edge Case Handling           | Robust to empty, invalid, or rare inputs         | Error messages, fallback logic  |
| Web App                      | Streamlit-based, modern UI, interactive filters  | Ready for production            |

All main features have been tested and validated for accuracy, speed, and usability. The system is ready for real-world deployment.

## Features
* End-to-end workflow: EDA, feature engineering, modeling, search/filter experiments, deployment
* Modular, reusable codebase (Python, Streamlit, pytest)
* Ingredient-based and multi-criteria search
* Cosine similarity-based recommendations
* Automated data cleaning and preprocessing
* Professional visualizations and reporting (matplotlib, seaborn)
* Test coverage for core functions (pytest)
* Ready-to-use web interface (Streamlit)

## Getting Started
**Installation**
```
git clone https://github.com/ngocdangnguyen-ng/recipe-recommender.git
cd recipe-recommender
pip install -r requirements.txt
```
**Quick Example**
```python
import pandas as pd
from src.models.recommender import RecipeRecommender

df = pd.read_csv('data/cleaned/Food_Recipe_cleaned.csv')
recommender = RecipeRecommender(df)

# Find similar recipes
results = recommender.get_similar_recipes('Dim Posto Recipe - Bengali Egg Curry With Poppy Seeds')
print(results.head())
```

## Project Structure
```
recipe-recommender/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling_recommender.ipynb
│   └── 04_search_and_filters_experiments.ipynb
│
├── src/
│   ├── data/
│   ├── models/
│   ├── scripts/
│   ├── utils/
│   └── __init__.py
│
├── app/
│   └── app.py
│
├── tests/
│   ├── test_recommender.py
│   └── test_search.py
```

## Process Overview
1. **Exploratory Data Analysis:** Analyzed 7,000+ international recipes, visualized distributions, and identified key features
2. **Feature Engineering:** Created new features for improved search and recommendation
3. **Modeling:** Built and validated recommendation engine using cosine similarity and vectorization
4. **Search & Filter Experiments:** Tested ingredient and filter-based search, edge cases, and performance
5. **Deployment:** Developed a Streamlit web app for interactive recipe discovery

## What I Learned & Challenges
* **Data Preprocessing:** Cleaned and standardized recipe data, handled missing and inconsistent values
* **Feature Engineering:** Designed features for search and recommendation (ingredient vectors, filters)
* **Model Selection:** Implemented and compared search/recommendation strategies
* **Evaluation:** Used test coverage and performance metrics for robust assessment
* **Code Organization:** Modular, maintainable Python code and reproducible pipeline

**Key Insights:**
* Ingredient-based search is highly effective for user-driven discovery
* Combining multiple filters (time, diet, cuisine, course) improves relevance
* Cosine similarity enables accurate recommendations for similar recipes

## Limitations & Future Work
* Dataset limited to available Kaggle recipes
* Advanced recommendation models (e.g., neural networks) not yet explored
* Further feature engineering and explainability planned
* Add more domain-specific filters and user personalization
* Integrate hyperparameter tuning and model selection
* Expand deployment options (REST API, cloud platforms)
* Enhance reporting and user feedback

## Contact
- **Email**: [nndnguyen2016@gmail.com](mailto:nndnguyen2016@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/ngocnguyen-fr](https://www.linkedin.com/in/ngocnguyen-fr)
* **Portfolio:** [https://portfolio-qyyg.onrender.com](https://portfolio-qyyg.onrender.com)

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.