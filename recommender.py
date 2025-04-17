import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecipeRecommender:
    def __init__(self, data):
        self.data = data.copy()
        self.vectorizer = CountVectorizer(stop_words='english')
        self.similarity_matrix = None
        self._prepare()

    def _prepare(self):
        # Vectorisation des ingrédients
        self.data['ingredients_name'] = self.data['ingredients_name'].fillna("")
        ingredient_matrix = self.vectorizer.fit_transform(self.data['ingredients_name'])
        self.similarity_matrix = cosine_similarity(ingredient_matrix, ingredient_matrix)

   def get_similar_recipes(self, recipe_name, top_n=9):
        if recipe_name not in self.data['name'].values:
            return pd.DataFrame()
    
        idx = self.data.index[self.data['name'] == recipe_name][0]
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
        # Exclure la recette elle-même (indice 0)
        similar_indices = [i for i, _ in similarity_scores[1:top_n+1]]
        return self.data.iloc[similar_indices][['name', 'image_url', 'prep_time (in mins)', 'cook_time (in mins)', 
                                                'cuisine', 'description', 'course', 'diet', 'ingredients_name', 'ingredients_quantity', 'instructions']]
