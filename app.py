import streamlit as st

st.title("Application de Tourisme en Italie")
st.write("Bienvenue dans notre application qui recommande des séjours en Italie en fonction de votre budget et de la durée souhaitée.")

# Formulaire simple pour tester l'affichage
budget = st.number_input("Quel est votre budget ?", min_value=50, step=50)
duree = st.slider("Combien de jours ?", 1, 7, 3)

st.write(f"Votre budget : {budget}€")
st.write(f"Durée sélectionnée : {duree} jours")
