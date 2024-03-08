import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from utils.data_utils import load_data
st.set_page_config(layout="wide")
df = load_data()

def build_page():
    st.title("Vendas na Europa")
    st.write('Fonte dos dados: https://www.kaggle.com/datasets/mustafabayar/europe-sales-records')
    col1, col2 = st.columns(2)

    total_paises = df['Country'].nunique()
    total_itens = df['Item Type'].nunique()


    with col1:
        st.metric('Países', total_paises)
    with col2:
        st.metric('Tipos de Itens', total_itens)
    
    st.title('Total de itens Vendidos por País')

    graph_col1 = st.columns(1)[0]

    with graph_col1:

        df_agrupado_pelo_pais = df.groupby(['Country'], sort=False).agg({'Units Sold':np.sum}).reset_index()
        df_agrupado_pelo_pais = df_agrupado_pelo_pais.sort_values(by='Units Sold', ascending=False)
        fig = px.bar(df_agrupado_pelo_pais, x='Country', y='Units Sold', color='Country')
        fig.update_layout(
                xaxis_title='Países',  # Nome do eixo x será o nome da primeira coluna do DataFrame
                yaxis_title='Vendas',   # Nome do eixo y será o nome da segunda coluna do DataFrame
                title={'text': 'Total de Vendas por País', 'x': 0.5} # Centraliza o titulo
                )
        st.plotly_chart(fig, use_container_width=True)

        top_10_pais_venda = df_agrupado_pelo_pais.sort_values(by='Units Sold', ascending=False).head(10)
        st.markdown('**Top 10 Países com mais itens vendidos**')
        st.dataframe(top_10_pais_venda, hide_index=True)

build_page()




