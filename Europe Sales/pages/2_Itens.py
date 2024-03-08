import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
#import seaborn as sns

from utils.data_utils import load_data
df = load_data()
st.title('Vendas')

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Order Year'] = df['Order Date'].dt.year

def build_page():
    #Fazendo a listagem
    selected_pais = st.selectbox('Selecione um Pais', sorted(df['Country'].unique()), index=2)
    st.title(f'País - {selected_pais}')
    df_pais = df[df['Country'] == selected_pais]

    anos_disponiveis = df_pais['Order Year'].unique()
    selected_year = st.slider('Selecione um Ano', min_value=min(anos_disponiveis), max_value=max(anos_disponiveis), value=2014)
    df_ano_selecionado = df_pais[df_pais['Order Year'] == selected_year]

    selected_pais_vendas = df_ano_selecionado['Units Sold'].sum()
    selected_pais_tot = df_ano_selecionado['Total Profit'].sum()

    col1, col2 = st.columns(2)
    col1.metric(f'Quantidade de Vendas - {selected_pais}', selected_pais_vendas)
    col2.metric(f'Total de Lucro - {selected_pais}', f'{selected_pais_tot:,.2f}')
   

    st.title('Relação de Itens')
    #graph_col1, graph_col2 = st.columns(2)
    df_filtered = df[(df['Country'] == selected_pais) & (df['Order Year'] == selected_year)]
    df_agrupado_pelo_item = df_filtered.groupby('Item Type').agg({'Units Sold': 'sum'}).reset_index()


    fig = px.bar(df_agrupado_pelo_item, x='Item Type', y='Units Sold', color='Item Type')
    fig.update_layout(
        xaxis_title='Vendas',  # Nome do eixo x será o nome da primeira coluna do DataFrame
        yaxis_title='Itens',   # Nome do eixo y será o nome da segunda coluna do DataFrame
        title={'text': 'Vendas por item'} # Centraliza o titulo
        )
    st.plotly_chart(fig, use_container_width=True)

    df_ano_selecionado1 = df[df['Order Year'] == selected_year]

    df_agrupado_pelo_pais1 = df_ano_selecionado1.groupby(['Country'], sort=False).agg({'Total Profit':np.sum}).reset_index()
    df_agrupado_pelo_pais1 = df_agrupado_pelo_pais1.sort_values(by='Total Profit', ascending=False)

    top_10_pais_lucro = df_agrupado_pelo_pais1.sort_values(by='Total Profit', ascending=False).head(10)
    st.markdown('**Top 10 Países que Obtiveram Maior Lucro**')
    st.dataframe(top_10_pais_lucro, hide_index=True)


       
        

build_page()
