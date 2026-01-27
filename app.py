import streamlit as st
import pandas as pd
import plotly.express as px

st.title("日本の人口の推移")

df = pd.read_csv("./population_trends.csv")
header_cols = df.columns[1:]
col_series = pd.Series(header_cols)

with st.sidebar:
    st.header("絞り込み条件")
    select_year = st.selectbox(
        "年を選択",
        options=col_series.str.split('_').str[0].unique()
    )