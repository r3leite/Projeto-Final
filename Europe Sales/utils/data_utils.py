import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df_full = pd.read_csv('data/Europe Sales Records.CSV')
    df_full = df_full[df_full.LAT!=0]
    df_full = df_full[df_full.AREA > 0]
    df_full['population_density'] = df_full['ESTIMATED_POP'] / df_full['AREA']
    df_full['estimated_pop_size'] = ((df_full['ESTIMATED_POP'] - df_full['ESTIMATED_POP'].min()) / df_full['ESTIMATED_POP'].max()) * 500000
    df_full['region'] = df_full['STATE'].apply(lambda x: map_region(x))
    return df_full