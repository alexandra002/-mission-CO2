########################################################################
### Projet : Création d'un Dashboard avec streamlit                  ###
########################################################################

# Commande à insérer dans le terminal : 
# cd /Users/...
# streamlit run dash.py

###
#### Importation des librairies 
###

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

###
#### Configuration de la page
###

st.set_page_config(
    layout="wide",
    page_title="Émission de CO2 par pays",
)


st.title("Dashboard de l'émissions de CO2 en metricton par habitant de tous les pays du monde de 1990 à 2019 ♻️")
st.markdown(
    """
    Bienvenue dans ce Dashboard interactif qui explore l'émission de CO2 dans le monde de 1990 à 2019. Les données utilisées pour ce projet sont ceux du sites
    [Kaggle](https://www.kaggle.com/datasets/koustavghosh149/co2-emission-around-the-world/data).
    """
)

# Chargement des données
df = pd.read_csv('/Users/alexandra/iref/projetperso/CO2_emission.csv')

# Colonne des années disponibles dans le dataframe
available_years = [col for col in df.columns if col.isdigit()]

###
#### Sidebar
###

st.sidebar.title("🧮 Dashboard interactif : Je vous invite à manipuler les réglages de sélection")

# Bande latérale pour la sélection des pays et de l'année
selected_year = st.sidebar.slider('Sélectionner une année', min_value=1990, max_value=2019, value=1990)
selected_column = str(selected_year)
unique_countries = df['Country Name'].unique()
default_countries = ['France']
selected_countries = st.sidebar.multiselect('Sélectionner les pays', unique_countries, default=default_countries)

with st.sidebar:
    st.title("Projet")
    st.info(
    """
    Ce projet visait à réaliser mon premier Dashboard en utilisant des outils et fonctionnalités gratuites. 
    Pour cela, j'ai utilisée **Streamlit** qui transforme les scripts de données en applications Web partageables en quelques minutes.
    
    L'objectif étant de développer une visualisation interactive pertinente et facile d'utilisation,
    permettant aux utilisateurs d'explorer les données sur l'émission de CO2 par habitant 
    dans différents pays du monde sur une période de 1990 à 2019.
    Tout cela, en utilisant les bibliothèques Python telles que **Plotly Express**, **Altair** et **Pandas**.
    """,
    icon="📊",
)

# Affichage de l'image centrée dans la barre latérale avec style CSS
st.sidebar.image("co2.png", width=50, use_column_width=True)

st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[GitHub](https://github.com/alexandra002)  | Mai 2024 | [Alexandra MILLOT](https://www.linkedin.com/in/alexandramillot/)</small>''', unsafe_allow_html=True)

###
#### Graphiques
###

filtered_data = df[df['Country Name'].isin(selected_countries)] # Filtrage des données par pays sélectionnés

# Mise en forme des données pour Altair
melted_data = filtered_data.melt(id_vars=['Country Name', 'country_code', 'Region', 'Indicator Name'],
                                 value_vars=available_years,
                                 var_name='Year', value_name='CO2 Emissions')

melted_data['Year'] = pd.to_numeric(melted_data['Year'], errors='coerce') # Conversion de l'année en format numérique

# Carte choroplèthe
fig_map = px.choropleth(df,
                        locations='country_code',
                        color=selected_column,
                        hover_name='Country Name',
                        color_continuous_scale='RdYlGn_r',
                        projection='natural earth')
fig_map.update_layout(width=800, height=600)

# Graphique à barres
sorted_data = df[['Country Name', 'country_code', selected_column]].dropna().sort_values(by=selected_column, ascending=False).head(10)
bar_chart = px.bar(sorted_data, x='Country Name', y=selected_column, color='Country Name',
                   labels={'Country Name': 'Pays', selected_column: 'Consommation de CO2 par habitant'},
                   title=f"Top 10 des pays avec la plus haute consommation de CO2 par habitant en {selected_year}")

bar_chart.update_layout(
    xaxis_title=None,
    yaxis_title='Consommation de CO2 par habitant (metric tons per capita)',
    coloraxis_showscale=False,
    margin=dict(l=40, r=40, t=80, b=40),
    height=600  # Ajuster la hauteur du graphique à barres
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_map)

with col2:
    st.plotly_chart(bar_chart)

# Graphique avec Altair
chart = alt.Chart(melted_data).mark_line().encode(
    x='Year:O',
    y='CO2 Emissions:Q',
    color='Country Name:N',
    tooltip=['Country Name', 'Year', 'CO2 Emissions']
).properties(
    width=800,
    height=500
).interactive()

st.altair_chart(chart, use_container_width=True)