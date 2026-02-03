import streamlit as st
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go

# --- ページ設定 ---
st.set_page_config(page_title="日本の人口推移アプリ", layout="wide")

st.title("🇯🇵 日本の人口の推移")

st.markdown("""
### アプリの概要
このアプリは、 **e-Stat（政府統計ポータルサイト）** のオープンデータを使用し、日本の人口構成の変化を可視化したものです。
下のタブを切り替えることで、 **「ピラミッド型の構成」** と **「時系列の推移」** をそれぞれ詳しく確認できます。
""")


# データの読み込み
df = pd.read_csv("./population_trends.csv")
header_cols = df.columns[1:]
col_series = pd.Series(header_cols)
year = sorted(col_series.str.split('_').str[0].unique().astype(int))

with st.sidebar:
    st.write("表示設定")
    st.subheader("人口ピラミッド")
    select_year = st.slider(
        label='分析対象の年を選択してください', 
        min_value=min(year),
        max_value=max(year),
        value=min(year),
        step=1)
    
    st.divider()
    
    st.subheader("人口の長期推移")
    selected_color_label = st.multiselect(
        '人口の長期推移に表示する項目',
        options=['Total', 'male', 'female'],
        default=['Total']
    )

st.subheader("分析データの表示")

with st.container(border=True):
    tab1, tab2 = st.tabs(["人口ピラミッドを確認する", "過去からの推移を確認する"])

    with tab1:
        st.write(f"### {select_year}年の人口構成")
        
        # データの準備
        male_col = f"{select_year}_Male"
        female_col = f"{select_year}_Female"
        male_data = df[male_col]
        female_data = df[female_col]
        age_labels = df['age']

        fig = go.Figure()
        fig.add_trace(go.Bar(y=age_labels, x=male_data * -1, name='男性', orientation='h', marker=dict(color="#23a3ff")))
        fig.add_trace(go.Bar(y=age_labels, x=female_data, name='女性', orientation='h', marker=dict(color="#ff0ebb")))
        fig.update_layout(xaxis_title="人口（千人）", barmode='overlay', height=600)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("### データの考察")
        st.info("""
        2010年時のグラフから、以下の傾向が読み取れる：
        **高齢化の進行**: 若年層の割合が減り、65歳以上の層が厚くなっていることがピラミッド形状からも確認できる。
        """)

    with tab2:
        st.write("### 人口の長期推移")
        
        years_list, total_pop, male_pop, female_pop = [], [], [], []
        for y in year:
            m_sum = df[f"{y}_Male"].sum()
            f_sum = df[f"{y}_Female"].sum()
            years_list.append(y)
            male_pop.append(m_sum)
            female_pop.append(f_sum)
            total_pop.append(m_sum + f_sum)

        fig_line = go.Figure()
        if 'Total' in selected_color_label:
            fig_line.add_trace(go.Scatter(x=years_list, y=total_pop, name='合計', mode='lines+markers', line=dict(color='gray')))
        if 'male' in selected_color_label:
            fig_line.add_trace(go.Scatter(x=years_list, y=male_pop, name='男性', mode='lines+markers', line=dict(color='#23a3ff')))
        if 'female' in selected_color_label:
            fig_line.add_trace(go.Scatter(x=years_list, y=female_pop, name='女性', mode='lines+markers', line=dict(color='#ff0ebb')))

        fig_line.add_vline(x=select_year, line_width=2, line_dash="dash", line_color="green", annotation_text=f"{select_year}年を選択中")
        
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("### データの考察")
        st.info("""
        グラフの推移から、以下の傾向が読み取れる：
        **総人口のピークアウト**: 2010年前後を境に、総人口が減少傾向に転じている。
        """)