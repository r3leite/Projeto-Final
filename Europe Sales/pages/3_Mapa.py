import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px
from utils.data_utils import load_data
from geopy.geocoders import Nominatim

df = load_data()

def get_country_center(country_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(country_name)
    return location.latitude, location.longitude

def build_page():
    st.title('Vendas por País')

    # Adicionando o controle de seleção de país
    selected_country = st.selectbox('Selecione um país', df['Country'].unique())

    # Obtendo as coordenadas do centro do país selecionado
    center_lat, center_lon = get_country_center(selected_country)

    # Filtrando os dados com base no país selecionado
    df_country = df[df['Country'] == selected_country]

    # Criando o mapa com base nas vendas totais
    fig = px.choropleth(df_country, 
                        locations='Country', 
                        locationmode='country names',
                        color='Total Profit', 
                        hover_name='Country', 
                        color_continuous_scale='Viridis',
                        title='Vendas Totais por País',
                        labels={'Total Sales': 'Vendas Totais'})

    # Ajustando o layout do mapa
    fig.update_geos(
        center=dict(lon=center_lon, lat=center_lat),
        projection_scale=4,
        showcountries=True,  # Exibir nomes dos países
        countrycolor='gray',  # Cor das fronteiras dos países
        showland=True,  # Exibir as áreas de terra
        landcolor='rgb(217, 217, 217)',  # Cor das áreas de terra
        showocean=True,  # Exibir oceano
        oceancolor='rgb(0, 204, 255)',  # Cor do oceano
        showcoastlines=True,  # Exibir linhas costeiras
        showframe=False,  # Ocultar borda do mapa
    )

    st.plotly_chart(fig, use_container_width=True)

# Chamando a função para construir a página
build_page()