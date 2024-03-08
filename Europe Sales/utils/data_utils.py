import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df_full = pd.read_csv('data/Europe Sales Records.csv')
    return df_full