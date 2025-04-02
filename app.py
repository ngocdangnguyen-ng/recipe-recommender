import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Application de Tourisme en Italie")
st.write("Bienvenue ! Veuillez entrer vos informations pour que nous puissions vous recommander un séjour en Italie.")

# Formulaire d'entrée
budget = st.number_input("Quel est votre budget ? (en €)", min_value=50, step=50)
duree = st.slider("Combien de jours ?", 1, 7, 3)

st.write(f"Votre budget : {budget}€")
st.write(f"Durée du séjour : {duree} jours")

# Exemples de recommandations en fonction du budget et de la durée
if budget >= 500 and duree >= 3:
    st.write("Voici vos recommandations pour un séjour de qualité en Italie :")
    st.write("### Hébergements")
    st.write("1. Hôtel Luxe Roma")
    st.write("2. Airbnb à Florence")
    
    st.write("### Sites à visiter")
    st.write("1. Le Colisée à Rome")
    st.write("2. La Galerie des Offices à Florence")
    
    st.write("### Restaurants")
    st.write("1. Restaurant Da Vinci à Rome")
    st.write("2. Pizzeria Gusto à Florence")
    
elif budget < 500 and duree <= 3:
    st.write("Pour un budget plus modeste, voici des suggestions adaptées :")
    st.write("### Hébergements")
    st.write("1. Auberge à Venise")
    st.write("2. Appartement Airbnb à Milan")
    
    st.write("### Sites à visiter")
    st.write("1. La Place Saint-Marc à Venise")
    st.write("2. Le Duomo à Milan")
    
    st.write("### Restaurants")
    st.write("1. Trattoria Pugliese à Venise")
    st.write("2. Panino Giusto à Milan")

# Option pour afficher un itinéraire
if st.button("Voir l'itinéraire suggéré"):
    st.write(f"Voici un itinéraire optimisé pour {duree} jours à {budget}€ :")
    # Exemple d'itinéraire simple
    for i in range(duree):
        st.write(f"Jour {i+1}: Visiter les monuments principaux, explorer la ville...")
