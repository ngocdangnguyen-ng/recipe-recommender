elif page == "Recommandations":
    st.title("🔍 Recommandation de recettes similaires")
    selected_recipe = st.selectbox("Choisissez une recette :", df["name"].unique())

    if st.button("Recommander"):
        results = recommender.get_similar_recipes(selected_recipe)
        if results.empty:
            st.warning("Aucune recommandation trouvée.")
        else:
            st.success(f"Voici des recettes similaires à **{selected_recipe}** :")
            num_results = st.slider("Nombre de résultats à afficher", min_value=3, max_value=20, value=9)
            cols = st.columns(3)
            for i, (_, row) in enumerate(results.head(num_results).iterrows()):
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

            if len(results) > num_results:
                if st.button("Voir tout"):
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
