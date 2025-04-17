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
        return self.data.iloc[similar_indices][['name', 'image_url', 'prep_time (in mins)', 'cook_time (in mins)']]

    def display_recommendations(results):
    num_results = 9  # Nombre de résultats à afficher initialement
    displayed_results = results.head(num_results)

    cols = st.columns(3)
    for i, (_, row) in enumerate(displayed_results.iterrows()):
        with cols[i % 3]:
            try:
                response = requests.get(row["image_url"], timeout=5)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content)).resize((300, 300))
                    st.image(image)
                else:
                    st.image("https://via.placeholder.com/300", caption="Image non dispo")
            except:
                st.image("https://via.placeholder.com/300", caption="Image non dispo")
            st.markdown(f"**{row['name']}**")
            total_time = int(row['prep_time (in mins)']) + int(row['cook_time (in mins)'])
            st.markdown(f"🕒 {total_time} minutes")
            if st.button(f"Voir tout - {row['name']}"):
                st.write(f"### {row['name']}")
                st.write(f"**Cuisine**: {row['cuisine']}")
                st.write(f"**Temps de préparation**: {row['prep_time (in mins)']} minutes")
                st.write(f"**Temps de cuisson**: {row['cook_time (in mins)']} minutes")
                st.write(f"**Ingrédients**: {row['ingredients_name']}")
                st.write(f"**Description**: {row['description']}")

    if len(results) > num_results:
        if st.button("Voir plus de résultats"):
            st.write("### Toutes les recommandations")
            for i, (_, row) in enumerate(results.iterrows()):
                with cols[i % 3]:
                    try:
                        response = requests.get(row["image_url"], timeout=5)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content)).resize((300, 300))
                            st.image(image)
                        else:
                            st.image("https://via.placeholder.com/300", caption="Image non dispo")
                    except:
                        st.image("https://via.placeholder.com/300", caption="Image non dispo")
                    st.markdown(f"**{row['name']}**")
                    total_time = int(row['prep_time (in mins)']) + int(row['cook_time (in mins)'])
                    st.markdown(f"🕒 {total_time} minutes")
                    if st.button(f"Voir tout - {row['name']}"):
                        st.write(f"### {row['name']}")
                        st.write(f"**Cuisine**: {row['cuisine']}")
                        st.write(f"**Temps de préparation**: {row['prep_time (in mins)']} minutes")
                        st.write(f"**Temps de cuisson**: {row['cook_time (in mins)']} minutes")
                        st.write(f"**Ingrédients**: {row['ingredients_name']}")
                        st.write(f"**Description**: {row['description']}")
