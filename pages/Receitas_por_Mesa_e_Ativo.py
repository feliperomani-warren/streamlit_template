import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from login import check_password
from datetime import date

st.set_page_config(page_title="Resultados Warren Rena", page_icon="assets/LogoW.png", layout="wide", initial_sidebar_state="expanded")

st.logo("assets/LogoWarrenRena.png", icon_image="assets/LogoWRena.png")

if not check_password():
    st.stop()

color_scale_desks = alt.Scale(
    domain=['TP', 'BMF', 'BOV', 'CP'],
    range=['#C64F39', '#34639C', '#AC783F', '#7E527A']
)

color_scale_assets = alt.Scale(
    domain=['NTN-B/C','2a volta', "LFT", "BMF", 'LTN', 'B CASADA', "DI", 'DAP', "DEBENTURE", 'NTN-F', 'BOV', 'LF', 'CRA'],
    range=['#C64F39', '#AC783F', '#D8A370', '#34639C','#D3944E', '#A2402F', "#44737E", '#749EA9', '#51448C', '#BC6672', '#7E527A', '#913042', '#7E74B7']
)

@st.cache_data
def load_data():
    df_INOA = pd.read_excel("data/Mapa de Resultados Institucional v1.xlsx", sheet_name="Receitas INOA", usecols=["Pregao", "reference_month", "Bolsa (XBMF/XBSP)", "Corretagem"])
    df_INOA = df_INOA.rename(columns={"Pregao":"reference_day", "Bolsa (XBMF/XBSP)": "desk_name", "Corretagem":"revenue"})
    df_INOA['reference_month'] = pd.to_datetime(df_INOA['reference_month']).dt.date
    # df_INOA['reference_day'] = pd.to_datetime(df_INOA['reference_day']).dt.date
    df_INOA["asset_name"] = df_INOA["desk_name"]
    df_INOA = df_INOA[["reference_month", "reference_day", "desk_name", "revenue", "asset_name"]]

    df_ADROIT = pd.read_excel("data/Mapa de Resultados Institucional v1.xlsx", sheet_name="Receitas TP", usecols=["reference_month", "reference_day","asset-name", "desk_name", "revenue"])
    df_ADROIT = df_ADROIT.rename(columns={"asset-name":"asset_name"})
    df_ADROIT['reference_month'] = pd.to_datetime(df_ADROIT['reference_month']).dt.date
    # df_ADROIT['reference_day'] = pd.to_datetime(df_ADROIT['reference_day']).dt.date
    
    df = pd.concat([df_INOA, df_ADROIT], ignore_index=True).dropna(how='all')
    df = df.groupby(["reference_month", "reference_day", "desk_name", "asset_name"])["revenue"].sum().reset_index()
    df['year'] = pd.to_datetime(df['reference_day']).dt.year
    df['quarter'] = pd.to_datetime(df['reference_day']).dt.quarter
    df['month'] = pd.to_datetime(df['reference_day']).dt.month
    df['week'] = pd.to_datetime(df['reference_day']).dt.isocalendar().week
    df["month_day"] = df["reference_day"].dt.strftime("%m-%d")
    df['reference_day'] = pd.to_datetime(df['reference_day']).dt.date
    # df = pd.read_csv("data/df.csv", dtype={
    # "desk_name": "string",
    # "asset_name": "string",
    # "revenue": "float",
    # "year": "int",
    # "quarter": "int",
    # "month": "int",
    # "week": "int",
    # "reference_month": "string",
    # "reference_day": "string"})
    # df['reference_month'] = pd.to_datetime(df['reference_month']).dt.date
    # df['reference_day'] = pd.to_datetime(df['reference_day']).dt.date
    return df

if "df" not in st.session_state:
    st.session_state['df'] = load_data()

df = st.session_state['df']

st.title(":material/attach_money: Receitas por Mesa e Ativo")

with st.sidebar:
    st.subheader("Filtro :material/filter_list:")
    with st.expander("Selecione o período a ser analisado"):
        periodo = st.slider("Período", min_value= df["reference_day"].min(), max_value=df["reference_day"].max() ,value=(date(2025, 1, 2), df["reference_day"].max()))
        data_inicial, data_final = periodo
        
        # col1,col2 = st.columns([2,2])
        # with col1:
        #     data_inicial = st.date_input("De:", value=data_inicial ,min_value=df["reference_day"].min() ,max_value=df["reference_day"].max())
        # with col2:
        #     data_final = st.date_input("Até:", value=data_final, min_value=df["reference_day"].min() ,max_value=df["reference_day"].max())
        
        df = df[(df['reference_day'] >= data_inicial) & (df['reference_day'] <= data_final)]
        
    with st.expander("Selecione a mesa:"):
        mesas = st.multiselect("Mesa", df["desk_name"].unique(), default=df["desk_name"].unique())
        df = df[df["desk_name"].isin(mesas)]
        
    with st.expander("Selecione o ativo:"):
        ativos = st.multiselect("Ativo", df["asset_name"].unique(), default=df["asset_name"].unique())
        df = df[df["asset_name"].isin(ativos)]
        
    st.write("---")
    if st.button("Logout"):
        st.session_state['password_correct'] = False
        st.rerun()
        
col1, col2 = st.columns([4,6])

with col1:
    st.write("Receita por Mesa")
    df1 = df.groupby(["desk_name"])["revenue"].sum().reset_index().sort_values('revenue', ascending=False)
    chart = alt.Chart(df1).mark_bar(color="#C7452D").encode(
        x='revenue',
        y=alt.Y('desk_name', sort='-x'),
        tooltip=[alt.Tooltip('revenue', format='$,.2f')]
    ).properties(
        height=400,
        width=800
    )

    st.altair_chart(chart, use_container_width=True)

with col2:
    st.write("Receita por Ativo")
    df2 = df.groupby("asset_name")["revenue"].sum().reset_index().sort_values('revenue', ascending=False)

    chart = alt.Chart(df2).mark_bar(color="#AC783F").encode(
        x='revenue',
        y=alt.Y('asset_name', sort='-x'),
        tooltip=[alt.Tooltip('revenue', format='$,.2f')]
    ).properties(
        height=400,
        width=800
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

st.write("-------------------------------------------------------------------------------------------")

col1, col2 = st.columns([4,6])

with col1:
    gran = "reference_month"
    granularidade = st.pills("Receita por Mesa", ["Mês","Dia"], selection_mode="single", default="Mês",key="receita_por_mesa")
    if granularidade == "Dia":
        gran = "reference_day"
    elif granularidade == "Mês":
        gran = "reference_month"
    
    df3 = df.groupby([gran, "desk_name"])["revenue"].sum().reset_index()
    
    chart = alt.Chart(df3).mark_line(strokeWidth=3).encode(
        x=gran,
        y='revenue',
        color=alt.Color('desk_name', 
                    scale=color_scale_desks,
                    legend=alt.Legend(orient="bottom")
                   ),
        tooltip=[
            alt.Tooltip(gran, title='Data', format="%Y-%m-%d"),
            alt.Tooltip('desk_name', title='Mesa'),
            alt.Tooltip('revenue', title='Receita', format="$,.2f")
        ]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

with col2:
    gran4 = "reference_month"
    granularidade4 = st.pills("Receita por Ativo", ["Mês","Dia"], selection_mode="single", default="Mês",key="receita_por_ativo")
    if granularidade4 == "Dia":
        gran4 = "reference_day"
    elif granularidade4 == "Mês":
        gran4 = "reference_month"
    
    df4 = df.groupby([gran4, "asset_name"])["revenue"].sum().reset_index()
    
    chart = alt.Chart(df4).mark_line(strokeWidth=3).encode(
    x=gran4,
    y='revenue',
    color=alt.Color('asset_name', 
                    scale=color_scale_assets,
                    legend=alt.Legend(orient="bottom")
                   ),
    tooltip=[
        alt.Tooltip(gran4, title='Data', format="%Y-%m-%d"),
        alt.Tooltip('asset_name', title='Ativo'),
        alt.Tooltip('revenue', title='Receita', format="$,.2f")
    ]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

st.write("-------------------------------------------------------------------------------------------")
col1, col2 = st.columns([5,5])

with col1:
    df_grouped = df.groupby(['reference_day','desk_name'])['revenue'].sum().reset_index()
    df_pivot = df_grouped.pivot_table(values="revenue",
                          index="reference_day",
                          columns='desk_name',
                          aggfunc='sum',
                          fill_value=0).reset_index()
    colors = ['#B23B51', '#D3944E', '#41864D']
    custom_cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)
    df_styled = df_pivot.style.background_gradient(
    cmap=custom_cmap,
    subset=df_pivot.columns[1:],
    vmin=df_pivot.iloc[:, 1:].min().min(),
    vmax=df_pivot.iloc[:, 1:].max().max()
).format("${:,.2f}", subset=df_pivot.columns[1:])
    st.write("Desempenho Diário das Mesas")
    st.dataframe(df_styled, hide_index=True)

with col2:
    df_grouped = df.groupby(['reference_month','desk_name'])['revenue'].sum().reset_index()
    df_pivot = df_grouped.pivot_table(values="revenue",
                          index="reference_month",
                          columns='desk_name',
                          aggfunc='sum',
                          fill_value=0).reset_index()

    colors = ['#B23B51', '#D3944E', '#41864D']
    custom_cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)
    df_styled = df_pivot.style.background_gradient(
        cmap=custom_cmap,
        subset=df_pivot.columns[1:],
        vmin=df_pivot.iloc[:, 1:].min().min(),
        vmax=df_pivot.iloc[:, 1:].max().max()
        ).format("${:,.2f}", subset=df_pivot.columns[1:])
    st.write("Desempenho Mensal das Mesas")
    st.dataframe(df_styled, hide_index=True)